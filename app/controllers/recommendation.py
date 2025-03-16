"""
This module contains the Streamlit app for the recommendation page.
"""
# import os
# from pathlib import Path
import pandas as pd
import streamlit as st

from config import DATA_DIR

from src.inference import recommendation_engine
from src.image_fetching.fetcher import fetch_product_image
from src.buttons.back_home import back_home_action
from src.buttons.like import like_action
from src.buttons.dislike import dislike_action

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
        st.button("🔙 Back to Home", key="back_home", on_click=back_home_action)
        return

    if "current_index" not in st.session_state:
        st.session_state.current_index = 0

    index = st.session_state.current_index
    if index >= len(recommendations):
        st.success("🎉 You've seen all recommendations!")
        st.button("🔙 Back to Home", key="back_home", on_click=back_home_action)
        return


    row = recommendations.iloc[index]
    product_name = row["product_name"]

    image_url = fetch_product_image(product_name)

    st.subheader(product_name)
    st.write(f"**Brand:** {row['brand_name']}")
    st.write(f"💰 **Price:** {row['price_usd']}")

    if image_url:
        st.image(image_url, caption=product_name, use_container_width=False)
    else:
        st.warning("No image available.")

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
