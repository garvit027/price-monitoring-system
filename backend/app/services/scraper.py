import httpx
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

async def fetch_page_content(url: str) -> str:
    """
    Fetches the HTML content of a given URL.
    """
    async with httpx.AsyncClient(headers=HEADERS, follow_redirects=True, timeout=15.0) as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            return response.text
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error occurred: {e.response.status_code} for URL: {url}")
            return ""
        except Exception as e:
            logger.error(f"An error occurred while fetching {url}: {str(e)}")
            return ""

def get_soup(html: str) -> BeautifulSoup:
    """
    Returns a BeautifulSoup object from HTML string.
    """
    return BeautifulSoup(html, "html.parser")
