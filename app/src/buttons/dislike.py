"""
This file contains the dislike_action function, 
which is called when the dislike button is clicked.
"""

import streamlit as st

def dislike_action():
    """
    Function to handle the dislike button click.
    """
    st.session_state.current_index += 1
    st.session_state.do_rerun = True
