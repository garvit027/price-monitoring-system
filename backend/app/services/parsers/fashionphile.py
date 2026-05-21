from bs4 import BeautifulSoup
import re
import json

def parse(data):
    if isinstance(data, str) and "<html" in data.lower():
        soup = BeautifulSoup(data, "html.parser")
        
        # Base result
        result = {"source": "Fashionphile"}
        
        # 1. Price
        price_meta = soup.find("meta", property="og:price:amount")
        if price_meta and price_meta.get("content"):
            result["price"] = float(price_meta["content"].replace(",", ""))
        
        # 2. Metadata (Name, Brand, Image)
        title_meta = soup.find("meta", property="og:title")
        if title_meta:
            name_str = title_meta["content"].split(" – ")[0]
            result["name"] = name_str
            # Use the first 2 words of the title as a fallback brand, e.g., 'Bottega Veneta'
            parts = name_str.split(" ")
            result["brand"] = " ".join(parts[:2]) if len(parts) >= 2 else parts[0]

        desc_meta = soup.find("meta", property="og:description")
        if desc_meta:
            # Try to extract the all-caps brand after 'authentic '
            brand_match = re.search(r"authentic\s+([A-Z0-9\s&]+?)(?:\s+[A-Z][a-z]|\s+Nappa|\s+Canvas|\s+Leather)", desc_meta["content"])
            if brand_match:
                result["brand"] = brand_match.group(1).strip().title()

        img_meta = soup.find("meta", property="og:image")
        if img_meta:
            result["image"] = img_meta["content"]

        # External ID from URL or meta
        url_meta = soup.find("link", rel="canonical")
        if url_meta:
            match = re.search(r"-(\d+)$", url_meta["href"])
            if match:
                result["external_id"] = match.group(1)
        
        # Category
        if "necklace" in result.get("name", "").lower() or "pendant" in result.get("name", "").lower():
            result["category"] = "Jewelry"
        else:
            result["category"] = "Accessories"

        return result
    
    return data