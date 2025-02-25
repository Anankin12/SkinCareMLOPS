from src.image_fetching.cache_checker import get_cached_image
from src.image_fetching.ebay_api import fetch_ebay_image
from src.image_fetching.google_search import fetch_google_image
from src.image_fetching.cache_manager import save_to_cache

def fetch_product_image(product_name):
    """
    Fetch product image, checking cache first, then eBay, then Google.
    """
    # 1️⃣ Check cache first
    cached_image = get_cached_image(product_name)
    if cached_image:
        return cached_image

    # 2️⃣ Try eBay
    ebay_image = fetch_ebay_image(product_name)
    if ebay_image:
        save_to_cache(product_name, ebay_image)
        return ebay_image

    # 3️⃣ Try Google if eBay fails
    google_image = fetch_google_image(product_name)
    if google_image:
        save_to_cache(product_name, google_image)
        return google_image

    # 4️⃣ Return None if no image is found
    return None
