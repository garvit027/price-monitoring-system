import sys
import asyncio
import json
from bs4 import BeautifulSoup
from app.services.scraper import fetch_page_content
from app.services.parsers.flipkart import parse

async def main():
    url = "https://www.flipkart.com/hillgrove-electric-gadget-8in1-new-mobile-soldering-iron-equipment-tool-machine-combo-kit-set-flux-paste-wire-25-w-simple/p/itm69b963f2cf099?pid=SOIGFTPZ9A4TJGBD"
    html = await fetch_page_content(url)
    soup = BeautifulSoup(html, "html.parser")
    for script in soup.find_all("script", type="application/ld+json"):
        data = json.loads(script.string or "")
        items = data if isinstance(data, list) else [data]
        for item in items:
             if isinstance(item, dict) and "offers" in item:
                 print("JSON-LD offers:", item["offers"])

    price_selectors = [
        ("div", {"class": "_30jeq3"}),
        ("div", {"class": "_30jeq3 _16Jk6d"}),
        ("div", {"class": "Nx9bqj"}),
        ("div", {"class": "_16Jk6d"}),
    ]
    for tag, attrs in price_selectors:
        els = soup.find_all(tag, attrs)
        for el in els:
            print(f"Fallback {tag} {attrs}: {el.get_text(strip=True)}")

asyncio.run(main())
