import pytest
from unittest.mock import patch
from src.image_fetching.google_search import fetch_google_image

@patch("src.image_fetching.google_search.GoogleSearch.get_dict")
def test_fetch_google_image(mock_get_dict):
    """Test fetching an image from Google API."""
    mock_get_dict.return_value = {
        "images_results": [{"original": "http://example.com/google_image.jpg"}]
    }

    product_name = "Sunscreen"
    image_url = fetch_google_image(product_name)

    assert image_url == "http://example.com/google_image.jpg"

@patch("src.image_fetching.google_search.GoogleSearch.get_dict")
def test_fetch_google_image_fail(mock_get_dict):
    """Test handling when Google API returns no images."""
    mock_get_dict.return_value = {}

    product_name = "Unknown Product"
    image_url = fetch_google_image(product_name)

    assert image_url is None
