import sys
import asyncio
from bs4 import BeautifulSoup
from app.services.scraper import fetch_page_content

async def main():
    url = "https://www.flipkart.com/hillgrove-electric-gadget-8in1-new-mobile-soldering-iron-equipment-tool-machine-combo-kit-set-flux-paste-wire-25-w-simple/p/itm69b963f2cf099?pid=SOIGFTPZ9A4TJGBD"
    html = await fetch_page_content(url)
    soup = BeautifulSoup(html, "html.parser")
    
    price_selectors = [
        ("div", {"class": "Nx9bqj CxhGGd"}),
        ("div", {"class": "Nx9bqj"}),
        ("div", {"class": "_30jeq3 _16Jk6d"}),
    ]
    for tag, attrs in price_selectors:
        el = soup.find(tag, attrs)
        if el:
            print(f"Match {tag} {attrs}: {el.get_text(strip=True)}")

asyncio.run(main())
