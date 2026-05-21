from app.services.parsers.generic import parse

with open("amazon_test.html") as f:
    print("Amazon:", parse(f.read()))

with open("flipkart_test.html") as f:
    print("Flipkart:", parse(f.read()))
