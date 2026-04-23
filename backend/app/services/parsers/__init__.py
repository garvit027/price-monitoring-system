from .grailed import parse as grailed_parser
from .fashionphile import parse as fashionphile_parser
from .stdibs import parse as stdibs_parser

def get_parser(source_or_url):
    """
    Returns the appropriate parser based on the filename, source name, or URL.
    """
    s = str(source_or_url).lower()
    
    if "grailed" in s:
        return grailed_parser, "Grailed"
    elif "fashionphile" in s:
        return fashionphile_parser, "Fashionphile"
    elif "1stdibs" in s or "stdibs" in s:
        return stdibs_parser, "1stdibs"
    
    return None, "Unknown"