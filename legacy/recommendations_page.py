import streamlit as st
import requests
import os
import pandas as pd

# Load brands from CSV
DATA_PATH = os.path.join("notebooks", "clean_cosmetics_data.csv")
df = pd.read_csv(DATA_PATH)
valid_brands = sorted(df["Brand"].unique().tolist())  # Sorted for better UI

# API URLs
RECOMMEND_API = "http://localhost:8000/recommend"
IMAGE_API = "http://localhost:8001/get_image"

# Placeholder image
PLACEHOLDER_IMAGE = os.path.join("src", "Placeholder_Image.jpg")

# Streamlit UI
st.title("Skincare Product Recommendation System")

st.sidebar.header("Input Parameters")

# User Inputs
skin_type = st.sidebar.selectbox("Select Skin Type", ["Dry", "Oily", "Combination", "Normal"])
label_filter = st.sidebar.selectbox("Select Product Type", ["All", "Moisturizer", "Face Mask", "Serum"])
brand_filter = st.sidebar.selectbox("Select Brand", ["All"] + valid_brands)
price_range = st.sidebar.slider("Select Price Range", min_value=10, max_value=300, value=(10, 100))
rank_filter = st.sidebar.slider("Select Rank Range", min_value=0.0, max_value=5.0, value=(4.0, 5.0))
ingredient_input = st.sidebar.text_input("Enter a Key Ingredient (Optional)")

if st.sidebar.button("Get Recommendation"):
    payload = {
        "skin_type": skin_type,
        "label_filter": label_filter,
        "rank_filter": rank_filter,
        "brand_filter": brand_filter,
        "price_range": price_range,
        "ingredient_input": ingredient_input,
        "num_recommendations": 5
    }

    response = requests.post(RECOMMEND_API, json=payload)
    
    if response.status_code == 200:
        results = response.json()["recommendations"]
        
        # Display recommended products
        st.write("### Recommended Products")
        
        for product in results:
            name = product["Name"]
            brand = product["Brand"]
            price = product["Price"]
            rank = product["Rank"]

            # Fetch image separately
            image_response = requests.get(IMAGE_API, params={"brand": brand, "name": name})
            if image_response.status_code == 200:
                image_url = image_response.json()["image_url"]
            else:
                image_url = PLACEHOLDER_IMAGE

            # Display as a card-like format
            col1, col2 = st.columns([1, 3])
            with col1:
                st.image(image_url, width=150)
            with col2:
                st.write(f"**{name}**  \nBrand: {brand}  \nPrice: ${price}  \n⭐ Rank: {rank}")

    else:
        st.error("Error fetching recommendations. Please try again.")
