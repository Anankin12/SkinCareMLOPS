import requests
from config import EBAY_APP_ID, EBAY_API_URL, EBAY_ACCESS_TOKEN

HEADERS = {
    "Authorization": f"Bearer {EBAY_ACCESS_TOKEN}",
    "Accept": "application/json",
}

def fetch_ebay_image(product_name):
    """
    Query eBay for the product image.
    """
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

    try:
        response = requests.get(EBAY_API_URL, params=params, headers=HEADERS)
        response.raise_for_status()
        data = response.json()

        items = data.get("findItemsByKeywordsResponse", [])[0].get("searchResult", [])[0].get("item", [])

        if not items:
            return None

        for item in items:
            image_url = item.get("galleryURL")
            if image_url:
                return image_url.replace("s-l140", "s-l1200")  # High-resolution image

    except requests.exceptions.RequestException:
        return None

    return None
