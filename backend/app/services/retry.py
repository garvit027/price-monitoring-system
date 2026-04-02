import asyncio

async def retry(func, *args, retries=3, delay=1, **kwargs):
    for attempt in range(retries):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            print(f"Retry {attempt+1} failed: {e}")
            await asyncio.sleep(delay)
    print("❌ All retries failed")
    raise Exception("Max retries exceeded")