import asyncio
from curl_cffi.requests import AsyncSession
from app.services.parsers.flipkart import parse

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
}

async def test():
    url = "https://www.flipkart.com/apple-iphone-15-pink-128-gb/p/itm6ac6485515ae4"
    async with AsyncSession(impersonate="chrome120") as client:
        response = await client.get(url, headers=HEADERS)
        print("Status:", response.status_code)
        
        with open("flipkart_test.html", "w") as f:
            f.write(response.text)
            
        parsed = parse(response.text)
        print("Parsed Data:", parsed)

if __name__ == "__main__":
    asyncio.run(test())
