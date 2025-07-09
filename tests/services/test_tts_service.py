"""Tests for the TTS service."""

import pytest
from unittest.mock import patch, MagicMock
from src.services.tts_service import generate_tts_base64

@patch('src.services.tts_service.gTTS')
def test_generate_tts_base64_success(mock_gtts):
    """Test successful TTS generation."""
    # Mock the gTTS object and its write_to_fp method
    mock_tts_instance = MagicMock()
    mock_gtts.return_value = mock_tts_instance
    
    # Simulate writing to the BytesIO buffer
    def write_to_fp_side_effect(buffer):
        buffer.write(b'fake_mp3_data')
    mock_tts_instance.write_to_fp.side_effect = write_to_fp_side_effect

    sound_ref, encoded_data = generate_tts_base64("hello", "hello_word")
    
    assert sound_ref == "[sound:tts_hello_word.mp3]"
    assert encoded_data == "ZmFrZV9tcDNfZGF0YQ==" # base64 for 'fake_mp3_data'
    mock_gtts.assert_called_once_with("hello")
    mock_tts_instance.write_to_fp.assert_called_once()

@patch('src.services.tts_service.gTTS', side_effect=Exception("TTS API is down"))
def test_generate_tts_base64_failure(mock_gtts):
    """Test TTS generation failure."""
    sound_ref, encoded_data = generate_tts_base64("hello", "hello_word", exit_on_error=False)
    
    assert sound_ref is None
    assert encoded_data is None
    mock_gtts.assert_called_once_with("hello") 