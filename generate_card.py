import os
import sys
from dotenv import load_dotenv
from docs.error_messages import (
    PEXELS_API_ERRORS,
    ANKI_ERRORS,
    TTS_ERRORS,
    DICTIONARY_ERRORS,
    IMAGE_SELECTION_ERRORS,
    GENERAL_ERRORS,
    SUCCESS_MESSAGES,
    CONFIG_ERRORS
)
from src.services.clipboard_service import get_clean_sentence_from_clipboard
from src.linguistics.pos import detect_pos_from_context, get_irregular_forms
from src.utils.highlight import highlight_focus_word
from src.services.pexels_api import fetch_pexels_images
from src.services.dictionary_service import (
    fetch_word_data,
    format_dictionary_entry,
    format_word_list,
    load_cefr_frequency_data
)
from src.services.tts_service import generate_tts_base64
from src.services.media_service import send_media_file
from src.ui.image_selector import create_image_selection_page, select_image
from src.services.anki_service import check_anki_connect, add_note
from src.services.deck_service import get_deck_name, create_deck_if_not_exists, load_last_deck
from src.utils.validation import validate_config

# ============================================================================
# STEP 1: INITIALIZATION & CONFIGURATION
# ============================================================================

# Load .env file
load_dotenv()

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

# Read deck name from last_deck.txt or .env, but do NOT prompt the user before validation
default_deck_name = None
if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "r") as f:
        default_deck_name = f.read().strip()
if not default_deck_name:
    default_deck_name = os.getenv("DECK_NAME") or "Default"

# ===== STRICT EARLY CONFIG VALIDATION (no user prompt, no data loading) =====
config = {
    "deck_name": default_deck_name,
    "model_name": MODEL_NAME,
    "pexels_api_key": PEXELS_API_KEY,
    "big_huge_api_key": BIG_HUGE_API_KEY,
    "anki_connect_url": ANKI_CONNECT_URL,
    "config_file": CONFIG_FILE,
}

try:
    validate_config(config)
except ValueError as e:
    print(f"\n❌ Config error: {e}")
    print("Please fix the configuration and try again.")
    sys.exit(1)

# =========================================================================
# STEP 2: ANKI CONNECTION CHECK (no user prompt, no data loading)
# =========================================================================
try:
    check_anki_connect()
except Exception as e:
    print(ANKI_ERRORS['connection'])
    print(ANKI_ERRORS['setup_instructions'])
    sys.exit(1)

# =========================================================================
# STEP 3: USER INTERACTION & INPUT VALIDATION
# =========================================================================

# Now prompt the user for the deck name (if needed)
deck_name = get_deck_name()
create_deck_if_not_exists(deck_name)

# Get sentence from clipboard
sentence = get_clean_sentence_from_clipboard()

# Get focus word from user
word = input("🔤 Введи слово, яке хочеш вивчати: ").strip().lower()

# Detect and confirm part of speech
detected_pos = detect_pos_from_context(word, sentence) or "noun"
pos = input(f"📝 Частина мови [{detected_pos}] [Натисни Enter для підтвердження або поміняй (noun/verb/adjective/adverb)]: ").strip().lower()
if not pos:
    pos = detected_pos

# ============================================================================
# STEP 4: DATA GATHERING & PROCESSING
# ============================================================================

# Load CEFR/frequency data for 172782 words
load_cefr_frequency_data()

# Fetch dictionary data with confirmed POS
dictionary_data = fetch_word_data(word, pos)
if not dictionary_data:
    exit(1)

# Highlight focus word in sentence
pos_map = {'noun': 'n', 'verb': 'v', 'adjective': 'a', 'adverb': 'r'}
highlighted = highlight_focus_word(sentence, word, pos=pos_map.get(pos, 'n'))

# Fetch and select image
print("\n🔍 Пошук відповідних зображень...")
images = fetch_pexels_images(word)
if images:
    print(f"Знайдено {len(images)} зображень. Відкриваю попередній перегляд у браузері...")
    image_url = select_image(images, word)
    if image_url:
        print("✅ Зображення успішно вибрано.")
    else:
        print("⚠️ Зображення не вибрано. Продовжую без зображення.")
else:
    print("⚠️ Зображень не знайдено. Продовжую без зображення.")
    image_url = ""

# Generate audio files
word_audio_ref, word_audio_data = generate_tts_base64(word, word)
if word_audio_ref is None or word_audio_data is None:
    print(TTS_ERRORS["skip_card"])
    sys.exit(1)

sentence_audio_ref, sentence_audio_data = generate_tts_base64(sentence, f"sentence_{word}")
if sentence_audio_ref is None or sentence_audio_data is None:
    print(TTS_ERRORS["skip_card"])
    sys.exit(1)

# Get irregular verb forms
forms = get_irregular_forms(word)
if forms:
    irregular_forms_field = " - ".join(forms)  # Наприклад, "flee - fled - fled"
else:
    irregular_forms_field = ""

# Get Ukrainian translation
print("\n📝 Введіть український переклад:")
translation_ua = input("🔤 Введіть слова перекладу (розділяйте комами): ").strip()

# Format full dictionary entry
dictionary_entry = format_dictionary_entry(dictionary_data["dictionary_api_response"])

# ============================================================================
# STEP 5: MEDIA FILE UPLOAD
# ============================================================================

# Upload audio files to Anki
if word_audio_data:
    send_media_file(f"tts_{word}.mp3", word_audio_data)

if sentence_audio_data:
    send_media_file(f"tts_sentence_{word}.mp3", sentence_audio_data)

# ============================================================================
# STEP 6: CARD CONSTRUCTION & SUBMISSION
# ============================================================================

# Build note structure
note = {
    "deckName": deck_name,
    "modelName": MODEL_NAME,
    "fields": {
        "Word": word,
        "Front": "",
        "Back": "",
        "Image": f'<div style="width: 250px; height: 250px; margin: 0 auto; overflow: hidden; display: flex; align-items: center; justify-content: center;"><img src="{image_url}" style="width: 100%; height: 100%; object-fit: contain;"></div>' if image_url else "",
        "Definition": dictionary_data["definition"],
        "Synonyms": dictionary_data["synonyms"],
        "Antonyms": dictionary_data["antonyms"],
        "Related": dictionary_data["related"],
        "Similar": dictionary_data["similar"],
        "Sentence": highlighted,
        "Sentence_Repeated": sentence,
        "Sentence_Audio": sentence_audio_ref,
        "Word_Audio": word_audio_ref,
        "Irregular_Forms": irregular_forms_field,
        "Dictionary_Entry": dictionary_entry,
        "Translation_UA": translation_ua,
        "Tags": ""
    },
    "options": {
        "allowDuplicate": False
    },
    "tags": []
}

# Submit card to Anki
try:
    result = add_note(note)
    print(f"✅ Картку додано: ID = {result['result']}")
except Exception as e:
    print(str(e))
