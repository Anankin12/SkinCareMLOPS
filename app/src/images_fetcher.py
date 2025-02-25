from serpapi import GoogleSearch
from dotenv import load_dotenv
import os
import requests
load_dotenv()

class ImageFetcher:

    def __init__(self, product_name):
        self.product_name = product_name


    def google_search(self):
        # GOOGLE_SEARCH_API = os.getenv("GOOGLE_SEARCH_API")
        GOOGLE_SEARCH_API = '54df708ef0dba519ac244d5263ec6b378eeb74c220c53b44048863b6be2a421b'
        search = GoogleSearch(
            {
                "q": self.product_name + " skincare",
                "tbm": "isch",  # Image search
                "num": 1,
                "api_key": GOOGLE_SEARCH_API,
            }
        )
        results = search.get_dict()
        images = results.get("images_results", [])
        return images[0]["original"] if images else None
    
    def ebay_search(self): 

        # Prepare API request
        
        EBAY_APP_ID = os.getenv("EBAY_PROD_APP_ID")
        EBAY_API_URL = os.getenv("EBAY_PROD_API_URL")
        EBAY_AUTH_URL = os.getenv("EBAY_PROD_AUTH_URL")
        EBAY_ACCESS_TOKEN = os.getenv("EBAY_PROD_ACCESS_TOKEN")

        params = {
            "OPERATION-NAME": "findItemsByKeywords",
            "SERVICE-VERSION": "1.0.0",
            "SECURITY-APPNAME": EBAY_APP_ID,
            "RESPONSE-DATA-FORMAT": "JSON",
            "REST-PAYLOAD": "",
            "keywords": self.product_name,
            "paginationInput.entriesPerPage": 5,  # Get up to 5 results
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
            
                # Find the first valid image
            for item in items[:5]:  # Only check first 5 results
                image_url = item.get("galleryURL")
                if isinstance(image_url, list):
                    image_url = image_url[0]  # Take first image if multiple are returned

                if image_url and isinstance(image_url, str):
                    # ✅ Modify the URL to request a higher resolution image
                    if "s-l140" in image_url:  # If it's a small thumbnail
                        high_res_url = image_url.replace("s-l140", "s-l1200")  # Increase size to 500px
                    elif "s-l225" in image_url:
                        high_res_url = image_url.replace("s-l225", "s-l1200")
                    elif "s-l400" in image_url:
                        high_res_url = image_url.replace("s-l400", "s-l1200")
                    else:
                        high_res_url = image_url  # Fallback to the original URL

                    # ✅ Store both eBay URL and downloaded image
                    ext = high_res_url.split(".")[-1].lower()
                    if ext not in ["jpg", "jpeg", "png", "gif", "webp"]:
                        ext = "jpg"  # Default to jpg if unknown

            return None

        except requests.exceptions.RequestException as e:
            
            return None
