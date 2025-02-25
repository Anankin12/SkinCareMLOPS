"""
This module contains the Streamlit recommendation page.
It makes use of the recommendation engine to provide
personalized skincare product recommendations based on
the user's preferences.
"""

from pathlib import Path
import os
import pandas as pd
import streamlit as st

from src.inference import recommendation_engine
from src.images_fetcher import ImageFetcher
from src.ebay_image_fetcher import (
    get_cached_image,
    get_ebay_product_image,
    image_cache,
    save_cache,
)

CACHE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "cached_images"))


@st.cache_data
def load_data():
    """
    Load the cleaned data from the CSV file.
    """
    csv_path = (
        Path(__file__).resolve().parent.parent
        / "data"
        / "processed"
        / "cleaned_data.csv"
    )
    return pd.read_csv(csv_path, sep=";")


def recommendation_page():
    """
    Recommendation page for the web app: it displays the user's
    skincare recommendations based on their preferences.
    """
    st.set_page_config(page_title="Recommendations")

    st.markdown(
        "<h2 style='text-align: center;'>Your Skincare Recommendations</h2>",
        unsafe_allow_html=True,
    )

    skin_type = st.session_state.get("selected_skin_type", None)
    component = st.session_state.get("selected_component", None)
    num_recommendations = st.session_state.get("num_recommendations", 5)
    selected_category = st.session_state.get("selected_category", None)
    skin_tone = st.session_state.get("selected_skin_tone", None)

    if not component or not selected_category:
        st.warning("Please go back and select your preferences.")
        return

    clean_df = load_data()
    recommender = recommendation_engine(clean_df)
    recommendations = recommender.recommendation_function(
        selected_category,
        component,
        skin_tone,
        skin_type,
        n_recommendations=num_recommendations,
    )

    st.info(f"**Your Skin Type:** {skin_type}")
    st.info(f"**Preferred Component:** {component}")
    st.info(f"🔢 **Displaying {num_recommendations} recommendations.**")

    if recommendations.empty:
        st.warning("No matching products found.")
        return

    # Track current product index
    if "current_index" not in st.session_state:
        st.session_state.current_index = 0

    # Get current product
    index = st.session_state.current_index
    if index >= len(recommendations):
        st.success("🎉 You've seen all recommendations!")
        return

    row = recommendations.iloc[index]
    product_name = row["product_name"]

    os.makedirs(CACHE_DIR, exist_ok=True)

    # --- Image fetching logic ---
    # 1. Try fetching from cache
    image_url = get_cached_image(product_name)
    # 2. If not cached, try fetching from eBay (which also caches if found)
    if not image_url:
        image_url = get_ebay_product_image(product_name)
    # 3. If still not found, fall back to Google Images
    # and then cache that result
    if not image_url:
        image_fetcher = ImageFetcher(product_name)
        image_url = image_fetcher.google_search()
        if image_url:
            image_cache[product_name] = {
                "ebay_url": image_url,
                "local_path": None,
            }
            save_cache()

    st.subheader(product_name)
    st.write(f"**Brand:** {row['brand_name']}")
    st.write(f"💰 **Price:** {row['price_usd']}")

    if image_url:
        st.image(image_url, caption=product_name, use_container_width=True)
    else:
        st.warning("No image available.")

    # Centered "Like" and "Dislike" Buttons
    col1, col2, col3 = st.columns([1, 2, 1])  # Add spacing columns
    with col2:  # Center the buttons
        col_a, col_b = st.columns(2)  # Create two equal columns inside
        # the center column
        with col_a:
            if st.button("👍 Like", key="like"):
                st.session_state.current_index += 1
                st.rerun()
        with col_b:
            if st.button("👎 Dislike", key="dislike"):
                st.session_state.current_index += 1
                st.rerun()

    # Add a "Back to Home" Button
    if st.button("🔙 Back to Home"):
        st.session_state.page = "home"
        st.rerun()


if __name__ == "__main__":
    recommendation_page()
