"""
Configuration settings for the SkinCareMLOPS application.
"""

import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from the .env file.
load_dotenv()

# Basic Settings
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Directories
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "data"
CACHE_DIR = BASE_DIR / "src" / "image_fetching" / "cached_images"

# Streamlit Page Configuration
PAGE_CONFIG = {
    "page_title": "SkinCare MLOPS",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
}

# Determine environment mode
USE_PRODUCTION = os.getenv("USE_PRODUCTION", "True").lower() == "true"

# External API Keys (loaded from .env)
if USE_PRODUCTION:
    EBAY_APP_ID = os.getenv("EBAY_PROD_APP_ID")
    EBAY_API_URL = os.getenv("EBAY_PROD_API_URL")
    EBAY_AUTH_URL = os.getenv("EBAY_PROD_AUTH_URL")
    EBAY_ACCESS_TOKEN = os.getenv("EBAY_PROD_ACCESS_TOKEN")
    GOOGLE_SEARCH_API_KEY = os.getenv("GOOGLE_SEARCH_API_KEY")
else:
    EBAY_APP_ID = os.getenv("EBAY_SANDBOX_APP_ID")
    EBAY_API_URL = os.getenv("EBAY_SANDBOX_API_URL")
    EBAY_AUTH_URL = os.getenv("EBAY_SANDBOX_AUTH_URL")
    EBAY_ACCESS_TOKEN = os.getenv("EBAY_SANDBOX_ACCESS_TOKEN")
    GOOGLE_SEARCH_API_KEY = os.getenv("GOOGLE_SEARCH_API_KEY")
