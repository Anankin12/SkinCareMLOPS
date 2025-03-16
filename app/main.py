"""
Main entry point for the SkinCareMLOPS web application.
"""

import streamlit as st
from config import PAGE_CONFIG

# IMPORTANT: This must be the first Streamlit call in this script
st.set_page_config(**PAGE_CONFIG)


from controllers.homepage import homepage
from controllers.recommendation import recommendation_page

def main():
    """
    Configure Streamlit settings and launch the appropriate page.
    """
    # Simple manual navigation approach using session state
    if "page" not in st.session_state:
        st.session_state.page = "homepage"

    if st.session_state.page == "homepage":
        homepage()
    elif st.session_state.page == "recommendation":
        recommendation_page()

if __name__ == '__main__':
    main()
