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
    'media_save': "⚠️ Помилка додавання {filename}: {error}",
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