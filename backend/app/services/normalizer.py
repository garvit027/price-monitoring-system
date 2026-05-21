import html
import re

def clean_product_data(parsed_data: dict, source_name: str, url: str) -> dict:
    """
    Cleans up the raw parsed data to make it extremely clean and accurate.
    Removes HTML entities, prefixes like 'Amazon.com: ', and sets proper defaults.
    """
    name = parsed_data.get("name", "Unknown Product")
    
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
        
    return {
        "name": name[:500],
        "brand": brand[:200],
        "category": parsed_data.get("category", "General")[:200],
        "source": source_name,
        "external_id": str(parsed_data.get("external_id", hash(url))),
        "price": float(parsed_data.get("price", 0.0) or 0.0),
        "image": parsed_data.get("image"),
        "url": url
    }