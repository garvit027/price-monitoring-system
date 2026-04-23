from bs4 import BeautifulSoup
import re
import json

def parse(data):
    if isinstance(data, str) and "<html" in data.lower():
        soup = BeautifulSoup(data, "html.parser")
        result = {"source": "1stdibs"}
        
        # Method 1: JSON-LD
        scripts = soup.find_all("script", type="application/ld+json")
        for script in scripts:
            try:
                content = json.loads(script.string)
                if isinstance(content, dict) and content.get("@type") == "Product":
                    offers = content.get("offers")
                    if isinstance(offers, dict):
                        if offers.get("price"):
                            result["price"] = float(str(offers["price"]).replace(",", ""))
                        elif offers.get("lowPrice"):
                            result["price"] = float(str(offers["lowPrice"]).replace(",", ""))
                    
                    result["name"] = content.get("name")
                    result["brand"] = content.get("brand", {}).get("name") if isinstance(content.get("brand"), dict) else content.get("brand")
                    result["image"] = content.get("image")
                    result["category"] = "Accessories"
                    
                    # External ID from SKU or URL
                    result["external_id"] = content.get("sku")
            except (json.JSONDecodeError, ValueError):
                continue
        
        # Fallback for External ID from URL if not in JSON
        if "external_id" not in result:
            url_meta = soup.find("link", rel="canonical")
            if url_meta:
                 match = re.search(r"id-([v_\d]+)", url_meta["href"])
                 if match:
                     result["external_id"] = match.group(1)

        return result

    return data