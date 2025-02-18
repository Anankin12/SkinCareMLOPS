# ebay_image_fetcher.py
import os
import requests
from dotenv import load_dotenv
from glob import glob  # Used to match cached images with any format

# Load API credentials from .env file
load_dotenv()

# === CONFIGURATION ===
USE_PRODUCTION = True  # Set to True for Production API, False for Sandbox API
VERBOSE = True  # Set to True to enable verbose output

# Select API environment based on USE_PRODUCTION
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

CACHE_DIR = CACHE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "cached_images"))
  # Directory for cached images

# Ensure cache directory exists
os.makedirs(CACHE_DIR, exist_ok=True)

def log(message):
    """ Prints verbose messages only if VERBOSE is enabled. """
    if VERBOSE:
        print(message)

def get_cached_image(product_name):
    """
    Check if an image exists in cache for a given product.
    Returns the file path if found, otherwise None.
    """
    safe_filename = product_name.replace(" ", "_").lower()
    matching_files = glob(os.path.join(CACHE_DIR, f"{safe_filename}.*"))  # Match any extension

    if matching_files:
        log(f"🖼️ Using cached image for '{product_name}': {matching_files[0]}")
        return matching_files[0]
    
    return None

def get_ebay_product_image(product_name):
    """
    Fetch product image from eBay API and cache it if found.
    Returns the image path if successful, otherwise None.
    """

    # Check if image is cached
    cached_image_path = get_cached_image(product_name)
    if cached_image_path:
        return cached_image_path

    log(f"🔍 Searching eBay for images of: {product_name}")

    # Prepare API request
    params = {
        "OPERATION-NAME": "findItemsByKeywords",
        "SERVICE-VERSION": "1.0.0",
        "SECURITY-APPNAME": EBAY_APP_ID,
        "RESPONSE-DATA-FORMAT": "JSON",
        "REST-PAYLOAD": "",
        "keywords": product_name,
        "paginationInput.entriesPerPage": 5,  # Get up to 5 results to find an image
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
            log(f"❌ No items found for '{product_name}'.")
            return None

        # Find the first valid image within the first 5 results
        for item in items[:5]:  # Only check first 5 results
            image_url = item.get("galleryURL")
            if isinstance(image_url, list):
                image_url = image_url[0]  # Take first image if multiple are returned
            
            if image_url and isinstance(image_url, str):
                # Determine file extension
                ext = image_url.split(".")[-1].lower()
                if ext not in ["jpg", "jpeg", "png", "gif", "webp"]:
                    ext = "jpg"  # Default to jpg if unknown
                
                save_path = os.path.join(CACHE_DIR, f"{product_name.replace(' ', '_').lower()}.{ext}")

                # Download and save image
                img_response = requests.get(image_url, stream=True)
                if img_response.status_code == 200:
                    with open(save_path, "wb") as img_file:
                        for chunk in img_response.iter_content(1024):
                            img_file.write(chunk)
                    log(f"✅ Found NEW image for '{product_name}', saved to: {save_path}")
                    return save_path

        log(f"❌ No valid images found for '{product_name}'.")
        return None

    except requests.exceptions.RequestException as e:
        log(f"🚨 eBay API request failed for '{product_name}': {e}")
        return None
