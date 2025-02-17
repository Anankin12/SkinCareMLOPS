import sys
import os
import pandas as pd

# Ensure Python finds `ebay_image_fetcher.py`
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ebay_image_fetcher import get_ebay_product_image

# === CONFIGURATION ===
PRODUCT_CSV_PATH = os.path.join("..", "data", "raw", "product_info.csv")
VERBOSE = True  # Set to True for detailed output

def log(message):
    """ Prints verbose messages only if VERBOSE is enabled. """
    if VERBOSE:
        print(message)

try:
    log("🔄 Loading product_info.csv...")
    product_df = pd.read_csv(PRODUCT_CSV_PATH)

    # Ensure correct column name
    correct_col_name = None
    for col in product_df.columns:
        if "name" in col.lower():
            correct_col_name = col
            break

    if correct_col_name is None:
        raise ValueError("❌ Could not find a column containing 'name' in product_info.csv.")

    log(f"✅ Found product name column: {correct_col_name}")

    # Test the first 5 products
    for idx in range(min(5, len(product_df))):
        product_name = product_df.iloc[idx][correct_col_name]
        log(f"\n🔍 Testing with product: {product_name}")

        image_path = get_ebay_product_image(product_name)
        log(f"📸 Image Path: {image_path}")

    log("✅ Testing complete.")

except FileNotFoundError:
    print(f"❌ Error: Could not find the file at {PRODUCT_CSV_PATH}. Check the path and try again.")

except ValueError as ve:
    print(f"❌ Error: {ve}")

except Exception as e:
    print(f"🚨 Unexpected error occurred: {e}")
