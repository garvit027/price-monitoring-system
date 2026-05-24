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

    # --- Price Extraction ---
    price = None

    # 1. JSON-LD parsing (robust list/dict support)
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(script.string or "")
            items = data if isinstance(data, list) else [data]
            for item in items:
                if not isinstance(item, dict):
                    continue
                if "offers" in item:
                    offers = item["offers"]
                    val = None
                    if isinstance(offers, dict):
                        val = offers.get("price")
                    elif isinstance(offers, list) and offers:
                        val = offers[0].get("price")
                    if val is not None:
                        try:
                            price = float(val)
                            break
                        except (ValueError, TypeError):
                            pass
        except Exception:
            continue
        if price:
            break

    # 2. HTML CSS Selectors
    if not price:
        # We try to extract price from various selectors
        # Try a-offscreen first, as it contains full price with decimals (e.g. "$19.99")
        offscreen_tags = soup.find_all("span", class_="a-offscreen")
        for tag in offscreen_tags:
            text = tag.get_text(strip=True).replace(",", "").replace("₹", "").replace("$", "").replace("£", "")
            # Sometimes U+00A0 (non-breaking space) is present
            text = text.replace("\xa0", " ")
            numbers = re.findall(r"[\d.]+", text)
            if numbers:
                try:
                    val = float(numbers[0])
                    if val > 0:
                        price = val
                        break
                except ValueError:
                    continue

    if not price:
        # Try combining whole + fraction
        whole_el = soup.find("span", class_="a-price-whole")
        if whole_el:
            whole = whole_el.get_text(strip=True).replace(",", "").replace(".", "")
            fraction_el = whole_el.find_next_sibling("span", class_="a-price-fraction")
            fraction = fraction_el.get_text(strip=True) if fraction_el else "00"
            try:
                price = float(f"{whole}.{fraction}")
            except ValueError:
                pass

    if not price:
        # Other fallback selectors
        other_selectors = [
            ("span", {"id": "priceblock_ourprice"}),
            ("span", {"id": "priceblock_dealprice"}),
            ("span", {"id": "price_inside_buybox"}),
            ("span", {"class": "a-color-price"}),
            ("span", {"class": "apex-price-to-pay-value"}),
        ]
        for tag, attrs in other_selectors:
            el = soup.find(tag, attrs)
            if el:
                text = el.get_text(strip=True).replace(",", "").replace("₹", "").replace("$", "").replace("£", "")
                text = text.replace("\xa0", " ")
                numbers = re.findall(r"[\d.]+", text)
                if numbers:
                    try:
                        val = float(numbers[0])
                        if val > 0:
                            price = val
                            break
                    except ValueError:
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
