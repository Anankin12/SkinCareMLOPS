"""
Module to check the cache for a given product name.
"""
import json
from config import CACHE_JSON


def get_cached_image(product_name: str) -> str:
    """
    Return the cached image URL for the given product if available.
    Uses the key "ebay_url" from the cache structure.
    """
    if not CACHE_JSON.exists():
        return None
    try:
        with open(CACHE_JSON, "r", encoding="utf-8") as f:
            image_cache = json.load(f)
    except json.JSONDecodeError:
        image_cache = {}

    product_entry = image_cache.get(product_name, {})
    return product_entry.get("ebay_url")
