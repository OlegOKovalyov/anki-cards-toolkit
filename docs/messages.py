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
    "config_file_invalid": "CONFIG_FILE must be exactly 'last_deck.txt'."
}

# STEP 2: ANKI CONNECTION CHECK
ANKI_CONNECTION_CHECK = {
    "connection_error": "❌ Не вдалося підключитися до Anki",
    "setup_instructions": """
📝 Переконайтеся, що:
   1. Anki запущено
   2. Встановлено додаток AnkiConnect
   3. AnkiConnect налаштовано на порт 8765""",
    "add_card_connection_error": "❌ Не вдалося додати картку: немає зʼєднання з Anki",
    "add_card_generic_error": "❌ Помилка при додаванні картки: {error}"
}

# STEP 3: USER INTERACTION & INPUT VALIDATION
USER_INTERACTION_INPUT_VALIDATION = {
    # Deck name prompt
    "deck_name_prompt": "Введіть назву колоди [{last_deck}]: ",
    # Deck creation errors
    "deck_creation_error": "⚠️ Помилка створення колоди: {error}",
    "deck_creation_timeout": "❌ Перевищено час очікування відповіді від Anki",
    "deck_creation_request_error": "❌ Помилка запиту до Anki: {error}",
    "deck_creation_unexpected_error": "❌ Неочікувана помилка при створенні колоди: {error}",
    # Clipboard/sentence prompts
    "clipboard_sentence_prompt": "📋 Скопійоване речення:\n{clipboard_sentence}\nВсе вірно? [Натисніть Enter при згоді або введіть заново]: ",
    "clipboard_empty_prompt": "Буфер обміну порожній. Будь ласка, введіть речення тут: ",
    "sentence_not_provided": "Речення не було надано. Можливо, виникла проблема з буфером обміну або вашим введеним даних. Вихід.",
    # POS detection error
    "pos_detection_error": "⚠️ Помилка при визначенні частини мови: {error}",
    # Word and POS prompts (from user_messages.py)
    "word_prompt": "🔤 Введи слово, яке хочеш вивчати: ",
    "pos_prompt": "📝 Частина мови [{detected_pos}] [Натисни Enter для підтвердження або поміняй (noun/verb/adjective/adverb)]: "
}

# STEP 4: DATA GATHERING & PROCESSING
DATA_GATHERING_PROCESSING = {
    "translation_intro": "\n📝 Введіть український переклад:",
    "translation_prompt": "🔤 Введіть слова перекладу (розділяйте комами): "
}

# STEP 5: MEDIA FILE UPLOAD
MEDIA_FILE_UPLOAD = {
    # No direct user messages in this step currently
}

# STEP 6: CARD CONSTRUCTION & SUBMISSION
CARD_CONSTRUCTION_SUBMISSION = {
    "card_added": "✅ Картку додано: ID = {card_id}",
    "exception": "{error}"
}

# DEVELOPER / SYSTEM MESSAGES
DEVELOPER_NOTES = {
    "nltk_download_failure": "⚠️ Could not download NLTK data for testing: {error}"
} 