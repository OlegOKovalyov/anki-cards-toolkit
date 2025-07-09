import sys
from dotenv import load_dotenv
from src.utils.config_builder import config_build, get_default_deck_name
from docs.messages import (
    USER_INTERACTION_INPUT_VALIDATION,
    DATA_GATHERING_PROCESSING
)
from src.services.clipboard_service import get_clean_sentence_from_clipboard
from src.linguistics.pos import detect_pos_from_context, get_irregular_forms
from src.utils.highlight import highlight_focus_word
from src.services.dictionary_service import (
    fetch_word_data,
    format_dictionary_entry
)
from src.services.tts_service import generate_tts_base64
from src.services.media_service import send_media_file
from src.ui.image_selector import select_image_for_card
from src.services.anki_service import check_anki_connect, add_note
from src.services.deck_service import get_deck_name, create_deck_if_not_exists
from src.utils.validation import validate_config
from src.utils.note_builder import build_anki_note
from src.utils.note_builder import submit_note_to_anki
from src.ui.user_input import get_confirmed_pos

# ============================================================================
# STEP 1: INITIALIZATION & CONFIGURATION
# ============================================================================

# Load .env file
load_dotenv(override=True)

# ===== STRICT EARLY CONFIG VALIDATION (no user prompt, no data loading) =====
config = config_build()

# Read deck name from last_deck.txt or .env, but do NOT prompt the user before validation
default_deck_name = get_default_deck_name(config)

validate_config(config)

# =========================================================================
# STEP 2: ANKI CONNECTION CHECK (no user prompt, no data loading)
# =========================================================================
check_anki_connect()

# =========================================================================
# STEP 3: USER INTERACTION & INPUT VALIDATION
# =========================================================================

# Now prompt the user for the deck name (if needed)
deck_name = get_deck_name()
create_deck_if_not_exists(deck_name)

# Get sentence from clipboard
sentence = get_clean_sentence_from_clipboard()

# Get focus word from user
word = input(USER_INTERACTION_INPUT_VALIDATION["word_prompt"]).strip().lower()

# Detect and confirm part of speech
pos = get_confirmed_pos(word, sentence)

# ============================================================================
# STEP 4: DATA GATHERING & PROCESSING
# ============================================================================

# Load CEFR/frequency data for 172782 words


# Fetch dictionary data with confirmed POS
dictionary_data = fetch_word_data(word, pos)

# Highlight focus word in sentence
pos_map = {'noun': 'n', 'verb': 'v', 'adjective': 'a', 'adverb': 'r'}
highlighted = highlight_focus_word(sentence, word, pos=pos_map.get(pos, 'n'))

# Fetch and select image
image_url = select_image_for_card(word)

# Generate audio files
word_audio_ref, word_audio_data = generate_tts_base64(word, word)

sentence_audio_ref, sentence_audio_data = generate_tts_base64(sentence, f"sentence_{word}")

# Get irregular verb forms
irregular_forms_field = get_irregular_forms(word)

# Get Ukrainian translation
print(DATA_GATHERING_PROCESSING["translation_intro"])
translation_ua = input(DATA_GATHERING_PROCESSING["translation_prompt"]).strip()

# Format full dictionary entry
dictionary_entry = format_dictionary_entry(dictionary_data["dictionary_api_response"])

# ============================================================================
# STEP 5: MEDIA FILE UPLOAD
# ============================================================================

# Upload audio files to Anki
send_media_file(f"tts_{word}.mp3", word_audio_data)
send_media_file(f"tts_sentence_{word}.mp3", sentence_audio_data)

# ============================================================================
# STEP 6: CARD CONSTRUCTION & SUBMISSION
# ============================================================================

# Build card data dictionary
card_data = {
    "word": word,
    "sentence": sentence,
    "highlighted": highlighted,
    "image_url": image_url,
    "dictionary_data": dictionary_data,
    "sentence_audio_ref": sentence_audio_ref,
    "word_audio_ref": word_audio_ref,
    "irregular_forms_field": irregular_forms_field,
    "dictionary_entry": dictionary_entry,
    "translation_ua": translation_ua,
    "config": config,
    "deck_name": deck_name
}

# Submit card to Anki
submit_note_to_anki(**card_data)
