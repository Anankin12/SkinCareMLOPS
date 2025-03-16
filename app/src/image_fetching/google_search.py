"""
This module contains a function to fetch an image of a product 
from Google Custom Search API.
"""

import requests
from config import GOOGLE_SEARCH_API_KEY, GOOGLE_SEARCH_CSE_ID

def fetch_google_image(product_name: str) -> str:
    """
    Query Google Custom Search API for an image of the product.
    """
    search_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": product_name,
        "cx": GOOGLE_SEARCH_CSE_ID,
        "key": GOOGLE_SEARCH_API_KEY,
        "searchType": "image",
        "num": 1,
    }
    try:
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        results = response.json().get("items", [])
        if results:
            return results[0].get("link")
        return None
    except requests.RequestException:
        return None
