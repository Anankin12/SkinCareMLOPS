import streamlit as st 
import pandas as pd
from src.inference import recommendation
from src.ebay_image_fetcher import log, get_cached_image, get_ebay_product_image
from pathlib import Path

VERBOSE = True

@st.cache_data
def load_data():
    csv_path = Path(__file__).resolve().parent.parent / "data" / "processed" / "clean_cosmetics_data.csv"
    return pd.read_csv(csv_path)


def recommendation_page():
    st.set_page_config(page_title="Recommendations")

    st.markdown("<h2 style='text-align: center;'>Your Skincare Recommendations</h2>", unsafe_allow_html=True)

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

    st.subheader(product_name)
    st.write(f"**Brand:** {row['Brand']}")
    st.write(f"💰 **Price:** {row['Price']}")

    # ✅ Debugging: Print product name
    log(f"🔍 Looking for image: {product_name}")

    # ✅ First, try fetching cached eBay image URL
    image_url = get_cached_image(product_name)

    # ✅ If not cached, query eBay and update the cache
    if not image_url:
        image_url = get_ebay_product_image(product_name)

    # ✅ Debugging: Print image URL
    log(f"📸 Image URL: {image_url}")

    # ✅ Display the image if found
    if image_url:
        st.image(image_url, caption=product_name, use_container_width=False)
    else:
        st.warning(f"⚠️ No image found for this product: {product_name}")

    # ✅ "Like" and "Dislike" Buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("👍 Like", key=f"like_{index}"):
            st.session_state.current_index += 1
            st.rerun()
    with col2:
        if st.button("👎 Dislike", key=f"dislike_{index}"):
            st.session_state.current_index += 1
            st.rerun()

    # ✅ Add a "Back to Home" Button
    if st.button("🔙 Back to Home"):
        st.session_state.page = "home"
        st.rerun()


if __name__ == "__main__":
    recommendation_page()
