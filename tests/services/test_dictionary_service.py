import pytest
from unittest.mock import patch, MagicMock
from src.services.dictionary_service import fetch_word_data, format_dictionary_entry

# Mock API responses
mock_dict_response = {
    "word": "test",
    "meanings": [
        {
            "partOfSpeech": "noun",
            "definitions": [{"definition": "a procedure for critical evaluation", "example": "a test of skill"}]
        },
        {
            "partOfSpeech": "verb",
            "definitions": [{"definition": "take measures to check the quality", "example": "this is a test"}]
        }
    ]
}

mock_thes_response = {
    "noun": {"syn": ["trial", "examination"], "ant": ["proof"]},
    "verb": {"syn": ["check", "try"], "ant": ["guess"]}
}

@patch('src.services.dictionary_service._fetch_thesaurus_api_data')
@patch('src.services.dictionary_service._fetch_dictionary_api_data')
def test_fetch_word_data_with_pos(mock_fetch_dict, mock_fetch_thes):
    """Test fetching data for a specific part of speech."""
    mock_fetch_dict.return_value = mock_dict_response
    mock_fetch_thes.return_value = mock_thes_response

    result = fetch_word_data("test", requested_pos="noun")

    assert result is not None
    assert result['partOfSpeech'] == 'noun'
    assert result['definition'] == "a procedure for critical evaluation"
    assert "trial" in result['synonyms']
    assert "examination" in result['synonyms']
    assert "proof" in result['antonyms']

@patch('src.services.dictionary_service._fetch_thesaurus_api_data')
@patch('src.services.dictionary_service._fetch_dictionary_api_data')
def test_fetch_word_data_no_pos(mock_fetch_dict, mock_fetch_thes):
    """Test fetching data without a specific part of speech (defaults to first)."""
    mock_fetch_dict.return_value = mock_dict_response
    mock_fetch_thes.return_value = mock_thes_response

    result = fetch_word_data("test")

    assert result is not None
    assert result['partOfSpeech'] == 'noun'
    assert "trial" in result['synonyms'] # Synonyms from all POS are combined

@patch('src.services.dictionary_service._fetch_dictionary_api_data')
def test_fetch_word_data_dict_fails(mock_fetch_dict):
    """Test when the dictionary API call fails."""
    mock_fetch_dict.return_value = None

    result = fetch_word_data("test")
    assert result is None

@patch('src.services.dictionary_service._fetch_thesaurus_api_data')
@patch('src.services.dictionary_service._fetch_dictionary_api_data')
def test_fetch_word_data_thesaurus_fails(mock_fetch_dict, mock_fetch_thes):
    """Test when only the thesaurus API call fails."""
    mock_fetch_dict.return_value = mock_dict_response
    mock_fetch_thes.return_value = None

    result = fetch_word_data("test", requested_pos="noun")

    assert result is not None
    assert result['partOfSpeech'] == 'noun'
    assert result['synonyms'] == "" # No synonyms should be found
    assert result['antonyms'] == "" 

def test_format_dictionary_entry_multi_entry():
    # Simulate two entries: noun and verb, with two noun entries
    data = [
        {
            "word": "test",
            "phonetics": [{"text": "/tɛst/"}],
            "meanings": [
                {
                    "partOfSpeech": "noun",
                    "definitions": [
                        {"definition": "a procedure for critical evaluation", "example": "a test of skill"}
                    ]
                }
            ]
        },
        {
            "word": "test",
            "phonetics": [],
            "meanings": [
                {
                    "partOfSpeech": "noun",
                    "definitions": [
                        {"definition": "an event or situation that reveals the strength or quality of someone or something"}
                    ]
                },
                {
                    "partOfSpeech": "verb",
                    "definitions": [
                        {"definition": "take measures to check the quality", "example": "this is a test"}
                    ]
                }
            ]
        }
    ]
    html = format_dictionary_entry(data)
    # Should include both noun definitions under one heading, and verb under another
    assert html.count('<div class="pos">noun</div>') == 1
    assert html.count('<div class="pos">verb</div>') == 1
    assert "a procedure for critical evaluation" in html
    assert "an event or situation that reveals the strength or quality of someone or something" in html
    assert "take measures to check the quality" in html
    assert "/tɛst/" in html  # phonetic from first entry 
    