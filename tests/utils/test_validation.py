import pytest

from src.utils.validation import validate_config
from docs.error_messages import CONFIG_ERRORS

# A valid config for use in tests
def valid_config():
    return {
        "deck_name": "Valid Deck",
        "model_name": "VocabCard_English_UA",
        "pexels_api_key": "a" * 56,
        "big_huge_api_key": "b" * 32,
        "anki_connect_url": "http://localhost:8765",
        "config_file": "last_deck.txt",
    }

def test_validate_config_success():
    config = valid_config()
    validate_config(config)

def test_validate_config_missing_deck_name():
    config = valid_config()
    config.pop("deck_name")
    with pytest.raises(ValueError, match=CONFIG_ERRORS['deck_name_missing']):
        validate_config(config)

def test_validate_config_none_deck_name():
    config = valid_config()
    config["deck_name"] = None
    with pytest.raises(ValueError, match=CONFIG_ERRORS['deck_name_missing']):
        validate_config(config)

def test_validate_config_empty_deck_name():
    config = valid_config()
    config["deck_name"] = ""
    with pytest.raises(ValueError, match=CONFIG_ERRORS['deck_name_invalid_whitespace']):
        validate_config(config)

def test_validate_config_whitespace_deck_name():
    config = valid_config()
    config["deck_name"] = "   "
    with pytest.raises(ValueError, match=CONFIG_ERRORS['deck_name_invalid_whitespace']):
        validate_config(config)

@pytest.mark.parametrize("char", ['/', '\\', ':', '*', '?', '"', '<', '>', '|'])
def test_validate_config_forbidden_characters(char):
    config = valid_config()
    config["deck_name"] = f"My Deck{char}Name"
    with pytest.raises(ValueError, match=CONFIG_ERRORS['deck_name_invalid_characters']):
        validate_config(config)

def test_validate_config_invalid_model_name():
    config = valid_config()
    config["model_name"] = "WrongModel"
    with pytest.raises(ValueError, match=CONFIG_ERRORS['model_name_invalid']):
        validate_config(config)

def test_validate_config_invalid_pexels_api_key_length():
    config = valid_config()
    config["pexels_api_key"] = "a" * 55
    with pytest.raises(ValueError, match=CONFIG_ERRORS['pexels_api_key_invalid']):
        validate_config(config)

def test_validate_config_invalid_pexels_api_key_spaces():
    config = valid_config()
    config["pexels_api_key"] = "a" * 55 + " "
    with pytest.raises(ValueError, match=CONFIG_ERRORS['pexels_api_key_invalid']):
        validate_config(config)

def test_validate_config_invalid_big_huge_api_key_length():
    config = valid_config()
    config["big_huge_api_key"] = "b" * 31
    with pytest.raises(ValueError, match=CONFIG_ERRORS['big_huge_api_key_invalid']):
        validate_config(config)

def test_validate_config_invalid_big_huge_api_key_spaces():
    config = valid_config()
    config["big_huge_api_key"] = "b" * 31 + " "
    with pytest.raises(ValueError, match=CONFIG_ERRORS['big_huge_api_key_invalid']):
        validate_config(config)

def test_validate_config_invalid_anki_connect_url():
    config = valid_config()
    config["anki_connect_url"] = "http://127.0.0.1:8765"
    with pytest.raises(ValueError, match=CONFIG_ERRORS['anki_connect_url_invalid']):
        validate_config(config)

def test_validate_config_invalid_config_file():
    config = valid_config()
    config["config_file"] = "wrong.txt"
    with pytest.raises(ValueError, match=CONFIG_ERRORS['config_file_invalid']):
        validate_config(config) 