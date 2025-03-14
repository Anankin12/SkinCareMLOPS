import pytest
from unittest.mock import patch
from src.image_fetching.fetcher import fetch_product_image

@patch("src.image_fetching.cache_checker.get_cached_image", return_value="http://cached.com/image.jpg")
def test_fetch_product_image_cache(mock_cache):
    """Test fetcher retrieves an image from cache first."""
    product_name = "Lotion"
    image_url = fetch_product_image(product_name)

    assert image_url == "http://cached.com/image.jpg"

@patch("src.image_fetching.cache_checker.get_cached_image", return_value=None)
@patch("src.image_fetching.ebay_api.fetch_ebay_image", return_value="http://ebay.com/image.jpg")
@patch("src.image_fetching.cache_manager.save_to_cache")
def test_fetch_product_image_ebay(mock_cache, mock_ebay, mock_get_cache):
    """Test fetcher retrieves an image from eBay if cache is empty."""
    product_name = "Serum"
    image_url = fetch_product_image(product_name)

    assert image_url == "http://ebay.com/image.jpg"

@patch("src.image_fetching.cache_checker.get_cached_image", return_value=None)
@patch("src.image_fetching.ebay_api.fetch_ebay_image", return_value=None)
@patch("src.image_fetching.google_search.fetch_google_image", return_value="http://google.com/image.jpg")
@patch("src.image_fetching.cache_manager.save_to_cache")
def test_fetch_product_image_google(mock_cache, mock_google, mock_ebay, mock_get_cache):
    """Test fetcher retrieves an image from Google if both cache and eBay fail."""
    product_name = "Lip Balm"
    image_url = fetch_product_image(product_name)

    assert image_url == "http://google.com/image.jpg"
