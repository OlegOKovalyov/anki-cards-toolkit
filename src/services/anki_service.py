import requests
import sys
from src.config import settings
from src.locales.loader import get_message

ANKI_CONNECT_URL = settings.ANKI_CONNECT_URL

def check_anki_connect():
    """Check if AnkiConnect is available. If not, print instructions and exit immediately."""
    try:
        response = requests.get(ANKI_CONNECT_URL)
        return True
    except requests.exceptions.ConnectionError:
        print(get_message("ANKI_CONNECTION_CHECK.connection_error"))
        print(get_message("ANKI_CONNECTION_CHECK.setup_instructions"))
        sys.exit(1)
    except Exception:
        print(get_message("ANKI_CONNECTION_CHECK.connection_error"))
        print(get_message("ANKI_CONNECTION_CHECK.setup_instructions"))
        sys.exit(1)

def add_note(note: dict):
    """
    Sends an addNote request to AnkiConnect.
    Returns the response dict (including note ID if successful).
    Raises an exception if the note could not be added.
    """
    payload = {
        "action": "addNote",
        "version": 6,
        "params": {"note": note}
    }
    try:
        response = requests.post(ANKI_CONNECT_URL, json=payload, timeout=5)
        response.raise_for_status()
        result = response.json()
        if result.get("error") is None:
            return result
        else:
            raise Exception(f"AnkiConnect error: {result['error']}")
    except requests.exceptions.ConnectionError:
        raise Exception(get_message("ANKI_CONNECTION_CHECK.add_card_connection_error"))
    except Exception as e:
        raise Exception(get_message("CARD_CONSTRUCTION_SUBMISSION.note_add_error", error=str(e))) 