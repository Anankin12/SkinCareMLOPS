"""
This file contains tests for the buttons modules.
"""
import sys
import os
from types import SimpleNamespace
import pytest
import streamlit as st

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.buttons.back_home import back_home_action
from src.buttons.like import like_action
from src.buttons.dislike import dislike_action


def test_back_home_action(monkeypatch):
    """
    Test the back_home_action function.
    """
    # Create a fake session state using SimpleNamespace.
    fake_state = SimpleNamespace()
    monkeypatch.setattr(st, "session_state", fake_state)

    # Call the back_home_action function.
    back_home_action()

    # Check that it sets the page to "homepage".
    assert fake_state.page == "homepage"


def test_like_action(monkeypatch):
    """
    Test the like_action function.
    """
    # Prepare a fake session state with a current_index.
    fake_state = SimpleNamespace(current_index=0)
    monkeypatch.setattr(st, "session_state", fake_state)

    like_action()
    # Expect that the like action increments current_index by 1.
    assert fake_state.current_index == 1


def test_dislike_action(monkeypatch):
    """
    Test the dislike_action function.
    """
    # Prepare a fake session state with a current_index.
    fake_state = SimpleNamespace(current_index=0)
    monkeypatch.setattr(st, "session_state", fake_state)

    dislike_action()
    # Expect that the dislike action increments current_index by 1.
    assert fake_state.current_index == 1
