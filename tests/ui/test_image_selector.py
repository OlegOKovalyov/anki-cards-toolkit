"""Tests for the image selection UI logic."""

import pytest
from unittest.mock import patch, mock_open
from src.ui.image_selector import create_image_selection_page, select_image_for_card

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

def sample_images():
    return [
        {"src": {"medium": "http://example.com/img1.jpg"}},
        {"src": {"medium": "http://example.com/img2.jpg"}},
        {"src": {"medium": "http://example.com/img3.jpg"}},
    ]

def test_select_image_for_card_valid_number(monkeypatch):
    # User selects image 2
    monkeypatch.setattr('builtins.input', lambda prompt: "2")
    with patch('src.ui.image_selector.fetch_pexels_images', return_value=sample_images()), \
         patch('src.ui.image_selector.webbrowser.open'), \
         patch('tempfile.NamedTemporaryFile') as mock_tempfile:
        # Mock temp file context manager
        mock_tempfile.return_value.__enter__.return_value.name = '/tmp/fake.html'
        mock_tempfile.return_value.__enter__.return_value.write = lambda x: None
        monkeypatch.setattr('os.unlink', lambda path: None)
        url = select_image_for_card("testword")
    assert url == "http://example.com/img2.jpg"

def test_select_image_for_card_enter(monkeypatch):
    # User presses Enter
    monkeypatch.setattr('builtins.input', lambda prompt: "")
    with patch('src.ui.image_selector.fetch_pexels_images', return_value=sample_images()), \
         patch('src.ui.image_selector.webbrowser.open'), \
         patch('tempfile.NamedTemporaryFile') as mock_tempfile:
        mock_tempfile.return_value.__enter__.return_value.name = '/tmp/fake.html'
        mock_tempfile.return_value.__enter__.return_value.write = lambda x: None
        monkeypatch.setattr('os.unlink', lambda path: None)
        url = select_image_for_card("testword")
    assert url == "http://example.com/img1.jpg"

def test_select_image_for_card_escape(monkeypatch):
    # User enters 'esc'
    monkeypatch.setattr('builtins.input', lambda prompt: "esc")
    with patch('src.ui.image_selector.fetch_pexels_images', return_value=sample_images()), \
         patch('src.ui.image_selector.webbrowser.open'), \
         patch('tempfile.NamedTemporaryFile') as mock_tempfile:
        mock_tempfile.return_value.__enter__.return_value.name = '/tmp/fake.html'
        mock_tempfile.return_value.__enter__.return_value.write = lambda x: None
        monkeypatch.setattr('os.unlink', lambda path: None)
        url = select_image_for_card("testword")
    assert url == ""

def test_select_image_for_card_no_images(monkeypatch):
    # No images found
    with patch('src.ui.image_selector.fetch_pexels_images', return_value=[]), \
         patch('src.ui.image_selector.webbrowser.open'), \
         patch('tempfile.NamedTemporaryFile') as mock_tempfile:
        mock_tempfile.return_value.__enter__.return_value.name = '/tmp/fake.html'
        mock_tempfile.return_value.__enter__.return_value.write = lambda x: None
        monkeypatch.setattr('os.unlink', lambda path: None)
        url = select_image_for_card("testword")
    assert url == "" 