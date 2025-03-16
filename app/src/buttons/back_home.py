"""
This file contains the back_home_action function, 
which is used to navigate back to the homepage.
"""

import streamlit as st

def back_home_action():
    st.session_state.page = "homepage"
    st.session_state.do_rerun = True