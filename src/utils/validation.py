from typing import Dict, Any
import os
import sys

from docs.messages import INITIALIZATION_CONFIGURATION
from src.config.settings import ANKI_CONNECT_URL, CONFIG_FILE


def validate_config(config: Dict[str, Any]) -> None:
    try:
        # Deck name validation
        deck_name = config.get("deck_name")
        if deck_name is None:
            raise ValueError(INITIALIZATION_CONFIGURATION['deck_name_missing'])
        if not isinstance(deck_name, str) or not deck_name.strip():
            raise ValueError(INITIALIZATION_CONFIGURATION['deck_name_invalid_whitespace'])
        forbidden_chars = r'\/\\*?"<>|'
        if any(char in deck_name for char in forbidden_chars):
            raise ValueError(INITIALIZATION_CONFIGURATION['deck_name_invalid_characters'])

        # Model name validation
        model_name = config.get("model_name")
        if model_name != "VocabCard_English_UA":
            raise ValueError(INITIALIZATION_CONFIGURATION['model_name_invalid'])

        # Pexels API key validation
        pexels_api_key = config.get("pexels_api_key")
        if not (isinstance(pexels_api_key, str) and len(pexels_api_key) == 56 and ' ' not in pexels_api_key):
            raise ValueError(INITIALIZATION_CONFIGURATION['pexels_api_key_invalid'])

        # Big Huge API key validation
        big_huge_api_key = config.get("big_huge_api_key")
        if not (isinstance(big_huge_api_key, str) and len(big_huge_api_key) == 32 and ' ' not in big_huge_api_key):
            raise ValueError(INITIALIZATION_CONFIGURATION['big_huge_api_key_invalid'])

        # AnkiConnect URL validation
        anki_connect_url = config.get("anki_connect_url")
        if anki_connect_url != ANKI_CONNECT_URL:
            raise ValueError(INITIALIZATION_CONFIGURATION['anki_connect_url_invalid'])

        # Config file validation
        config_file = config.get("config_file")
        if config_file != CONFIG_FILE:
            raise ValueError(INITIALIZATION_CONFIGURATION['config_file_invalid'])

        # Critical data file validation
        if not os.path.exists("data/merged_cefr_frequency.csv"):
            raise ValueError(INITIALIZATION_CONFIGURATION["missing_cefr_file"])
        if not os.path.exists("data/irregular_verbs.py"):
            raise ValueError(INITIALIZATION_CONFIGURATION["missing_irregular_verbs_file"])
    except ValueError as e:
        print(INITIALIZATION_CONFIGURATION["config_error"].format(error=e))
        print(INITIALIZATION_CONFIGURATION["config_fix"])
        sys.exit(1) 