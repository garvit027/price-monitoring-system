import asyncio
from app.services.discovery import discover_all

async def test():
    results = await discover_all()
    for source, urls in results.items():
        print(f"{source}: {len(urls)} URLs")
        if urls:
            print(f"Sample: {urls[0]}")

if __name__ == "__main__":
    asyncio.run(test())
