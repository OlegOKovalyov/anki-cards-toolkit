"""A service for uploading media files to AnkiConnect."""

import requests
from src.locales.loader import get_message
from src.config import settings

ANKI_CONNECT_URL = settings.ANKI_CONNECT_URL

def send_media_file(name: str, b64_data: str) -> bool:
    """
    Sends a base64-encoded media file to AnkiConnect.

    Args:
        name (str): The filename for the media.
        b64_data (str): The base64-encoded file content.

    Returns:
        True if the file was sent successfully, False otherwise.
    """
    if not b64_data:
        return False
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
            print(get_message("MEDIA_FILE_UPLOAD.media_save_error", filename=name, error=result['error']))
            return False
        
        print(get_message("MEDIA_FILE_UPLOAD.file_saved", filename=name))
        return True
            
    except requests.exceptions.ConnectionError:
        print(get_message("MEDIA_FILE_UPLOAD.media_connection_error", filename=name))
    except requests.exceptions.Timeout:
        print(get_message("MEDIA_FILE_UPLOAD.media_timeout_error", filename=name))
    except requests.exceptions.RequestException as e:
        print(get_message("MEDIA_FILE_UPLOAD.media_request_error", filename=name, error=str(e)))
    except Exception as e:
        print(get_message("MEDIA_FILE_UPLOAD.media_unexpected_error", filename=name, error=str(e)))
        
    return False 