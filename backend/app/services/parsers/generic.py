from bs4 import BeautifulSoup
import re
import json


def parse(html: str) -> dict:
    """
    Generic parser that works for any website using:
    1. JSON-LD Product schema
    2. Open Graph meta tags
    3. Common CSS patterns for price
    """
    soup = BeautifulSoup(html, "html.parser")
    result = {}

    # ---- 1. JSON-LD Schema.org Product ----
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(script.string or "")
            # Handle array of schemas
            if isinstance(data, list):
                for item in data:
                    if item.get("@type") == "Product":
                        data = item
                        break
            if isinstance(data, dict) and data.get("@type") == "Product":
                result["name"] = data.get("name", "")
                result["brand"] = (
                    data.get("brand", {}).get("name", "") if isinstance(data.get("brand"), dict)
                    else str(data.get("brand", ""))
                )
                result["image"] = (
                    data["image"][0] if isinstance(data.get("image"), list)
                    else data.get("image", "")
                )
                offers = data.get("offers")
                if isinstance(offers, dict):
                    result["price"] = float(offers.get("price", 0))
                    result["category"] = offers.get("category", "General")
                elif isinstance(offers, list) and offers:
                    result["price"] = float(offers[0].get("price", 0))
                if result.get("name") and result.get("price"):
                    return result
        except Exception:
            continue

    # ---- 2. Open Graph fallback ----
    og_title = soup.find("meta", {"property": "og:title"})
    og_image = soup.find("meta", {"property": "og:image"})
    if og_title:
        result.setdefault("name", og_title.get("content", ""))
    if og_image:
        result.setdefault("image", og_image.get("content", ""))

    # ---- 3. Page title fallback ----
    if not result.get("name"):
        title = soup.find("title")
        result["name"] = title.get_text(strip=True) if title else "Unknown Product"

    # ---- 4. Price extraction (common patterns) ----
    if not result.get("price"):
        price_patterns = [
            r"[\$₹£€][\s]*([\d,]+\.?\d*)",
            r"([\d,]+\.?\d*)[\s]*[\$₹£€]",
        ]
        price_candidates = []

        # Common class names for prices
        for cls in ["price", "product-price", "sale-price", "current-price", "offer-price", "price__current"]:
            els = soup.find_all(class_=re.compile(cls, re.I))
            for el in els[:3]:
                text = el.get_text(strip=True)
                for pat in price_patterns:
                    match = re.search(pat, text)
                    if match:
                        try:
                            price_candidates.append(float(match.group(1).replace(",", "")))
                        except Exception:
                            pass

        if price_candidates:
            result["price"] = min(price_candidates)  # take lowest (current price)
        else:
            result["price"] = 0.0

    result.setdefault("brand", "Unknown")
    result.setdefault("category", "General")
    return result
