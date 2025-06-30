"""
Centralized error messages for the Anki Cards Toolkit.
All messages are in Ukrainian to match the application's language.
"""

# API Errors
PEXELS_API_ERRORS = {
    'auth': "❌ Помилка авторизації Pexels API: недійсний API ключ",
    'rate_limit': "❌ Помилка Pexels API: перевищено ліміт запитів",
    'connection': "❌ Помилка підключення до Pexels API: перевірте підключення до інтернету",
    'timeout': "❌ Помилка Pexels API: перевищено час очікування",
    'request': "❌ Помилка запиту до Pexels API: {error}",
    'unexpected': "❌ Неочікувана помилка при отриманні зображень: {error}"
}

# Anki Errors
ANKI_ERRORS = {
    'connection': "❌ Не вдалося підключитися до Anki",
    'timeout': "❌ Перевищено час очікування відповіді від Anki",
    'deck_creation': "⚠️ Помилка створення колоди: {error}",
    'media_save_error': "⚠️ Помилка додавання {filename}: {error}",
    'media_connection_error': "⚠️ Не вдалося зберегти {filename}: немає зʼєднання з Anki",
    'media_timeout_error': "⚠️ Не вдалося зберегти {filename}: перевищено час очікування",
    'media_request_error': "⚠️ Помилка запиту при збереженні {filename}: {error}",
    'media_unexpected_error': "⚠️ Неочікувана помилка при збереженні {filename}: {error}",
    'note_add': "❌ Помилка додавання картки: {error}",
    'setup_instructions': """
📝 Переконайтеся, що:
   1. Anki запущено
   2. Встановлено додаток AnkiConnect
   3. AnkiConnect налаштовано на порт 8765"""
}

# TTS Errors
TTS_ERRORS = {
    'connection': "❌ Помилка: Не вдалося підключитися до сервісу TTS. Перевірте підключення до інтернету",
    'generation': "❌ Помилка при генерації TTS: {error}",
    'skip_card': "ℹ️ Пропускаємо створення картки через помилку TTS. Спробуйте наступне речення."
}

# Dictionary Errors
DICTIONARY_ERRORS = {
    'word_not_found': "❌ Помилка: слово '{word}' не знайдено у словнику",
    'pos_not_found': "⚠️ Визначення для частини мови '{pos}' не знайдено",
    'unexpected': "❌ Виняток при отриманні даних зі словника: {error}",
    'thesaurus_error': "❌ Помилка Thesaurus API: {error}"
}

# Image Selection Errors
IMAGE_SELECTION_ERRORS = {
    'no_images': "Зображень не знайдено.",
    'invalid_number': "❌ Будь ласка, введіть число від 1 до {max}",
    'invalid_input': "❌ Будь ласка, введіть правильне число",
    'skip_notice': "⚠️ Зображення не вибрано. Продовжую без зображення."
}

# General Errors
GENERAL_ERRORS = {
    'unexpected': "❌ Неочікувана помилка: {error}",
    'invalid_input': "❌ Невірний ввід: {error}",
    'file_not_found': "❌ Файл не знайдено: {filename}",
    'permission_denied': "❌ Відмовлено в доступі до файлу: {filename}"
}

# Success Messages
SUCCESS_MESSAGES = {
    'deck_created': "✅ Колоду створено",
    'card_added': "✅ Картку додано: ID = {card_id}",
    'file_saved': "📁 Файл {filename} збережено",
    'images_found': "✅ Знайдено {count} зображень",
    'image_selected': "✅ Зображення успішно вибрано",
    'thesaurus_data': "✅ Отримано відповідь від Big Huge Thesaurus"
}

DECK_NAME_MISSING = "Deck name is missing. Please provide a deck name in your configuration."
DECK_NAME_INVALID_WHITESPACE = "Deck name cannot be empty or contain only whitespace."
DECK_NAME_INVALID_CHARACTERS = "Deck name contains forbidden characters. Please avoid using /, \\, *, ?, \", <, >, |."

CONFIG_ERRORS = {
    'deck_name_missing': "Deck name is missing. Please provide a deck name in your configuration.",
    'deck_name_invalid_whitespace': "Deck name cannot be empty or contain only whitespace.",
    'deck_name_invalid_characters': "Deck name contains forbidden characters. Please avoid using /, \\, *, ?, \", <, >, |.",
    'model_name_invalid': "Model name must be exactly 'VocabCard_English_UA'.",
    'pexels_api_key_invalid': "PEXELS_API_KEY must be exactly 56 characters long and contain no spaces.",
    'big_huge_api_key_invalid': "BIG_HUGE_API_KEY must be exactly 32 characters long and contain no spaces.",
    'anki_connect_url_invalid': "ANKI_CONNECT_URL must be exactly 'http://localhost:8765'.",
    'config_file_invalid': "CONFIG_FILE must be exactly 'last_deck.txt'."
} 