import os
import pandas as pd
import requests
from dotenv import load_dotenv
from glob import glob  # Used to find files with any extension

# Load API credentials from .env file
load_dotenv()

EBAY_APP_ID = os.getenv("EBAY_APP_ID")
EBAY_API_URL = "https://svcs.sandbox.ebay.com/services/search/FindingService/v1"

PRODUCT_CSV_PATH = os.path.join("..", "data", "raw", "product_info.csv")
CACHE_DIR = os.path.join("cached_images")  # Directory to store images
PLACEHOLDER_IMAGE = os.path.join("src", "Placeholder_Image.jpg")

# Ensure cache directory exists
os.makedirs(CACHE_DIR, exist_ok=True)

def get_cached_image(product_name):
    """
    Check if an image exists for the product in any format (jpg, png, etc.).
    Returns the file path if found, otherwise None.
    """
    safe_filename = product_name.replace(" ", "_").lower()
    matching_files = glob(os.path.join(CACHE_DIR, f"{safe_filename}.*"))  # Match any extension

    return matching_files[0] if matching_files else None

def get_ebay_product_image(product_name):
    """
    Fetch product image from eBay API and cache it if found.
    """

    # Check if the image is already cached (any format)
    cached_image_path = get_cached_image(product_name)
    if cached_image_path:
        print(f"Using cached image: {cached_image_path}")
        return cached_image_path

    # If not cached, proceed to API request
    params = {
        "OPERATION-NAME": "findItemsByKeywords",
        "SERVICE-VERSION": "1.0.0",
        "SECURITY-APPNAME": EBAY_APP_ID,
        "RESPONSE-DATA-FORMAT": "JSON",
        "REST-PAYLOAD": "",
        "keywords": product_name,
        "paginationInput.entriesPerPage": 1,
        "outputSelector": "PictureURLLarge"
    }

    headers = {
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
        
        if items:
            image_url = items[0].get("galleryURL", None)
            if image_url:
                # Determine the image extension from the URL
                ext = image_url.split(".")[-1].lower()
                if ext not in ["jpg", "jpeg", "png", "gif", "webp"]:  # Default to jpg if unknown
                    ext = "jpg"

                save_path = os.path.join(CACHE_DIR, f"{product_name.replace(' ', '_').lower()}.{ext}")

                # Download and save the image
                img_response = requests.get(image_url, stream=True)
                if img_response.status_code == 200:
                    with open(save_path, "wb") as img_file:
                        for chunk in img_response.iter_content(1024):
                            img_file.write(chunk)
                    print(f"Saved image: {save_path}")
                    return save_path

        # If no image found, return the placeholder image (but do not cache it)
        print(f"No image found for '{product_name}'. Returning placeholder.")
        return PLACEHOLDER_IMAGE

    except requests.exceptions.RequestException as e:
        print(f"eBay API request failed: {e}")
        return PLACEHOLDER_IMAGE


if __name__ == "__main__":
    try:
        # Load product_info.csv
        product_df = pd.read_csv(PRODUCT_CSV_PATH)

        # Debug: Print column names
        print("Available columns in CSV:", product_df.columns)

        # Debug: Print first few rows
        print("First few rows:\n", product_df.head())

        # Ensure correct column name
        correct_col_name = None
        for col in product_df.columns:
            if "name" in col.lower():  # Case-insensitive match
                correct_col_name = col
                break

        if correct_col_name is None:
            raise ValueError("Could not find a column containing 'name' in product_info.csv.")

        test_product = product_df.iloc[1][correct_col_name]
        print(f"Testing with product: {test_product}")

        image_path = get_ebay_product_image(test_product)
        print(f"Image Path: {image_path}")

    except FileNotFoundError:
        print(f"Error: Could not find the file at {PRODUCT_CSV_PATH}. Check the path and try again.")

    except ValueError as ve:
        print(f"Error: {ve}")
