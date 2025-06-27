import requests
import sys
import os
from dotenv import load_dotenv

load_dotenv()

ANKI_CONNECT_URL = os.getenv("ANKI_CONNECT_URL", "http://localhost:8765")

def check_anki_connect():
    """Check if AnkiConnect is available. If not, print instructions and exit immediately."""
    try:
        response = requests.get(ANKI_CONNECT_URL)
        return True
    except requests.exceptions.ConnectionError:
        print("\n❌ Помилка: Не вдалося підключитися до Anki.")
        print("Будь ласка, запустіть Anki та спробуйте ще раз.")
        print("📝 Переконайтеся, що:")
        print("   1. Anki запущено")
        print("   2. Встановлено додаток AnkiConnect")
        print("   3. AnkiConnect налаштовано на порт 8765")
        sys.exit(1) 