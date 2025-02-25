from fastapi import FastAPI
import requests
import os

# FastAPI App
app = FastAPI()

# API URL for fetching images
MAKEUP_API_URL = "http://makeup-api.herokuapp.com/api/v1/products.json"
PLACEHOLDER_IMAGE = os.path.join("src", "Placeholder_Image.jpg")

# Function to fetch image
def fetch_product_image(brand, name):
    try:
        response = requests.get(MAKEUP_API_URL)
        response.raise_for_status()
        products = response.json()
        
        matching_product = next(
            (p for p in products if p["brand"] and brand.lower() in p["brand"].lower() and name.lower() in p["name"].lower()), 
            None
        )

        return matching_product["image_link"] if matching_product else PLACEHOLDER_IMAGE
    except requests.exceptions.RequestException:
        return PLACEHOLDER_IMAGE  # Use placeholder if API fails

# API Endpoint to get image URL
@app.get("/get_image")
def get_image(brand: str, name: str):
    image_url = fetch_product_image(brand, name)
    return {"image_url": image_url}
