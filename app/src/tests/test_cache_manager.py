import json
from pathlib import Path
from src.image_fetching.cache_manager import save_to_cache
from src.image_fetching.cache_checker import get_cached_image
from config import CACHE_DIR

CACHE_JSON = Path(CACHE_DIR) / "image_cache.json"

def test_save_to_cache():
    """Test saving an image to cache."""
    product_name = "Moisturizer"
    image_url = "http://example.com/moisturizer.jpg"

    save_to_cache(product_name, image_url)

    # Load cache file manually
    with open(CACHE_JSON, "r") as f:
        cache_data = json.load(f)

    assert product_name in cache_data
    assert cache_data[product_name]["image_url"] == image_url
