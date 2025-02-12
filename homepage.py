import streamlit as st


def homepage():
    st.set_page_config(page_title="Find Your Skincare Product", layout="wide")

    st.markdown("""
        <style>
        div.stButton > button {
            width: 100%;
            height: 60px;
            font-size: 18px;
            border-radius: 10px;
            border: 2px solid #ddd;
        }
        .selected {
            background-color: #4CAF50 !important;
            color: white !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Title
    st.markdown("<h2 style='text-align: center;'>Find a skincare product for...</h2>", unsafe_allow_html=True)

    # Skin Type Selection (2x2 Grid)
    st.markdown("### Skin Type")
    skin_types = {
        "Dry": "🧴 Dry",
        "Normal": "💧 Normal",
        "Oily": "🌿 Oily",
        "Sensitive": "🌸 Sensitive"
    }

    # Store selection state
    if "selected_skin_type" not in st.session_state:
        st.session_state.selected_skin_type = None

    # Skin Type Selection Grid
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)

    def select_skin_type(skin_type):
        st.session_state.selected_skin_type = skin_type

    # Row 1
    with col1:
        if st.button(skin_types["Dry"], key="dry", use_container_width=True):
            select_skin_type("Dry")
    with col2:
        if st.button(skin_types["Normal"], key="normal", use_container_width=True):
            select_skin_type("Normal")

    # Row 2
    with col3:
        if st.button(skin_types["Oily"], key="oily", use_container_width=True):
            select_skin_type("Oily")
    with col4:
        if st.button(skin_types["Sensitive"], key="sensitive", use_container_width=True):
            select_skin_type("Sensitive")

    
    st.markdown("### Principal Component")
    col1, col2 = st.columns(2)

    # Store component selection state
    if "selected_component" not in st.session_state:
        st.session_state.selected_component = None

    def select_component(component):
        st.session_state.selected_component = component

    with col1:
        if st.button("💦 water_based", key="water", use_container_width=True):
            select_component("water_based")
    with col2:
        if st.button("🧊 silicone_based", key="silicone", use_container_width=True):
            select_component("silicone_based")

    st.markdown("### Number of Recommendations")
    st.session_state.num_recommendations = st.slider("Select how many recommendations you want:", 1, 10, 5)


    # Show final selection
    if st.session_state.selected_skin_type and st.session_state.selected_component:
        if st.button("Get Recommendations", key="recommend", use_container_width=True):
            st.switch_page("pages/recommendation.py")  # Switch to the recommendation page

# Main execution
if __name__ == "__main__":
    homepage()