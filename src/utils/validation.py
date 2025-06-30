from typing import Dict, Any

from docs.error_messages import (
    DECK_NAME_INVALID_WHITESPACE,
    DECK_NAME_MISSING,
    DECK_NAME_INVALID_CHARACTERS,
)


def validate_config(config: Dict[str, Any]) -> None:
    deck_name = config.get("deck_name")

    if deck_name is None:
        raise ValueError(DECK_NAME_MISSING)

    if not isinstance(deck_name, str) or not deck_name.strip():
        raise ValueError(DECK_NAME_INVALID_WHITESPACE)

    forbidden_chars = r'\/\\:*?"<>|'
    if any(char in deck_name for char in forbidden_chars):
        raise ValueError(DECK_NAME_INVALID_CHARACTERS) 