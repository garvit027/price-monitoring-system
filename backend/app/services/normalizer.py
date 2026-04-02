def normalize(data, source, filename):
    brand = data.get("brand", "")
    model = data.get("model", "")
    name = f"{brand} {model}".strip()

    # category detection
    if "apparel" in filename:
        category = "Apparel"
    elif "belts" in filename:
        category = "Accessories"
    elif "tiffany" in filename:
        category = "Jewelry"
    else:
        category = "Other"

    # image handling
    image = data.get("image_url")
    if not image and "main_images" in data and data["main_images"]:
        first_img = data["main_images"][0]
        image = first_img.get("url") if isinstance(first_img, dict) else first_img

    price = data.get("price", 0)
    
    # 💥 SIMULATION: Inject random market volatility for demonstration
    import random
    if price > 0 and random.random() < 0.3:
        fluctuation = price * 0.05 * (random.random() * 2 - 1)
        price = round(price + fluctuation, 2)

    return {
        "name": name,
        "brand": brand,
        "category": category,
        "source": source,
        "external_id": data.get("product_id"),
        "price": price,
        "image": image,
        "url": data.get("product_url")
    }