from curl_cffi.requests import AsyncSession
import re
from bs4 import BeautifulSoup
import logging
from app.services.scraper import HEADERS

logger = logging.getLogger(__name__)

MARKETPLACES = {
    "Fashionphile": "https://www.fashionphile.com/shop",
    "Grailed": "https://www.grailed.com/shop",
    "1stdibs": "https://www.1stdibs.com/fashion/",
    "Flipkart": "https://www.flipkart.com/search?q=electronics",
    "Ebay": "https://www.ebay.com/sch/i.html?_nkw=electronics",
    "Myntra": "https://www.myntra.com/men-tshirts",
    "Etsy": "https://www.etsy.com/search?q=handmade",
}


async def discover_new_urls(source: str) -> list[str]:
    """
    Scrapes the marketplace gallery to find product URLs using curl_cffi.
    """
    url = MARKETPLACES.get(source)
    if not url:
        return []

    try:
        async with AsyncSession(impersonate="chrome120", timeout=25.0) as client:
            response = await client.get(url, headers=HEADERS)
            response.raise_for_status()
            html = response.text

            urls = []

            if source == "Fashionphile":
                found = re.findall(r'href="(/products/[^"]+)"', html)
                urls = [f"https://www.fashionphile.com{link}" for link in found if "products/" in link]

            elif source == "Grailed":
                found = re.findall(r'href="(/listings/\d+[^"]*)"', html)
                urls = [f"https://www.grailed.com{link}" for link in found]

            elif source == "1stdibs":
                found = re.findall(r'href="(/fashion/[^"]+/id-[^"]+)"', html)
                urls = [f"https://www.1stdibs.com{link}" for link in found]

            elif source == "Amazon":
                # Find product links /dp/ASINCODE
                found = re.findall(r'href="(/[^"]+/dp/[A-Z0-9]{10}[^"]*)"', html)
                urls = list(set([f"https://www.amazon.com{link.split('?')[0]}" for link in found]))

            elif source == "Flipkart":
                soup = BeautifulSoup(html, "html.parser")
                for a in soup.find_all("a", href=True):
                    href = a["href"]
                    if "/p/" in href:
                        urls.append(f"https://www.flipkart.com{href}" if not href.startswith("http") else href)

            elif source == "Ebay":
                found = re.findall(r'https://www\.ebay\.com/itm/\d+', html)
                urls = list(set(found))

            elif source == "Myntra":
                found = re.findall(r'https://www\.myntra\.com/[^"]+/buy', html)
                urls = list(set(found))

            elif source == "Etsy":
                found = re.findall(r'https://www\.etsy\.com/listing/\d+', html)
                urls = list(set(found))

            # Unique and limited per source per run
            unique_urls = list(set(urls))
            logger.info(f"Discovered {len(unique_urls)} URLs from {source}")
            return unique_urls[:50]  # cap per source

    except Exception as e:
        logger.error(f"Discovery failed for {source}: {e}")
        return []


async def discover_all() -> dict[str, list[str]]:
    results = {}
    for source in MARKETPLACES.keys():
        results[source] = await discover_new_urls(source)
    return results
