import json
from config import CACHE_JSON

def save_to_cache(product_name: str, image_url: str):
    """
    Save the image URL to the cache JSON file for the given product,
    using the cache structure with keys "ebay_url" and "local_path".
    """
    try:
        if CACHE_JSON.exists():
            with open(CACHE_JSON, "r") as f:
                image_cache = json.load(f)
        else:
            image_cache = {}
    except json.JSONDecodeError:
        image_cache = {}

    image_cache[product_name] = {"ebay_url": image_url, "local_path": None}

    with open(CACHE_JSON, "w") as f:
        json.dump(image_cache, f, indent=4)
