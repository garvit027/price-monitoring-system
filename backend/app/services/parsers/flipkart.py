from bs4 import BeautifulSoup
import re
import json


def parse(html: str) -> dict:
    """
    Parse Flipkart product pages to extract price, name, brand, image, and category.
    """
    soup = BeautifulSoup(html, "html.parser")
    result = {}

    # --- Product Name ---
    name_tag = (
        soup.find("span", {"class": "B_NuCI"})
        or soup.find("h1", {"class": "yhB1nd"})
        or soup.find("span", {"class": "_35KyD6"})
        or soup.find("h1")
    )
    result["name"] = name_tag.get_text(strip=True) if name_tag else "Unknown Product"

    # --- Brand ---
    brand_tag = soup.find("span", {"class": "G6XhRU"})
    if not brand_tag:
        brand_tag = soup.find("a", {"class": "_2WhKV3"})
    result["brand"] = brand_tag.get_text(strip=True) if brand_tag else "Flipkart"

    # --- Price ---
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

    # JSON-LD fallback
    if not price:
        for script in soup.find_all("script", type="application/ld+json"):
            try:
                data = json.loads(script.string or "")
                if isinstance(data, dict) and "offers" in data:
                    offers = data["offers"]
                    if isinstance(offers, dict):
                        price = float(offers.get("price", 0))
                    elif isinstance(offers, list) and offers:
                        price = float(offers[0].get("price", 0))
                if price:
                    break
            except Exception:
                continue

    result["price"] = price or 0.0

    # --- Image ---
    img_tag = soup.find("img", {"class": "_396cs4"}) or soup.find("img", {"class": "_2r_T1I"})
    if not img_tag:
        img_tag = soup.find("div", {"class": "_3kiddo"})
        if img_tag:
            img_tag = img_tag.find("img")
    result["image"] = img_tag.get("src") if img_tag else None

    # --- Category ---
    breadcrumb = soup.find_all("a", {"class": "_2whKao"})
    if breadcrumb:
        result["category"] = breadcrumb[0].get_text(strip=True)
    else:
        result["category"] = "General"

    return result
