import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

# === CONFIGURATION ===
USE_PRODUCTION = True  # Set to True for Production API, False for Sandbox API

if USE_PRODUCTION:
    EBAY_APP_ID = os.getenv("EBAY_PROD_APP_ID")
    EBAY_API_URL = os.getenv("EBAY_PROD_API_URL")
    EBAY_AUTH_URL = os.getenv("EBAY_PROD_AUTH_URL")
    EBAY_ACCESS_TOKEN = os.getenv("EBAY_PROD_ACCESS_TOKEN")
else:
    EBAY_APP_ID = os.getenv("EBAY_SANDBOX_APP_ID")
    EBAY_API_URL = os.getenv("EBAY_SANDBOX_API_URL")
    EBAY_AUTH_URL = os.getenv("EBAY_SANDBOX_AUTH_URL")
    EBAY_ACCESS_TOKEN = os.getenv("EBAY_SANDBOX_ACCESS_TOKEN")

# Use a consistent absolute path for the cache JSON
CACHE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "cached_images"))
CACHE_JSON = os.path.join(CACHE_DIR, "image_cache.json")

os.makedirs(CACHE_DIR, exist_ok=True)

if os.path.exists(CACHE_JSON):
    with open(CACHE_JSON, "r") as f:
        image_cache = json.load(f)
else:
    image_cache = {}

def save_cache():
    with open(CACHE_JSON, "w") as f:
        json.dump(image_cache, f, indent=4)

def get_cached_image(product_name):
    """Return the cached eBay image URL if available."""
    if product_name in image_cache:
        return image_cache[product_name]["ebay_url"]
    return None

def get_ebay_product_image(product_name):
    """
    Query eBay for the product image.
    Instead of downloading the image file, update the cache with the image URL only.
    """
    # Check cache first
    cached_image_url = get_cached_image(product_name)
    if cached_image_url:
        return cached_image_url

    # Prepare API request
    params = {
        "OPERATION-NAME": "findItemsByKeywords",
        "SERVICE-VERSION": "1.0.0",
        "SECURITY-APPNAME": EBAY_APP_ID,
        "RESPONSE-DATA-FORMAT": "JSON",
        "REST-PAYLOAD": "",
        "keywords": product_name,
        "paginationInput.entriesPerPage": 5,
        "outputSelector": "PictureURLLarge"
    }

    headers = {
        "Authorization": f"Bearer {EBAY_ACCESS_TOKEN}",
        "X-EBAY-SOA-OPERATION-NAME": "findItemsByKeywords",
        "X-EBAY-SOA-SECURITY-APPNAME": EBAY_APP_ID,
        "X-EBAY-SOA-RESPONSE-DATA-FORMAT": "JSON",
        "Accept": "application/json",
    }

    try:
        response = requests.get(EBAY_API_URL, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()

        items = data.get("findItemsByKeywordsResponse", [])[0].get("searchResult", [])[0].get("item", [])

        if not items:
            return None

        # Process the first valid image URL
        for item in items[:5]:
            image_url = item.get("galleryURL")
            if isinstance(image_url, list):
                image_url = image_url[0]

            if image_url and isinstance(image_url, str):
                # Modify the URL for higher resolution
                if "s-l140" in image_url:
                    high_res_url = image_url.replace("s-l140", "s-l1200")
                elif "s-l225" in image_url:
                    high_res_url = image_url.replace("s-l225", "s-l1200")
                elif "s-l400" in image_url:
                    high_res_url = image_url.replace("s-l400", "s-l1200")
                else:
                    high_res_url = image_url

                # Instead of saving the image locally, update the cache with the URL only.
                image_cache[product_name] = {
                    "ebay_url": high_res_url,
                    "local_path": None
                }
                save_cache()
                return high_res_url

        return None

    except requests.exceptions.RequestException:
        return None
