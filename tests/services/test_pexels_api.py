import pytest
from unittest.mock import patch
from src.services.pexels_api import fetch_pexels_images

@patch('src.services.pexels_api.get_api_data')
def test_fetch_pexels_images_success(mock_get_api_data):
    """Test fetch_pexels_images for a successful API call."""
    mock_response = {
        "photos": [
            {"id": 1, "src": {"medium": "url1"}},
            {"id": 2, "src": {"medium": "url2"}}
        ]
    }
    mock_get_api_data.return_value = mock_response
    
    images = fetch_pexels_images("nature")
    
    assert len(images) == 2
    assert images[0]['id'] == 1
    mock_get_api_data.assert_called_once()

@patch('src.services.pexels_api.get_api_data')
def test_fetch_pexels_images_failure(mock_get_api_data):
    """Test fetch_pexels_images for a failed API call."""
    mock_get_api_data.return_value = None
    
    images = fetch_pexels_images("nature")
    
    assert images == []
    mock_get_api_data.assert_called_once()

@patch('src.services.pexels_api.get_api_data')
def test_fetch_pexels_images_no_photos_key(mock_get_api_data):
    """Test fetch_pexels_images when response is missing 'photos' key."""
    mock_get_api_data.return_value = {"total_results": 0}
    
    images = fetch_pexels_images("nature")
    
    assert images == []
    mock_get_api_data.assert_called_once() 