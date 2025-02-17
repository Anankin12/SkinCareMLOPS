import sys
import os

# Add src/ directory to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ebay_image_fetcher import get_ebay_product_image

# Test fetching the cached image
product_name = "La Habana Eau de Parfum"
image_path = get_ebay_product_image(product_name)

print(f"Returned Image Path: {image_path}")
