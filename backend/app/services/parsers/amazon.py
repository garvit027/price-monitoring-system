from bs4 import BeautifulSoup
import re
import json


def parse(html: str) -> dict:
    """
    Parse Amazon product pages to extract price, name, brand, image, and category.
    Handles both regular and deal pages.
    """
    soup = BeautifulSoup(html, "html.parser")
    result = {}

    # --- Product Name ---
    name_tag = soup.find("span", {"id": "productTitle"})
    if name_tag:
        result["name"] = name_tag.get_text(strip=True)
    else:
        name_tag = soup.find("h1", {"id": "title"})
        result["name"] = name_tag.get_text(strip=True) if name_tag else "Unknown Product"

    # --- Brand ---
    brand_tag = soup.find("a", {"id": "bylineInfo"})
    if brand_tag:
        brand_text = brand_tag.get_text(strip=True)
        brand_text = re.sub(r"(Visit the |Store| Brand:)", "", brand_text).strip()
        result["brand"] = brand_text
    else:
        # Try tech specs table
        for row in soup.find_all("tr"):
            header = row.find("td", class_="a-span3")
            if header and "Brand" in header.get_text():
                val = row.find("td", class_="a-span9")
                if val:
                    result["brand"] = val.get_text(strip=True)
                    break
        if "brand" not in result:
            result["brand"] = "Amazon"

    # --- Price (multiple selectors for different page layouts) ---
    price = None
    price_selectors = [
        ("span", {"class": "a-price-whole"}),
        ("span", {"id": "priceblock_ourprice"}),
        ("span", {"id": "priceblock_dealprice"}),
        ("span", {"class": "a-offscreen"}),
        ("span", {"id": "price_inside_buybox"}),
    ]

    for tag, attrs in price_selectors:
        el = soup.find(tag, attrs)
        if el:
            text = el.get_text(strip=True).replace(",", "").replace("₹", "").replace("$", "").replace("£", "")
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
    img_tag = soup.find("img", {"id": "landingImage"}) or soup.find("img", {"id": "imgBlkFront"})
    if img_tag:
        result["image"] = img_tag.get("data-old-hires") or img_tag.get("src")

    # --- Category ---
    breadcrumbs = soup.find_all("a", {"class": "a-link-normal a-color-tertiary"})
    if breadcrumbs:
        result["category"] = breadcrumbs[0].get_text(strip=True)
    else:
        result["category"] = "General"

    # --- External ID (ASIN) ---
    asin_match = re.search(r"/dp/([A-Z0-9]{10})", html)
    if asin_match:
        result["external_id"] = asin_match.group(1)

    return result
