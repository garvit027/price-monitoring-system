import html
import re

def clean_product_data(parsed_data: dict, source_name: str, url: str) -> dict:
    """
    Cleans up the raw parsed data to make it extremely clean and accurate.
    Removes HTML entities, prefixes like 'Amazon.com: ', and sets proper defaults.
    """
    name = parsed_data.get("name") or parsed_data.get("model") or "Unknown Product"
    
    # 1. Unescape HTML entities (&amp; -> &)
    name = html.unescape(name)
    
    # 2. Strip garbage prefixes/suffixes
    name = re.sub(r"^Amazon\.com:\s*", "", name, flags=re.IGNORECASE)
    name = re.sub(r"\s*:\s*Electronics.*$", "", name, flags=re.IGNORECASE)
    name = re.sub(r"Buy Online at Best Prices.*$", "", name, flags=re.IGNORECASE)
    name = re.sub(r"\.\.\.more$", "", name, flags=re.IGNORECASE)
    
    # 3. Clean up whitespace
    name = " ".join(name.split())
    
    brand = parsed_data.get("brand", "")
    brand = html.unescape(brand) if brand else "Unknown"
    if brand.lower() in ["unknown", "", "amazon", "flipkart"] and source_name not in ["Amazon", "Flipkart"]:
        # Don't let the marketplace be the brand
        pass
        
    image = parsed_data.get("image")
    if not image and "main_images" in parsed_data and isinstance(parsed_data["main_images"], list) and len(parsed_data["main_images"]) > 0:
        image = parsed_data["main_images"][0].get("url")
        
    return {
        "name": name[:500],
        "brand": brand[:200],
        "category": parsed_data.get("category", "General")[:200],
        "source": source_name,
        "external_id": str(parsed_data.get("external_id", hash(url))),
        "price": float(parsed_data.get("price", 0.0) or 0.0),
        "image": image,
        "url": url
    }


def is_valid_product(product_data: dict) -> bool:
    """
    Validates if the product data is correct and not a bot-check page or broken scrape.
    """
    if not product_data:
        return False
        
    if product_data.get("price", 0.0) <= 0:
        return False
        
    if not product_data.get("image"):
        return False
        
    name = product_data.get("name", "").strip().lower()
    
    invalid_exact_names = {
        "unknown product", "amazon.com", "amazon.in", "prime", "amazon prime",
        "robot check", "bot check", "captcha", "no product", "amazon"
    }
    
    if not name or len(name) < 5:
        return False
        
    if name in invalid_exact_names:
        return False
        
    if "robot check" in name or "captcha" in name:
        return False

    return True