import os
from pathlib import Path
import pandas as pd
import streamlit as st
from src.image_fetching.fetcher import fetch_product_image

# Adjust these if you move them out of `src/`:
from config import DATA_DIR, CACHE_DIR
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
    csv_path = DATA_DIR / "processed" / "cleaned_data.csv"
    return pd.read_csv(csv_path, sep=";")

def recommendation_page():
    """
    Recommendation page for the web app: it displays the user's
    skincare recommendations based on their preferences.
    """
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
        st.info("Please go back and select your preferences.")
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

    if "current_index" not in st.session_state:
        st.session_state.current_index = 0

    index = st.session_state.current_index
    if index >= len(recommendations):
        st.success("🎉 You've seen all recommendations!")
        return

    row = recommendations.iloc[index]
    product_name = row["product_name"]

    os.makedirs(CACHE_DIR, exist_ok=True)

    # --- Image fetching logic ---
    image_url = get_cached_image(product_name)
    if not image_url:
        image_url = get_ebay_product_image(product_name)
    if not image_url:
        image_fetcher = ImageFetcher(product_name)
        image_url = image_fetcher.google_search()
        if image_url:
            image_cache[product_name] = {"ebay_url": image_url, "local_path": None}
            save_cache()

    st.subheader(product_name)
    st.write(f"**Brand:** {row['brand_name']}")
    st.write(f"💰 **Price:** {row['price_usd']}")

    if image_url:
        st.image(image_url, caption=product_name, use_container_width=True)
    else:
        st.warning("No image available.")

    # Define callback functions that only update state and set a flag.
    def like_action():
        st.session_state.current_index += 1
        st.session_state.do_rerun = True

    def dislike_action():
        st.session_state.current_index += 1
        st.session_state.do_rerun = True

    def back_home_action():
        st.session_state.page = "homepage"
        st.session_state.do_rerun = True

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        col_a, col_b = st.columns(2)
        col_a.button("👍 Like", key="like", on_click=like_action)
        col_b.button("👎 Dislike", key="dislike", on_click=dislike_action)

    st.button("🔙 Back to Home", key="back_home", on_click=back_home_action)


# Outside of any callbacks, check for a rerun flag.
if st.session_state.get("do_rerun", False):
    del st.session_state["do_rerun"]
    st.rerun()
