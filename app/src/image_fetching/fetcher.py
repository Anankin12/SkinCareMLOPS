from .cache_checker import get_cached_image
from .ebay_api import fetch_ebay_image
from .google_search import fetch_google_image
from .cache_manager import save_to_cache

def fetch_product_image(product_name: str) -> str:
    """
    Fetch product image by checking the cache first, then eBay, and finally Google.
    """
    print(f"🔍 Fetching image for: {product_name}")

    # 1️⃣ Check the cache first.
    cached_image = get_cached_image(product_name)
    if cached_image:
        print(f"📂 Found cached image: {cached_image}")
        return cached_image

    # 2️⃣ Try eBay.
    print("🔍 Searching eBay...")
    ebay_image = fetch_ebay_image(product_name)
    if ebay_image:
        print(f"🛒 Found eBay image: {ebay_image}")
        save_to_cache(product_name, ebay_image)
        return ebay_image

    print("🔍 Searching Google...")
    # 3️⃣ Try Google Custom Search.
    google_image = fetch_google_image(product_name)
    if google_image:
        print(f"🔍 Found Google image: {google_image}")
        save_to_cache(product_name, google_image)
        return google_image

    print("❌ No image found")
    return None
