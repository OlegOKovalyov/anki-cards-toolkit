from typing import Dict, Any

from docs.error_messages import CONFIG_ERRORS


def validate_config(config: Dict[str, Any]) -> None:
    # Deck name validation
    deck_name = config.get("deck_name")
    if deck_name is None:
        raise ValueError(CONFIG_ERRORS['deck_name_missing'])
    if not isinstance(deck_name, str) or not deck_name.strip():
        raise ValueError(CONFIG_ERRORS['deck_name_invalid_whitespace'])
    forbidden_chars = r'\/\\*?"<>|'
    if any(char in deck_name for char in forbidden_chars):
        raise ValueError(CONFIG_ERRORS['deck_name_invalid_characters'])

    # Model name validation
    model_name = config.get("model_name")
    if model_name != "VocabCard_English_UA":
        raise ValueError(CONFIG_ERRORS['model_name_invalid'])

    # Pexels API key validation
    pexels_api_key = config.get("pexels_api_key")
    if not (isinstance(pexels_api_key, str) and len(pexels_api_key) == 56 and ' ' not in pexels_api_key):
        raise ValueError(CONFIG_ERRORS['pexels_api_key_invalid'])

    # Big Huge API key validation
    big_huge_api_key = config.get("big_huge_api_key")
    if not (isinstance(big_huge_api_key, str) and len(big_huge_api_key) == 32 and ' ' not in big_huge_api_key):
        raise ValueError(CONFIG_ERRORS['big_huge_api_key_invalid'])

    # AnkiConnect URL validation
    anki_connect_url = config.get("anki_connect_url")
    if anki_connect_url != "http://localhost:8765":
        raise ValueError(CONFIG_ERRORS['anki_connect_url_invalid'])

    # Config file validation
    config_file = config.get("config_file")
    if config_file != "last_deck.txt":
        raise ValueError(CONFIG_ERRORS['config_file_invalid']) 