import pytest
from unittest.mock import patch
from src.image_fetching.ebay_api import fetch_ebay_image

@patch("src.image_fetching.ebay_api.requests.get")
def test_fetch_ebay_image(mock_get):
    """Test fetching an image from eBay API with a valid response."""
    mock_response = {
        "findItemsByKeywordsResponse": [{
            "searchResult": [{
                "item": [{"galleryURL": "http://example.com/image.jpg"}]
            }]
        }]
    }

    mock_get.return_value.json.return_value = mock_response

    product_name = "Face Cream"
    image_url = fetch_ebay_image(product_name)

    assert image_url == "http://example.com/image.jpg"

@patch("src.image_fetching.ebay_api.requests.get")
def test_fetch_ebay_image_fail(mock_get):
    """Test eBay API failure handling."""
    mock_get.return_value.json.return_value = {}

    product_name = "Unknown Product"
    image_url = fetch_ebay_image(product_name)

    assert image_url is None
