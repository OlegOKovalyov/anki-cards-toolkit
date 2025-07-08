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