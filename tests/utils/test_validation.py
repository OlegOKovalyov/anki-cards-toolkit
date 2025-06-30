import pytest

from src.utils.validation import validate_config
from docs.error_messages import (
    DECK_NAME_MISSING,
    DECK_NAME_INVALID_WHITESPACE,
    DECK_NAME_INVALID_CHARACTERS,
)


def test_validate_config_success():
    config = {"deck_name": "My Valid Deck"}
    validate_config(config)


def test_validate_config_missing_deck_name():
    config = {}
    with pytest.raises(ValueError, match=DECK_NAME_MISSING):
        validate_config(config)


def test_validate_config_none_deck_name():
    config = {"deck_name": None}
    with pytest.raises(ValueError, match=DECK_NAME_MISSING):
        validate_config(config)


def test_validate_config_empty_deck_name():
    config = {"deck_name": ""}
    with pytest.raises(ValueError, match=DECK_NAME_INVALID_WHITESPACE):
        validate_config(config)


def test_validate_config_whitespace_deck_name():
    config = {"deck_name": "   "}
    with pytest.raises(ValueError, match=DECK_NAME_INVALID_WHITESPACE):
        validate_config(config)


@pytest.mark.parametrize("char", ['/', '\\', ':', '*', '?', '"', '<', '>', '|'])
def test_validate_config_forbidden_characters(char):
    config = {"deck_name": f"My Deck{char}Name"}
    with pytest.raises(ValueError, match=DECK_NAME_INVALID_CHARACTERS):
        validate_config(config) 