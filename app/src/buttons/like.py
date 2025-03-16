"""
This file contains the like_action function which is 
called when the like button is clicked.
"""

import streamlit as st

def like_action():
    """
    Function to handle the like button click.
    """
    st.session_state.current_index += 1
    st.session_state.do_rerun = True
