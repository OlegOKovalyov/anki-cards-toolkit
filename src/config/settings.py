import os
from dotenv import load_dotenv

# Load .env if it exists
load_dotenv(override=True)

# MODEL_NAME refers to the name of the Note Type in Anki.
# To check or change it in Anki: open Anki → Tools → Manage Note Types.
# Your note type should be  named as VocabCard_English_UA
MODEL_NAME = os.getenv("MODEL_NAME", "VocabCard_English_UA")

# DECK_NAME is the name of the Anki deck where the new cards will be added.
# You can create or check deck names via Anki: open Anki → Decks → Add.
# The initial deck name will be Default
DECK_NAME = os.getenv("DECK_NAME", "Default")

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "")  # API key for Pexels
BIG_HUGE_API_KEY = os.getenv("BIG_HUGE_API_KEY", "")  # API key for Big Huge Thesaurus
ANKI_CONNECT_URL = os.getenv("ANKI_CONNECT_URL", "http://localhost:8765")  # URL of the AnkiConnect server

# Path to the file where the name of the last used deck will be stored
CONFIG_FILE = os.getenv("CONFIG_FILE", "last_deck.txt")

# API URLs
DICTIONARY_API_URL = os.getenv("DICTIONARY_API_URL", "https://api.dictionaryapi.dev/api/v2/entries/en")
BIGHUGE_API_URL = os.getenv("BIGHUGE_API_URL", "https://words.bighugelabs.com/api/2") 
PEXELS_API_URL = os.getenv("PEXELS_API_URL", "https://api.pexels.com/v1/search") 
PEXELS_IMAGE_COUNT = int(os.getenv("PEXELS_IMAGE_COUNT", "16")) 