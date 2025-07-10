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
    "translation_prompt": "🔤 Введіть слова перекладу (розділяйте комами): ",
    # CEFR/frequency data loading
    "cefr_loaded": "✅ Loaded CEFR/frequency data for {count} words",
    "cefr_load_error": "⚠️ Could not load CEFR/frequency data: {error}",
    # Dictionary fetch/format
    "dict_fetch_error": "❌ Не вдалося отримати дані зі словника для '{word}'.",
    "dict_format_error": "❌ Error formatting dictionary entry: {error}",
    "dict_format_invalid": "Invalid dictionary data.",
    "dict_format_generic": "Error formatting dictionary entry.",
    "dict_invalid_format": "❌ Невірний формат даних словника.",
    "dict_pos_not_found": "⚠️ Визначення для '{requested_pos}' не знайдено. Використовується перше доступне.",
    # Thesaurus
    "thesaurus_key_missing": "❌ BIG_HUGE_API_KEY не знайдено. Перевірте ваш .env файл.",
    "thesaurus_query": "\n🔍 Запит до Big Huge Thesaurus для слова '{word}'...",
    "thesaurus_success": "✅ Отримано відповідь від Big Huge Thesaurus",
    # Image selection
    "no_images_found": "Зображень не знайдено.",
    "image_number_prompt": "\n🔢 Введіть номер зображення (1-{max}) або натисніть Enter для пропуску: ",
    "image_invalid_number": "❌ Будь ласка, введіть число від 1 до {max}",
    "image_invalid_input": "❌ Будь ласка, введіть правильне число",
    "image_searching": "\n🔍 Пошук відповідних зображень...",
    "image_none_continue": "⚠️ Зображень не знайдено. Продовжую без зображення.",
    "image_found_count": "Знайдено {count} зображень. Відкриваю попередній перегляд у браузері...",
    "image_selected": "✅ Зображення успішно вибрано.",
    "image_skip_notice": "⚠️ Зображення не вибрано. Продовжую без зображення.",
    "image_default_selected": "✅ Вибрано перше зображення за замовчуванням.",
    "image_out_of_range": "⚠️ Номер поза діапазоном. Вибрано перше зображення за замовчуванням.",
    "image_number_full_prompt": "❌ Будь ласка, введіть число від 1 до {max}, Enter для першого, або Esc для пропуску."
}

# STEP 4: TTS ERRORS
TTS_ERRORS = {
    'connection': "❌ Помилка: Не вдалося підключитися до сервісу TTS. Перевірте підключення до інтернету",
    'generation': "❌ Помилка при генерації TTS: {error}",
    'skip_card': "❌ Сталася помилка під час генерації аудіо через gTTS API. Спробуйте пізніше."
}

# STEP 4: PEXELS ERRORS
PEXELS_ERRORS = {
    "missing_api_key": "❌ PEXELS_API_KEY не знайдено. Перевірте ваш .env файл.",
    "image_not_found": "⚠️ Не вдалося отримати зображення для '{query}' з Pexels."
}

# STEP 5: MEDIA FILE UPLOAD
MEDIA_FILE_UPLOAD = {
    "media_save_error": "⚠️ Помилка додавання {filename}: {error}",
    "media_connection_error": "⚠️ Не вдалося зберегти {filename}: немає зʼєднання з Anki",
    "media_timeout_error": "⚠️ Не вдалося зберегти {filename}: перевищено час очікування",
    "media_request_error": "⚠️ Помилка запиту при збереженні {filename}: {error}",
    "media_unexpected_error": "⚠️ Неочікувана помилка при збереженні {filename}: {error}",
    "file_saved": "📁 Файл {filename} збережено"
}

# STEP 6: CARD CONSTRUCTION & SUBMISSION
CARD_CONSTRUCTION_SUBMISSION = {
    "card_added": "✅ Картку додано: ID = {card_id}",
    "exception": "{error}",
    "note_add_error": "❌ Помилка додавання картки: {error}"
}

# DEVELOPER / SYSTEM MESSAGES
DEVELOPER_NOTES = {
    "nltk_download_failure": "⚠️ Could not download NLTK data for testing: {error}"
}

# GENERAL ERRORS (used by API client and other modules)
GENERAL_ERRORS = {
    'unexpected': "❌ Неочікувана помилка: {error}",
    'invalid_input': "❌ Невірний ввід: {error}",
    'file_not_found': "❌ Файл не знайдено: {filename}",
    'permission_denied': "❌ Відмовлено в доступі до файлу: {filename}",
    'http_error': "❌ HTTP помилка: {error}",
    'connection': "❌ Помилка підключення: перевірте підключення до інтернету",
    'timeout': "❌ Перевищено час очікування",
    'request_error': "❌ Помилка запиту: {error}",
    'auth': "❌ Помилка авторизації",
    'rate_limit': "❌ Перевищено ліміт запитів"
} 