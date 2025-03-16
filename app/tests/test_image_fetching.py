import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
import requests
from src.image_fetching.google_search import fetch_google_image

# A fake response for a successful Google API call.
class FakeSuccessResponse:
    def raise_for_status(self):
        pass
    def json(self):
        return {
            "items": [{"link": "https://example.com/image.jpg"}]
        }

# A fake response for when no items are found.
class FakeNoResultsResponse:
    def raise_for_status(self):
        pass
    def json(self):
        return {"items": []}

# A fake function to simulate network failure by raising a RequestException.
def fake_requests_get_failure(url, params):
    raise requests.RequestException("Network error")

# Test successful fetch.
def test_fetch_google_image_success(monkeypatch):
    def fake_requests_get(url, params):
        return FakeSuccessResponse()
    # Patch requests.get in the google_search module.
    monkeypatch.setattr("src.image_fetching.google_search.requests.get", fake_requests_get)
    result = fetch_google_image("Test Product")
    assert result == "https://example.com/image.jpg"

# Test when no results are returned.
def test_fetch_google_image_no_results(monkeypatch):
    def fake_requests_get(url, params):
        return FakeNoResultsResponse()
    monkeypatch.setattr("src.image_fetching.google_search.requests.get", fake_requests_get)
    result = fetch_google_image("Test Product")
    assert result is None

# Test when a RequestException occurs.
def test_fetch_google_image_failure(monkeypatch):
    monkeypatch.setattr("src.image_fetching.google_search.requests.get", fake_requests_get_failure)
    result = fetch_google_image("Test Product")
    assert result is None
