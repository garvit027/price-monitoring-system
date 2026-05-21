from .grailed import parse as grailed_parser
from .fashionphile import parse as fashionphile_parser
from .stdibs import parse as stdibs_parser
from .amazon import parse as amazon_parser
from .flipkart import parse as flipkart_parser
from .generic import parse as generic_parser
import re


def get_parser(source_or_url):
    """
    Returns (parser_fn, source_name) based on the URL or source name.
    """
    s = str(source_or_url).lower()

    if "grailed" in s:
        return grailed_parser, "Grailed"
    elif "fashionphile" in s:
        return fashionphile_parser, "Fashionphile"
    elif "1stdibs" in s or "stdibs" in s:
        return stdibs_parser, "1stdibs"
    elif "amazon" in s:
        # Amazon requires its dedicated parser because it doesn't expose standard og:image or JSON-LD reliably.
        return amazon_parser, "Amazon"
    elif "myntra" in s:
        return generic_parser, "Myntra"
    elif "ebay" in s:
        return generic_parser, "Ebay"
    elif "etsy" in s:
        return generic_parser, "Etsy"

    domain_match = re.search(r"https?://(?:www\.)?([^/]+)", s)
    source_name = domain_match.group(1).split(".")[0].capitalize() if domain_match else "Unknown"

    return generic_parser, source_name