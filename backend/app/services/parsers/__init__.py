from .grailed import parse as grailed_parser
from .fashionphile import parse as fashionphile_parser
from .stdibs import parse as stdibs_parser

def get_parser(filename):
    if "grailed" in filename:
        return grailed_parser, "Grailed"
    elif "fashionphile" in filename:
        return fashionphile_parser, "Fashionphile"
    elif "1stdibs" in filename:
        return stdibs_parser, "1stdibs"
    return None, "Unknown"