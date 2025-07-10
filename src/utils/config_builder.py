import os
from src.config import settings

def config_build(default_deck_name: str = None) -> dict:
    """
    Builds and returns a configuration dictionary.
    If default_deck_name is given, it is used, 
    otherwise the DECK_NAME from settings is used.
    """
    deck_name = default_deck_name or settings.DECK_NAME

    config = {
        "deck_name": deck_name,
        "model_name": settings.MODEL_NAME,
        "pexels_api_key": settings.PEXELS_API_KEY,
        "big_huge_api_key": settings.BIG_HUGE_API_KEY,
        "anki_connect_url": settings.ANKI_CONNECT_URL,
        "config_file": settings.CONFIG_FILE,
    }
    return config

def get_default_deck_name(config: dict) -> str:
    """
    Returns the deck name from the last_deck.txt file, 
    or from config, or 'Default'.
    """
    deck_name = None
    config_file = config.get("config_file")
    if config_file and os.path.exists(config_file):
        with open(config_file, "r") as f:
            deck_name = f.read().strip()
    if not deck_name:
        deck_name = config.get("deck_name") or "Default"
    return deck_name
