from serpapi import GoogleSearch
from config import GOOGLE_SEARCH_API_KEY

def fetch_google_image(product_name):
    """
    Fetch an image from Google Search if eBay fails.
    """
    search = GoogleSearch({
        "q": f"{product_name} skincare",
        "tbm": "isch",  # Image search
        "num": 1,
        "api_key": GOOGLE_SEARCH_API_KEY,
    })

    results = search.get_dict()
    images = results.get("images_results", [])

    return images[0]["original"] if images else None
