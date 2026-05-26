import sys
import asyncio
from bs4 import BeautifulSoup
from app.services.scraper import fetch_page_content

async def main():
    url = "https://www.flipkart.com/hillgrove-electric-gadget-8in1-new-mobile-soldering-iron-equipment-tool-machine-combo-kit-set-flux-paste-wire-25-w-simple/p/itm69b963f2cf099?pid=SOIGFTPZ9A4TJGBD"
    html = await fetch_page_content(url)
    soup = BeautifulSoup(html, "html.parser")
    
    # Search for any element containing the price text exactly
    for el in soup.find_all(text=lambda t: t and "390" in t):
        parent = el.parent
        print(f"Found '390' in tag <{parent.name}> with classes {parent.get('class')}")

asyncio.run(main())
