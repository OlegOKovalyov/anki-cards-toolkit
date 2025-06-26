"""Tests for the image selection UI logic."""

import pytest
from unittest.mock import patch, mock_open
from src.ui.image_selector import create_image_selection_page

def test_create_image_selection_page_generates_html():
    images = [
        {"src": {"medium": "http://example.com/img1.jpg"}},
        {"src": {"medium": "http://example.com/img2.jpg"}}
    ]
    word = "testword"
    fake_template = "<html>{{word}}<div>{{image_grid}}</div></html>"
    with patch("builtins.open", mock_open(read_data=fake_template)):
        html = create_image_selection_page(images, word)
    assert "img1.jpg" in html
    assert "img2.jpg" in html
    assert word in html
    assert html.count('<div class="image-container">') == 2 