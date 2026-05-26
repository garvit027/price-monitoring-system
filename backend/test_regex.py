import re

def test_regex():
    with open('flipkart_debug.html', 'r') as f:
        html = f.read()
    
    match = re.search(r'₹\s*([\d,]+)', html)
    if match:
        print("Extracted price:", float(match.group(1).replace(",", "")))
    else:
        print("Not found")

test_regex()
