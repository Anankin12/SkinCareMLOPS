from pathlib import Path

import pandas as pd
import streamlit as st

from src.images_fetcher import get_product_image
from src.inference import recommendation


@st.cache_data
def load_data():
    csv_path = (
        Path(__file__).resolve().parent.parent
        / "data"
        / "processed"
        / "clean_cosmetics_data.csv"
    )
    return pd.read_csv(csv_path)


def recommendation_page():
    st.set_page_config(page_title="Recommendations")

    st.markdown(
        "<h2 style='text-align: center;'>Your Skincare Recommendations</h2>",
        unsafe_allow_html=True,
    )

    skin_type = st.session_state.get("selected_skin_type", None)
    component = st.session_state.get("selected_component", None)
    num_recommendations = st.session_state.get("num_recommendations", 5)

    if not skin_type or not component:
        st.warning("Please go back and select your preferences.")
        return

    df = load_data()
    filtered_df = recommendation(df, skin_type, component, num_recommendations)

    st.info(f"**Your Skin Type:** {skin_type}")
    st.info(f"**Preferred Component:** {component}")
    st.info(f"🔢 **Displaying {num_recommendations} recommendations.**")

    if filtered_df.empty:
        st.warning("No matching products found.")
        return

    # ✅ Track current product index
    if "current_index" not in st.session_state:
        st.session_state.current_index = 0

    # ✅ Get current product
    index = st.session_state.current_index
    if index >= len(filtered_df):
        st.success("🎉 You've seen all recommendations!")
        return

    row = filtered_df.iloc[index]
    product_name = row["Name"]
    image = get_product_image(product_name)

    st.subheader(product_name)
    st.write(f"**Brand:** {row['Brand']}")
    st.write(f"💰 **Price:** {row['Price']}")

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
