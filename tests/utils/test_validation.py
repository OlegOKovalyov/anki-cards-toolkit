import pytest
import os
import sys
import requests

from src.utils.validation import validate_config
from src.services.anki_service import check_anki_connect
from src.config import settings

@pytest.fixture(autouse=True)
def set_user_locale():
    """Set USER_LOCALE to 'en' for all validation tests to avoid language prompts."""
    os.environ['USER_LOCALE'] = 'en'
    yield
    # Clean up after test
    if 'USER_LOCALE' in os.environ:
        del os.environ['USER_LOCALE']

# A valid config for use in tests
def valid_config():
    return {
        "deck_name": "Valid Deck",
        "model_name": settings.MODEL_NAME,
        "pexels_api_key": "a" * 56,
        "big_huge_api_key": "b" * 32,
        "anki_connect_url": settings.ANKI_CONNECT_URL,
        "config_file": settings.CONFIG_FILE,
    }

def test_validate_config_success():
    config = valid_config()
    validate_config(config)

def test_validate_config_missing_deck_name(monkeypatch):
    config = valid_config()
    config.pop("deck_name")
    monkeypatch.setattr("sys.exit", lambda code=1: (_ for _ in ()).throw(SystemExit(code)))
    with pytest.raises(SystemExit):
        validate_config(config)

def test_validate_config_none_deck_name(monkeypatch):
    config = valid_config()
    config["deck_name"] = None
    monkeypatch.setattr("sys.exit", lambda code=1: (_ for _ in ()).throw(SystemExit(code)))
    with pytest.raises(SystemExit):
        validate_config(config)

def test_validate_config_empty_deck_name(monkeypatch):
    config = valid_config()
    config["deck_name"] = ""
    monkeypatch.setattr("sys.exit", lambda code=1: (_ for _ in ()).throw(SystemExit(code)))
    with pytest.raises(SystemExit):
        validate_config(config)

def test_validate_config_whitespace_deck_name(monkeypatch):
    config = valid_config()
    config["deck_name"] = "   "
    monkeypatch.setattr("sys.exit", lambda code=1: (_ for _ in ()).throw(SystemExit(code)))
    with pytest.raises(SystemExit):
        validate_config(config)

@pytest.mark.parametrize("char", ['/', '\\', '*', '?', '"', '<', '>', '|'])
def test_validate_config_forbidden_characters(char, monkeypatch):
    config = valid_config()
    config["deck_name"] = f"My Deck{char}Name"
    monkeypatch.setattr("sys.exit", lambda code=1: (_ for _ in ()).throw(SystemExit(code)))
    with pytest.raises(SystemExit):
        validate_config(config)

def test_validate_config_invalid_model_name(monkeypatch):
    config = valid_config()
    config["model_name"] = "WrongModel"
    monkeypatch.setattr("sys.exit", lambda code=1: (_ for _ in ()).throw(SystemExit(code)))
    with pytest.raises(SystemExit):
        validate_config(config)

def test_validate_config_invalid_pexels_api_key_length(monkeypatch):
    config = valid_config()
    config["pexels_api_key"] = "a" * 55
    monkeypatch.setattr("sys.exit", lambda code=1: (_ for _ in ()).throw(SystemExit(code)))
    with pytest.raises(SystemExit):
        validate_config(config)

def test_validate_config_invalid_pexels_api_key_spaces(monkeypatch):
    config = valid_config()
    config["pexels_api_key"] = "a" * 55 + " "
    monkeypatch.setattr("sys.exit", lambda code=1: (_ for _ in ()).throw(SystemExit(code)))
    with pytest.raises(SystemExit):
        validate_config(config)

def test_validate_config_invalid_big_huge_api_key_length(monkeypatch):
    config = valid_config()
    config["big_huge_api_key"] = "b" * 31
    monkeypatch.setattr("sys.exit", lambda code=1: (_ for _ in ()).throw(SystemExit(code)))
    with pytest.raises(SystemExit):
        validate_config(config)

def test_validate_config_invalid_big_huge_api_key_spaces(monkeypatch):
    config = valid_config()
    config["big_huge_api_key"] = "b" * 31 + " "
    monkeypatch.setattr("sys.exit", lambda code=1: (_ for _ in ()).throw(SystemExit(code)))
    with pytest.raises(SystemExit):
        validate_config(config)

def test_validate_config_invalid_anki_connect_url(monkeypatch):
    config = valid_config()
    config["anki_connect_url"] = "http://127.0.0.1:8765"
    monkeypatch.setattr("sys.exit", lambda code=1: (_ for _ in ()).throw(SystemExit(code)))
    with pytest.raises(SystemExit):
        validate_config(config)

def test_validate_config_invalid_config_file(monkeypatch):
    config = valid_config()
    config["config_file"] = "wrong.txt"
    monkeypatch.setattr("sys.exit", lambda code=1: (_ for _ in ()).throw(SystemExit(code)))
    with pytest.raises(SystemExit):
        validate_config(config)

def test_validate_config_missing_cefr_file(monkeypatch):
    config = valid_config()
    monkeypatch.setattr("os.path.exists", lambda path: False if path == "data/merged_cefr_frequency.csv" else True)
    monkeypatch.setattr("sys.exit", lambda code=1: (_ for _ in ()).throw(SystemExit(code)))
    with pytest.raises(SystemExit):
        validate_config(config)

def test_validate_config_missing_irregular_verbs_file(monkeypatch):
    config = valid_config()
    monkeypatch.setattr("os.path.exists", lambda path: False if path == "data/irregular_verbs.py" else True)
    monkeypatch.setattr("sys.exit", lambda code=1: (_ for _ in ()).throw(SystemExit(code)))
    with pytest.raises(SystemExit):
        validate_config(config)

def test_check_anki_connect_connection_error(monkeypatch):
    # Patch requests.get to raise ConnectionError
    monkeypatch.setattr(requests, "get", lambda *a, **kw: (_ for _ in ()).throw(requests.exceptions.ConnectionError()))
    # Patch sys.exit to raise SystemExit
    exit_calls = []
    def fake_exit(code=1):
        exit_calls.append(code)
        raise SystemExit(code)
    monkeypatch.setattr(sys, "exit", fake_exit)
    with pytest.raises(SystemExit):
        check_anki_connect()
    assert exit_calls == [1] 