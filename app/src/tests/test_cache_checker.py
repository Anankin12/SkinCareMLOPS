import pytest
import json
from pathlib import Path
from src.image_fetching.cache_checker import get_cached_image
from src.image_fetching.cache_manager import save_to_cache
from config import CACHE_DIR

CACHE_JSON = Path(CACHE_DIR) / "image_cache.json"

def test_get_cached_image():
    """Test retrieving an image from the cache."""
    product_name = "Test Product"
    test_url = "http://example.com/test.jpg"

    # Save image to cache
    save_to_cache(product_name, test_url)

    # Fetch from cache
    assert get_cached_image(product_name) == test_url

def test_get_cached_image_missing():
    """Test retrieving an image that is not in cache."""
    assert get_cached_image("Nonexistent Product") is None
