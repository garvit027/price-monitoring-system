from bs4 import BeautifulSoup
import re
import json

def parse(data):
    if isinstance(data, str) and "<html" in data.lower():
        soup = BeautifulSoup(data, "html.parser")
        result = {"source": "Grailed"}
        
        # Method 1: JSON-LD or structured data
        scripts = soup.find_all("script", type="application/ld+json")
        for script in scripts:
            try:
                content = json.loads(script.string)
                if isinstance(content, dict) and content.get("@type") == "Product":
                    offers = content.get("offers")
                    if isinstance(offers, dict) and offers.get("price"):
                        result["price"] = float(str(offers["price"]).replace(",", ""))
                    
                    result["name"] = content.get("name")
                    result["brand"] = content.get("brand", {}).get("name") if isinstance(content.get("brand"), dict) else content.get("brand")
                    result["image"] = content.get("image")
                    result["category"] = "Apparel"
            except (json.JSONDecodeError, ValueError, KeyError):
                continue

        # Fallback to meta tags
        if "price" not in result:
            desc_meta = soup.find("meta", property="og:description")
            if desc_meta:
                match = re.search(r"\$([\d,]+)", desc_meta["content"])
                if match:
                    result["price"] = float(match.group(1).replace(",", ""))

        if "name" not in result:
            title_meta = soup.find("meta", property="og:title")
            if title_meta:
                result["name"] = title_meta["content"].split(" | ")[0]

        # External ID from URL
        url_meta = soup.find("link", rel="canonical")
        if url_meta:
            match = re.search(r"/listings/(\d+)", url_meta["href"])
            if match:
                result["external_id"] = match.group(1)

        return result

    return data