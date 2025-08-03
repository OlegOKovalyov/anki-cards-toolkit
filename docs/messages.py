# STEP 1: INITIALIZATION & CONFIGURATION
INITIALIZATION_CONFIGURATION = {
    "config_error": "\n❌ Config error: {error}",
    "config_fix": "Please fix the configuration and try again.",
    "missing_cefr_file": "The required data file 'data/merged_cefr_frequency.csv' is missing. Please ensure it exists in the data/ directory.",
    "missing_irregular_verbs_file": "The required data file 'data/irregular_verbs.py' is missing. Please ensure it exists in the data/ directory.",
    "deck_name_missing": "Deck name is missing. Please provide a deck name in your configuration.",
    "deck_name_invalid_whitespace": "Deck name cannot be empty or contain only whitespace.",
    "deck_name_invalid_characters": "Deck name contains forbidden characters. Please avoid using /, \\, *, ?, \", <, >, |.",
    "model_name_invalid": "Model name must be exactly 'VocabCard_English_UA'.",
    "pexels_api_key_invalid": "PEXELS_API_KEY must be exactly 56 characters long and contain no spaces.",
    "big_huge_api_key_invalid": "BIG_HUGE_API_KEY must be exactly 32 characters long and contain no spaces.",
    "anki_connect_url_invalid": "ANKI_CONNECT_URL must be exactly 'http://localhost:8765'.",
    "config_file_invalid": "CONFIG_FILE must be exactly 'last_deck.txt'.",
    "language_prompt": "Please choose your language:\n{options}\n> ",
    "language_invalid_choice_dynamic": "❌ Invalid choice. Please enter a valid number from the list: ",
    "language_set": "✅ Language set to: {language}"
}

# STEP 2: ANKI CONNECTION CHECK
ANKI_CONNECTION_CHECK = {
    "connection_error": "❌ Failed to connect to Anki",
    "setup_instructions": """
📝 Make sure that:
   1. Anki is running
   2. The AnkiConnect add-on is installed
   3. AnkiConnect is configured to use port 8765""",
    "add_card_connection_error": "❌ Failed to add the card: no connection to Anki",
    "add_card_generic_error": "❌ Error while adding the card: {error}"
}

# STEP 3: USER INTERACTION & INPUT VALIDATION
USER_INTERACTION_INPUT_VALIDATION = {
    # Deck name prompt
    "deck_name_prompt": "Enter deck name [{last_deck}]: ",
    # Deck creation errors
    "deck_creation_error": "⚠️ Error creating deck: {error}",
    "deck_creation_timeout": "❌ Timeout while waiting for response from Anki",
    "deck_creation_request_error": "❌ Request error while communicating with Anki: {error}",
    "deck_creation_unexpected_error": "❌ Unexpected error while creating deck: {error}",
    # Clipboard/sentence prompts
    "clipboard_sentence_prompt": "📋 Copied sentence:\n{clipboard_sentence}\nIs it correct? [Press Enter to confirm or type again]: ",
    "clipboard_empty_prompt": "Clipboard is empty. Please enter the sentence here: ",
    "sentence_not_provided": "No sentence was provided. There may be an issue with the clipboard or your input. Exiting.",
    # POS detection error
    "pos_detection_error": "⚠️ Error detecting part of speech: {error}",
    # Word and POS prompts
    "word_prompt": "🔤 Enter the word you want to study: ",
    "pos_prompt": "📝 Part of speech [{detected_pos}] [Press Enter to confirm or change (noun/verb/adjective/adverb)]: ",
    "about_message": "🃏 AnkiCardsToolkit v{version} by Oleg Kovalyov - Create Anki flashcard with word from your sentence\n",
    "duplicate_word_warning": "⚠️ This word is already present in your Anki collection. A new card cannot be created.\n👉 Please enter a different word, or press Enter to exit.",
    "duplicate_word_prompt": "Enter a different word: "
}

