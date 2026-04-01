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
    if not image and "main_images" in data:
        image = data["main_images"][0] if data["main_images"] else None

    return {
        "name": name,
        "brand": brand,
        "category": category,
        "source": source,
        "external_id": data.get("product_id"),
        "price": data.get("price", 0),
        "image": image,
        "url": data.get("product_url")
    }