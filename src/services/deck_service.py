import os
import requests
from dotenv import load_dotenv

load_dotenv()

CONFIG_FILE = os.getenv("CONFIG_FILE")  # last_deck.txt
ANKI_CONNECT_URL = os.getenv("ANKI_CONNECT_URL", "http://localhost:8765")

def load_last_deck():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return f.read().strip()
    return "Default"

def save_last_deck(deck_name):
    with open(CONFIG_FILE, "w") as f:
        f.write(deck_name.strip())

def get_deck_name():
    last_deck = load_last_deck()
    user_input = input(f"Введіть назву колоди [{last_deck}]: ").strip()
    deck = user_input if user_input else last_deck
    save_last_deck(deck)
    return deck

def create_deck_if_not_exists(deck_name):
    """Create a new deck in Anki if it doesn't exist"""
    payload = {
        "action": "createDeck",
        "version": 6,
        "params": {"deck": deck_name}
    }
    try:
        response = requests.post(ANKI_CONNECT_URL, json=payload, timeout=5)
        response.raise_for_status()  # Raise exception for bad status codes
        result = response.json()
        if result.get("error"):
            print(f"⚠️ Помилка створення колоди: {result['error']}")
            return False
        return True
    except requests.exceptions.ConnectionError:
        # Do not print error here; already handled at startup
        return False
    except requests.exceptions.Timeout:
        print("❌ Перевищено час очікування відповіді від Anki")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Помилка запиту до Anki: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Неочікувана помилка при створенні колоди: {str(e)}")
        return False 