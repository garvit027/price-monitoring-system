import httpx
import re
from bs4 import BeautifulSoup
import logging
from app.services.scraper import HEADERS

logger = logging.getLogger(__name__)

MARKETPLACES = {
    "Fashionphile": "https://www.fashionphile.com/shop",
    "Grailed": "https://www.grailed.com/shop",
    "1stdibs": "https://www.1stdibs.com/fashion/",
}

async def discover_new_urls(source: str) -> list[str]:
    """
    Scrapes the marketplace gallery to find product URLs.
    """
    url = MARKETPLACES.get(source)
    if not url:
        return []

    try:
        async with httpx.AsyncClient(headers=HEADERS, follow_redirects=True, timeout=15.0) as client:
            response = await client.get(url)
            response.raise_for_status()
            html = response.text
            
            urls = []
            if source == "Fashionphile":
                # Find links like /products/name-id
                found = re.findall(r'href="(/products/[^"]+)"', html)
                urls = [f"https://www.fashionphile.com{link}" for link in found if "products/" in link]
            
            elif source == "Grailed":
                # Find links like /listings/id
                found = re.findall(r'href="(/listings/\d+[^"]*)"', html)
                urls = [f"https://www.grailed.com{link}" for link in found]
            
            elif source == "1stdibs":
                # Find links like /fashion/.../id-v_...
                found = re.findall(r'href="(/fashion/[^"]+/id-[^"]+)"', html)
                urls = [f"https://www.1stdibs.com{link}" for link in found]

            # Unique and limited to ~20 per source per run
            unique_urls = list(set(urls))
            logger.info(f"Discovered {len(unique_urls)} URLs from {source}")
            return unique_urls[:20]

    except Exception as e:
        logger.error(f"Discovery failed for {source}: {e}")
        return []

async def discover_all() -> dict[str, list[str]]:
    results = {}
    for source in MARKETPLACES.keys():
        results[source] = await discover_new_urls(source)
    return results
