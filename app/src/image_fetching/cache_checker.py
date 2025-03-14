import json
import os
from config import CACHE_DIR

CACHE_JSON = os.path.join(CACHE_DIR, "image_cache.json")

# Ensure CACHE_DIR exists
os.makedirs(CACHE_DIR, exist_ok=True)

if os.path.exists(CACHE_JSON):
    with open(CACHE_JSON, "r") as f:
        image_cache = json.load(f)
else:
    image_cache = {}

def get_cached_image(product_name):
    """Return the cached image URL if available."""
    return image_cache.get(product_name, {}).get("image_url", None)
