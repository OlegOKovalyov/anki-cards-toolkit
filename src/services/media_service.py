"""A service for uploading media files to AnkiConnect."""

import os
import requests
from docs.error_messages import ANKI_ERRORS, SUCCESS_MESSAGES

ANKI_CONNECT_URL = os.getenv("ANKI_CONNECT_URL", "http://localhost:8765")

def send_media_file(name: str, b64_data: str) -> bool:
    """
    Sends a base64-encoded media file to AnkiConnect.

    Args:
        name (str): The filename for the media.
        b64_data (str): The base64-encoded file content.

    Returns:
        True if the file was sent successfully, False otherwise.
    """
    payload = {
        "action": "storeMediaFile",
        "version": 6,
        "params": {"filename": name, "data": b64_data}
    }
    try:
        response = requests.post(ANKI_CONNECT_URL, json=payload, timeout=5)
        response.raise_for_status()
        result = response.json()
        
        if result.get("error"):
            print(ANKI_ERRORS['media_save_error'].format(filename=name, error=result['error']))
            return False
        
        print(SUCCESS_MESSAGES['file_saved'].format(filename=name))
        return True
            
    except requests.exceptions.ConnectionError:
        print(ANKI_ERRORS['media_connection_error'].format(filename=name))
    except requests.exceptions.Timeout:
        print(ANKI_ERRORS['media_timeout_error'].format(filename=name))
    except requests.exceptions.RequestException as e:
        print(ANKI_ERRORS['media_request_error'].format(filename=name, error=str(e)))
    except Exception as e:
        print(ANKI_ERRORS['media_unexpected_error'].format(filename=name, error=str(e)))
        
    return False 