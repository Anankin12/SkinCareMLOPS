"""
Configuration file for the app.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Determine production vs. testing/sandbox mode.
USE_PRODUCTION = os.getenv("USE_PRODUCTION", "True").lower() == "true"

if USE_PRODUCTION:
    EBAY_APP_ID = os.getenv("EBAY_PROD_APP_ID")
    EBAY_API_URL = os.getenv("EBAY_PROD_API_URL")
    EBAY_AUTH_URL = os.getenv("EBAY_PROD_AUTH_URL")
    EBAY_ACCESS_TOKEN = os.getenv("EBAY_PROD_ACCESS_TOKEN")
    GOOGLE_SEARCH_API_KEY = os.getenv("GOOGLE_SEARCH_API_KEY")
    GOOGLE_SEARCH_CSE_ID=os.getenv("GOOGLE_SEARCH_CSE_ID")
else:
    EBAY_APP_ID = os.getenv("EBAY_SANDBOX_APP_ID")
    EBAY_API_URL = os.getenv("EBAY_SANDBOX_API_URL")
    EBAY_AUTH_URL = os.getenv("EBAY_SANDBOX_AUTH_URL")
    EBAY_ACCESS_TOKEN = os.getenv("EBAY_SANDBOX_ACCESS_TOKEN")
    GOOGLE_SEARCH_API_KEY = os.getenv("GOOGLE_SEARCH_API_KEY")
    GOOGLE_SEARCH_CSE_ID=os.getenv("GOOGLE_SEARCH_CSE_ID")

# Optional: if using Google Custom Search, you’ll likely need a Search Engine ID.
GOOGLE_SEARCH_ENGINE_ID = os.getenv("GOOGLE_SEARCH_ENGINE_ID")

# Directories
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "data"
# This cache folder is for storing image_cache.json used in image fetching.
CACHE_DIR = BASE_DIR / "src" / "image_fetching" / "cached_images"
if not CACHE_DIR.exists():
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

CACHE_JSON = CACHE_DIR / "image_cache.json"

# Streamlit page configuration
PAGE_CONFIG = {
    "page_title": "SkinCare MLOPS",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
}