# STEP 4: DATA GATHERING & PROCESSING
DATA_GATHERING_PROCESSING = {
    "translation_intro": "\n📝 Enter the Ukrainian translation:",
    "translation_prompt": "🔤 Enter translated words (separate with commas): ",
    # CEFR/frequency data loading
    "cefr_loaded": "✅ Loaded CEFR/frequency data for {count} words",
    "cefr_load_error": "⚠️ Could not load CEFR/frequency data: {error}",
    # Dictionary fetch/format
    "dict_fetch_error": "❌ Failed to fetch dictionary data for '{word}'.",
    "dict_format_error": "❌ Error formatting dictionary entry: {error}",
    "dict_format_invalid": "Invalid dictionary data.",
    "dict_format_generic": "Error formatting dictionary entry.",
    "dict_invalid_format": "❌ Invalid dictionary data format.",
    "dict_pos_not_found": "⚠️ Definition for '{requested_pos}' not found. Using the first available one.",
    # Thesaurus
    "thesaurus_key_missing": "❌ BIG_HUGE_API_KEY not found. Please check your .env file.",
    "thesaurus_query": "\n🔍 Querying Big Huge Thesaurus for '{word}'...",
    "thesaurus_success": "✅ Received response from Big Huge Thesaurus",
    # Image selection
    "no_images_found": "No images found.",
    "image_number_prompt": "\n🔢 Enter image number (1-{max}) or press Enter to skip: ",
    "image_invalid_number": "❌ Please enter a number between 1 and {max}",
    "image_invalid_input": "❌ Please enter a valid number",
    "image_searching": "\n🔍 Searching for suitable images...",
    "image_none_continue": "⚠️ No images found. Continuing without an image.",
    "image_selected": "✅ Image successfully selected.",
    "image_skip_notice": "⚠️ No image selected. Continuing without an image.",
    "image_default_selected": "✅ First image selected by default.",
    "image_out_of_range": "⚠️ Number out of range. First image selected by default.",
    "image_number_full_prompt": "❌ Please enter a number between 1 and {max}, press Enter for the first one, or Esc to skip."
}

# STEP 4: IMAGE SELECTION MESSAGES
IMAGE_SELECTION_MESSAGES = {
    "no_images_found": "No images found.",
    "prompt_basic": "\n🔢 Enter the image number (1-{count}) or press Enter to skip: ",
    "image_invalid_number": "❌ Please enter a number between 1 and {max}",
    "image_invalid_input": "❌ Please enter a valid number",
    "image_searching": "\n🔍 Searching for relevant images...",
    "image_none_continue": "⚠️ No images found. Continuing without an image.",
    "image_found_count": "Found {count} images. Opening preview in browser...",
    "prompt_range": "\n🔢 Enter a number (1-{count}) or press Enter: ",
    "image_default_selected": "✅ First image selected by default.",
    "image_skip_notice": "⚠️ No image selected. Continuing without an image.",
    "image_selected": "✅ Image successfully selected.",
    "image_out_of_range": "⚠️ Number out of range. First image selected by default.",
    "image_number_full_prompt": "❌ Please enter a number between 1 and {max}, press Enter for the first one, or Esc to skip."
}

# STEP 4: TTS ERRORS
TTS_ERRORS = {
    'connection': "❌ Error: Failed to connect to the TTS service. Please check your internet connection",
    'generation': "❌ Error during TTS generation: {error}",
    'skip_card': "❌ An error occurred while generating audio via gTTS API. Please try again later."
}

# STEP 4: PEXELS ERRORS
PEXELS_ERRORS = {
    "missing_api_key": "❌ PEXELS_API_KEY not found. Please check your .env file.",
    "image_not_found": "⚠️ Failed to fetch image for '{query}' from Pexels."
}

# STEP 5: MEDIA FILE UPLOAD
MEDIA_FILE_UPLOAD = {
    "media_save_error": "⚠️ Error adding {filename}: {error}",
    "media_connection_error": "⚠️ Failed to save {filename}: no connection to Anki",
    "media_timeout_error": "⚠️ Failed to save {filename}: request timed out",
    "media_request_error": "⚠️ Request error while saving {filename}: {error}",
    "media_unexpected_error": "⚠️ Unexpected error while saving {filename}: {error}",
    "file_saved": "📁 File {filename} saved"
}

# STEP 6: CARD CONSTRUCTION & SUBMISSION
CARD_CONSTRUCTION_SUBMISSION = {
    "card_added": "✅ Card added: ID = {card_id}",
    "exception": "{error}",
    "note_add_error": "❌ Error adding card: {error}"
}

# DEVELOPER / SYSTEM MESSAGES
DEVELOPER_NOTES = {
    "nltk_download_failure": "⚠️ Could not download NLTK data for testing: {error}"
}

# GENERAL ERRORS (used by API client and other modules)
GENERAL_ERRORS = {
    'unexpected': "❌ Unexpected error: {error}",
    'invalid_input': "❌ Invalid input: {error}",
    'file_not_found': "❌ File not found: {filename}",
    'permission_denied': "❌ Permission denied for file: {filename}",
    'http_error': "❌ HTTP error: {error}",
    'connection': "❌ Connection error: please check your internet connection",
    'timeout': "❌ Request timed out",
    'request_error': "❌ Request error: {error}",
    'auth': "❌ Authorization error",
    'rate_limit': "❌ Request rate limit exceeded"
}
