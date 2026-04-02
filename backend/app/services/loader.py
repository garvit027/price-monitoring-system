import os
import json
import asyncio
import aiofiles

DATASET_PATH = "dataset/sample_products"

async def fetch_file(file_path):
    # Simulate network call delay
    await asyncio.sleep(0.1)
    async with aiofiles.open(file_path, "r") as f:
        content = await f.read()
        return json.loads(content)

async def load_products():
    from app.services.retry import retry
    
    for root, _, files in os.walk(DATASET_PATH):
        for filename in files:
            if not filename.endswith(".json"):
                continue

            file_path = os.path.join(root, filename)

            try:
                data = await retry(fetch_file, file_path)
                yield data, filename
            except Exception as e:
                print(f"Error reading {filename}: {e}")