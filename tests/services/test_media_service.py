"""Tests for the media service."""

import pytest
from unittest.mock import patch, MagicMock
from src.services.media_service import send_media_file
import requests

@patch('src.services.media_service.requests.post')
def test_send_media_file_success(mock_post):
    """Test successful media file upload."""
    mock_response = MagicMock()
    mock_response.json.return_value = {"result": "tts_test.mp3", "error": None}
    mock_post.return_value = mock_response

    success = send_media_file("tts_test.mp3", "base64data")
    
    assert success is True
    mock_post.assert_called_once()

@patch('src.services.media_service.requests.post')
def test_send_media_file_anki_error(mock_post):
    """Test media file upload when AnkiConnect returns an error."""
    mock_response = MagicMock()
    mock_response.json.return_value = {"result": None, "error": "deck not found"}
    mock_post.return_value = mock_response

    success = send_media_file("tts_test.mp3", "base64data")
    
    assert success is False
    mock_post.assert_called_once()

@patch('src.services.media_service.requests.post', side_effect=requests.exceptions.ConnectionError)
def test_send_media_file_connection_error(mock_post):
    """Test media file upload with a connection error."""
    success = send_media_file("tts_test.mp3", "base64data")
    
    assert success is False
    mock_post.assert_called_once() 