from typing import Dict, Any
import os
import sys

from src.locales.loader import get_message
from src.config.settings import ANKI_CONNECT_URL, CONFIG_FILE, MODEL_NAME


def validate_config(config: Dict[str, Any]) -> None:
    try:
        # Deck name validation
        deck_name = config.get("deck_name")
        if deck_name is None:
            raise ValueError(get_message("INITIALIZATION_CONFIGURATION.deck_name_missing"))
        if not isinstance(deck_name, str) or not deck_name.strip():
            raise ValueError(get_message("INITIALIZATION_CONFIGURATION.deck_name_invalid_whitespace"))
        forbidden_chars = r'\/\\*?"<>|'
        if any(char in deck_name for char in forbidden_chars):
            raise ValueError(get_message("INITIALIZATION_CONFIGURATION.deck_name_invalid_characters"))

        # Model name validation
        model_name = config.get("model_name")
        if model_name != MODEL_NAME:
            raise ValueError(get_message("INITIALIZATION_CONFIGURATION.model_name_invalid"))

        # Pexels API key validation
        pexels_api_key = config.get("pexels_api_key")
        if not (isinstance(pexels_api_key, str) and len(pexels_api_key) == 56 and ' ' not in pexels_api_key):
            raise ValueError(get_message("INITIALIZATION_CONFIGURATION.pexels_api_key_invalid"))

        # Big Huge API key validation
        big_huge_api_key = config.get("big_huge_api_key")
        if not (isinstance(big_huge_api_key, str) and len(big_huge_api_key) == 32 and ' ' not in big_huge_api_key):
            raise ValueError(get_message("INITIALIZATION_CONFIGURATION.big_huge_api_key_invalid"))

        # AnkiConnect URL validation
        anki_connect_url = config.get("anki_connect_url")
        if anki_connect_url != ANKI_CONNECT_URL:
            raise ValueError(get_message("INITIALIZATION_CONFIGURATION.anki_connect_url_invalid"))

        # Config file validation
        config_file = config.get("config_file")
        if config_file != CONFIG_FILE:
            raise ValueError(get_message("INITIALIZATION_CONFIGURATION.config_file_invalid"))

        # Critical data file validation
        if not os.path.exists("data/merged_cefr_frequency.csv"):
            raise ValueError(get_message("INITIALIZATION_CONFIGURATION.missing_cefr_file"))
        if not os.path.exists("data/irregular_verbs.py"):
            raise ValueError(get_message("INITIALIZATION_CONFIGURATION.missing_irregular_verbs_file"))
    except ValueError as e:
        print(get_message("INITIALIZATION_CONFIGURATION.config_error", error=e))
        print(get_message("INITIALIZATION_CONFIGURATION.config_fix"))
        sys.exit(1) 