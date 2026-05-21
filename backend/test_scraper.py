import asyncio
from app.services.scraper import fetch_page_content

async def main():
    print("Testing Grailed...")
    html_g = await fetch_page_content("https://www.grailed.com/listings/12345")
    print("Grailed HTML length:", len(html_g))
    
    print("Testing 1stdibs...")
    html_1 = await fetch_page_content("https://www.1stdibs.com/fashion/accessories/belts/chanel-gold-tone-metal-92a-coco-chanel-chain-belt-oz/id-v_28218692/")
    print("1stdibs HTML length:", len(html_1))

if __name__ == "__main__":
    asyncio.run(main())
