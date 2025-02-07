import requests
import json

# Base URL for the Makeup API
MAKEUP_API_URL = "https://makeup-api.herokuapp.com/api/v1/products.json"

# Example request: Fetch products by brand
def fetch_products_by_brand(brand):
    params = {"brand": brand}
    response = requests.get(MAKEUP_API_URL, params=params)

    if response.status_code == 200:
        products = response.json()
        return products
    else:
        print(f"Error: {response.status_code}")
        return None

# Example usage
brand_name = "maybelline"  # Change this to any brand available in the API
products = fetch_products_by_brand(brand_name)

# Display sample product data
if products:
    print(f"Found {len(products)} products for brand '{brand_name}':")
    for product in products[:5]:  # Print first 5 products for testing
        print(f"Name: {product['name']}, Price: ${product['price']}, Image URL: {product.get('image_link', 'No Image')}")
else:
    print("No products found or error in API request.")
