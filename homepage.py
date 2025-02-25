import streamlit as st


def homepage():
    """
    Homepage for the web app: it takes in user input for product category,
    principal component, skin type, and skin tone (saved in session state).
    Then, it asks for hair and eye color before switching to the
    recommendation page.
    """
    st.set_page_config(page_title="Find Your Skincare Product", layout="wide")

    st.markdown(
        """
        <style>
        div.stButton > button {
            width: 100%;
            height: 60px;
            font-size: 18px;
            border-radius: 10px;
            border: 2px solid #ddd;
        }
        </style>
    """,
        unsafe_allow_html=True,
    )

    # **Step 1: Select Product Category**
    st.markdown("### Select Product Category")
    categories = {"Cosmetics": "💄 Cosmetics",
                  "Eye Care": "👁 Eye Care",
                  "Random": "🎁 Random"}

    if "selected_category" not in st.session_state:
        st.session_state.selected_category = None

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button(categories["Cosmetics"], key="cosmetics"):
            st.session_state.selected_category = "Cosmetics"
    with col2:
        if st.button(categories["Eye Care"], key="eye_care"):
            st.session_state.selected_category = "Eye Care"
    with col3:
        if st.button(categories["Random"], key="random"):
            st.session_state.selected_category = "Random"

    if not st.session_state.selected_category:
        st.stop()  # Wait until category is selected

    # **Step 2: Select Principal Component**
    st.markdown("### Select Principal Component")

    if "selected_component" not in st.session_state:
        st.session_state.selected_component = None

    col1, col2 = st.columns(2)
    with col1:
        if st.button("💦 Water Based", key="water"):
            st.session_state.selected_component = "Water"
    with col2:
        if st.button("🧊 Silicone Based", key="silicone"):
            st.session_state.selected_component = "Silicone"

    if not st.session_state.selected_component:
        st.stop()  # Wait until component is selected

    # **Step 3: Select Skin Type**
    st.markdown("### Select Skin Type")

    skin_types = {
        "Dry": "🧴 Dry",
        "Normal": "💧 Normal",
        "Oily": "🌿 Oily",
        "Combination": "🌸 Combination",
    }

    if "selected_skin_type" not in st.session_state:
        st.session_state.selected_skin_type = None

    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)

    with col1:
        if st.button(skin_types["Dry"], key="dry"):
            st.session_state.selected_skin_type = "Dry"
    with col2:
        if st.button(skin_types["Normal"], key="normal"):
            st.session_state.selected_skin_type = "Normal"
    with col3:
        if st.button(skin_types["Oily"], key="oily"):
            st.session_state.selected_skin_type = "Oily"
    with col4:
        if st.button(skin_types["Combination"], key="combination"):
            st.session_state.selected_skin_type = "Combination"

    if not st.session_state.selected_skin_type:
        st.stop()  # Wait until skin type is selected

    # **Step 4: Select Skin Tone**
    st.markdown("### Select Skin Tone")

    skin_tones = ["Light", "Fair", "Unknown", "Tan", "Light Medium"]

    if "selected_skin_tone" not in st.session_state:
        st.session_state.selected_skin_tone = None

    selected_tone = st.radio("Choose your skin tone:", skin_tones,
                             horizontal=True)
    st.session_state.selected_skin_tone = selected_tone

    # # **Step 5: Select Hair Color**
    # st.markdown("### Select Hair Color")

    # hair_colors = ["Dark", "Light", "Red"]
    # selected_hair_color = st.radio("Choose your hair color:",
    #                                hair_colors, horizontal=True)

    # **Step 6: Select Eye Color**
    st.markdown("### Select Eye Color")

    # eye_colors = ["Light", "Dark"]
    # selected_eye_color = st.radio("Choose your eye color:", eye_colors,
    #                               horizontal=True)

    # **Step 7: Number of Recommendations**
    st.markdown("### Number of Recommendations")
    st.session_state.num_recommendations = st.slider(
        "Select how many recommendations you want:", 1, 10, 5
        )

    # **Step 8: Show Final Selection & Proceed**
    # Switch to recommendation page
    if st.button("Get Recommendations", key="recommend"):
        st.switch_page("pages/recommendation.py")


# Main execution
if __name__ == "__main__":
    homepage()
