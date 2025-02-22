from pathlib import Path

import pandas as pd
import streamlit as st
from src.inference import recommendation_engine
from src.images_fetcher import ImageFetcher


@st.cache_data
def load_data():
    csv_path = (
        Path(__file__).resolve().parent.parent
        / "data"
        / "processed"
        / "cleaned_data.csv"
    )
    return pd.read_csv(csv_path, sep=";")


def recommendation_page():
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
    recommendations = recommender.recommendation_function(selected_category, 
                                                         component,
                                                         skin_tone,
                                                         skin_type, 
                                                         n_recommendations=num_recommendations)
    
    st.info(f"**Your Skin Type:** {skin_type}")
    st.info(f"**Preferred Component:** {component}")
    st.info(f"🔢 **Displaying {num_recommendations} recommendations.**")

    if recommendations.empty:
        st.warning("No matching products found.")
        return

    # ✅ Track current product index
    if "current_index" not in st.session_state:
        st.session_state.current_index = 0

    # ✅ Get current product
    index = st.session_state.current_index
    if index >= len(recommendations):
        st.success("🎉 You've seen all recommendations!")
        return

    row = recommendations.iloc[index]
    product_name = row["product_name"]
    image_fetcher = ImageFetcher(product_name)
    image = image_fetcher.google_search()

    st.subheader(product_name)
    st.write(f"**Brand:** {row['brand_name']}")
    st.write(f"💰 **Price:** {row['price_usd']}")

    if image:
        st.image(image, caption=product_name, use_container_width=True)
    else:
        st.warning("No image available.")

    # ✅ Centered "Like" and "Dislike" Buttons
    col1, col2, col3 = st.columns([1, 2, 1])  # Add spacing columns
    with col2:  # Center the buttons
        colA, colB = st.columns(2)  # Create two equal columns inside the center column
        with colA:
            if st.button("👍 Like", key="like"):
                st.session_state.current_index += 1
                st.rerun()
        with colB:
            if st.button("👎 Dislike", key="dislike"):
                st.session_state.current_index += 1
                st.rerun()

    # ✅ Add a "Back to Home" Button
    if st.button("🔙 Back to Home"):
        st.session_state.page = "home"
        st.rerun()


if __name__ == "__main__":
    recommendation_page()
