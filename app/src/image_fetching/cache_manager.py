import json
from config import CACHE_DIR

CACHE_JSON = CACHE_DIR / "image_cache.json"

def save_to_cache(product_name, image_url):
    """
    Save the image URL to the cache file.
    """
    try:
        with open(CACHE_JSON, "r") as f:
            image_cache = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        image_cache = {}

    image_cache[product_name] = {"image_url": image_url}

    with open(CACHE_JSON, "w") as f:
        json.dump(image_cache, f, indent=4)
