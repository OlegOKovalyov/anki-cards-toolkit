import os
from dotenv import load_dotenv

# Load .env if it exists
load_dotenv(override=True)

# Reading constants from the environment

# == Configuration from .env ==
# MODEL_NAME refers to the name of the Note Type in Anki.
# To check or change it in Anki: open Anki → Tools → Manage Note Types.
# Your note type should be  named as VocabCard_English_UA
MODEL_NAME = os.getenv("MODEL_NAME")

# DECK_NAME is the name of the Anki deck where the new cards will be added.
# You can create or check deck names via Anki: open Anki → Decks → Add.
# The initial deck name will be Default
DECK_NAME = os.getenv("DECK_NAME")

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY") # API key for Pexels
BIG_HUGE_API_KEY = os.getenv("BIG_HUGE_API_KEY") # API key for Big Huge Thesaurus
ANKI_CONNECT_URL = os.getenv("ANKI_CONNECT_URL") # URL of the AnkiConnect server

# Path to the file where the name of the last used deck will be stored
CONFIG_FILE = os.getenv("CONFIG_FILE") # last_deck.txt

def config_build(default_deck_name: str = None) -> dict:
    """
    Builds and returns a configuration dictionary.
    If default_deck_name is given, it is used, 
    otherwise the DECK_NAME from .env is used.
    """
    deck_name = default_deck_name or DECK_NAME

    config = {
        "deck_name": deck_name,
        "model_name": MODEL_NAME,
        "pexels_api_key": PEXELS_API_KEY,
        "big_huge_api_key": BIG_HUGE_API_KEY,
        "anki_connect_url": ANKI_CONNECT_URL,
        "config_file": CONFIG_FILE,
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
