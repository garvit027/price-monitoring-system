import sys
import asyncio
import json
from bs4 import BeautifulSoup
from app.services.scraper import fetch_page_content

async def main():
    url = "https://www.flipkart.com/hillgrove-electric-gadget-8in1-new-mobile-soldering-iron-equipment-tool-machine-combo-kit-set-flux-paste-wire-25-w-simple/p/itm69b963f2cf099?pid=SOIGFTPZ9A4TJGBD"
    html = await fetch_page_content(url)
    soup = BeautifulSoup(html, "html.parser")

    print("--- ALL Nx9bqj elements ---")
    for el in soup.find_all("div", {"class": "Nx9bqj"}):
        print(el.get_text(strip=True))

asyncio.run(main())
