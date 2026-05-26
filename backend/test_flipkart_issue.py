import asyncio
from app.services.scraper import fetch_page_content
from app.services.parsers.flipkart import parse

async def main():
    url = "https://www.flipkart.com/apple-iphone-15-black-128-gb/p/itm6ac6485515ae4?pid=MOBGTAGPTB3VS24W&lid=LSTMOBGTAGPTB3VS24WVZNSZF&marketplace=FLIPKART&q=iphone+15&store=tyy%2F4io&srno=s_1_1&otracker=search&otracker1=search&fm=organic&iid=a8d85fcd-9b9f-4318-971c-4b5f49e0a811.MOBGTAGPTB3VS24W.SEARCH&ppt=hp&ppn=homepage&ssid=w5oix8l2xs0000001716592275955&qH=2f54b45b321e3ae5"
    html = await fetch_page_content(url)
    if not html:
        print("Failed to fetch")
        return
    res = parse(html)
    print("Parsed Result:", res)

if __name__ == "__main__":
    asyncio.run(main())
