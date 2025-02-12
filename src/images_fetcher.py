from serpapi import GoogleSearch  

def get_product_image(product_name):
    API_KEY = "54df708ef0dba519ac244d5263ec6b378eeb74c220c53b44048863b6be2a421b"  # Replace with your SerpAPI key
    search = GoogleSearch({
        "q": product_name + " skincare",
        "tbm": "isch",  # Image search
        "num": 1,
        "api_key": API_KEY
    })
    results = search.get_dict()
    images = results.get("images_results", [])
    return images[0]["original"] if images else None
