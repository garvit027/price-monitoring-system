from bs4 import BeautifulSoup
import re
import json


def parse(html: str) -> dict:
    """
    Parse Flipkart product pages to extract price, name, brand, image, and category.
    """
    soup = BeautifulSoup(html, "html.parser")
    result = {}

    # --- Robust JSON-LD parsing first ---
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(script.string or "")
            items = data if isinstance(data, list) else [data]
            for item in items:
                if not isinstance(item, dict):
                    continue
                # Extract product details
                if "name" in item and not result.get("name"):
                    result["name"] = item["name"]
                
                if "brand" in item and not result.get("brand"):
                    brand = item["brand"]
                    if isinstance(brand, dict) and "name" in brand:
                        result["brand"] = brand["name"]
                    elif isinstance(brand, str):
                        result["brand"] = brand
                
                if "category" in item and not result.get("category"):
                    result["category"] = item["category"]
                
                if "image" in item and not result.get("image"):
                    image = item["image"]
                    if isinstance(image, list) and image:
                        result["image"] = image[0]
                    elif isinstance(image, str):
                        result["image"] = image

                if "offers" in item and "price" not in result:
                    offers = item["offers"]
                    price = None
                    if isinstance(offers, dict):
                        price = offers.get("price")
                    elif isinstance(offers, list) and offers:
                        price = offers[0].get("price")
                    if price is not None:
                        try:
                            result["price"] = float(price)
                        except (ValueError, TypeError):
                            pass
        except Exception:
            continue

    # --- HTML / CSS Fallbacks ---
    
    # 1. Name Fallback
    if not result.get("name"):
        name_tag = (
            soup.find("span", {"class": "B_NuCI"})
            or soup.find("h1", {"class": "yhB1nd"})
            or soup.find("span", {"class": "_35KyD6"})
            or soup.find("h1")
        )
        result["name"] = name_tag.get_text(strip=True) if name_tag else "Unknown Product"

    # 2. Brand Fallback
    if not result.get("brand"):
        brand_tag = soup.find("span", {"class": "G6XhRU"})
        if not brand_tag:
            brand_tag = soup.find("a", {"class": "_2WhKV3"})
        result["brand"] = brand_tag.get_text(strip=True) if brand_tag else "Flipkart"

    # 3. Price Fallback
    if "price" not in result:
        price = None
        price_selectors = [
            ("div", {"class": "_30jeq3"}),
            ("div", {"class": "_30jeq3 _16Jk6d"}),
            ("div", {"class": "Nx9bqj"}),
            ("div", {"class": "_16Jk6d"}),
        ]
        for tag, attrs in price_selectors:
            el = soup.find(tag, attrs)
            if el:
                text = el.get_text(strip=True).replace(",", "").replace("₹", "").replace("$", "")
                numbers = re.findall(r"[\d.]+", text)
                if numbers:
                    try:
                        price = float(numbers[0])
                        break
                    except ValueError:
                        continue
        result["price"] = price or 0.0

    # 4. Image Fallback
    if not result.get("image"):
        img_tag = soup.find("img", {"class": "_396cs4"}) or soup.find("img", {"class": "_2r_T1I"})
        if not img_tag:
            img_tag = soup.find("div", {"class": "_3kiddo"})
            if img_tag:
                img_tag = img_tag.find("img")
        result["image"] = img_tag.get("src") if img_tag else None

    # 5. Category Fallback
    if not result.get("category"):
        breadcrumb = soup.find_all("a", {"class": "_2whKao"})
        if breadcrumb:
            result["category"] = breadcrumb[0].get_text(strip=True)
        else:
            result["category"] = "General"

    # Cleaning / Normalization formatting
    if "brand" in result:
        # Title case the brand for consistency (e.g. APPLE -> Apple)
        result["brand"] = str(result["brand"]).strip().title()

    return result
