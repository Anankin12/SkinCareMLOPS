import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from types import SimpleNamespace
import streamlit as st

def test_back_home_action(monkeypatch):
    # Import the function from your buttons module.
    from src.buttons.back_home import back_home_action

    # Create a fake session state using SimpleNamespace.
    fake_state = SimpleNamespace()
    monkeypatch.setattr(st, "session_state", fake_state)

    # Call the back_home_action function.
    back_home_action()

    # Check that it sets the page to "homepage".
    assert fake_state.page == "homepage"


def test_like_action(monkeypatch):
    # Import the like action function.
    from src.buttons.like import like_action

    # Prepare a fake session state with a current_index.
    fake_state = SimpleNamespace(current_index=0)
    monkeypatch.setattr(st, "session_state", fake_state)

    like_action()
    # Expect that the like action increments current_index by 1.
    assert fake_state.current_index == 1


def test_dislike_action(monkeypatch):
    # Import the dislike action function.
    from src.buttons.dislike import dislike_action

    # Prepare a fake session state with a current_index.
    fake_state = SimpleNamespace(current_index=0)
    monkeypatch.setattr(st, "session_state", fake_state)

    dislike_action()
    # Expect that the dislike action increments current_index by 1.
    assert fake_state.current_index == 1
