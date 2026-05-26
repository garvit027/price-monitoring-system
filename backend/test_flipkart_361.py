import sys
import asyncio
from app.services.scraper import fetch_page_content

async def main():
    url = "https://www.flipkart.com/hillgrove-electric-gadget-8in1-new-mobile-soldering-iron-equipment-tool-machine-combo-kit-set-flux-paste-wire-25-w-simple/p/itm69b963f2cf099?pid=SOIGFTPZ9A4TJGBD"
    html = await fetch_page_content(url)
    if "361" in html:
        print("Found 361 in HTML!")
        lines = html.split('\n')
        for i, line in enumerate(lines):
            if "361" in line:
                print(f"Line {i}: {line[:100]}...")

asyncio.run(main())
