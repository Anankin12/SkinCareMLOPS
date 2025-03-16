import requests
from config import EBAY_APP_ID, EBAY_API_URL, EBAY_ACCESS_TOKEN

def fetch_ebay_image(product_name: str) -> str:
    """
    Query eBay for a product image and return a high-resolution image URL if found.
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
                # Replace parts of the URL for higher resolution if needed.
                if "s-l140" in image_url:
                    high_res_url = image_url.replace("s-l140", "s-l1200")
                elif "s-l225" in image_url:
                    high_res_url = image_url.replace("s-l225", "s-l1200")
                elif "s-l400" in image_url:
                    high_res_url = image_url.replace("s-l400", "s-l1200")
                else:
                    high_res_url = image_url
                return high_res_url
        return None
    except requests.RequestException:
        return None
