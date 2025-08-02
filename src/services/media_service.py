"""A service for uploading media files to AnkiConnect."""

import os
import shutil
import requests
from src.locales.loader import get_message
from src.config import settings

ANKI_CONNECT_URL = settings.ANKI_CONNECT_URL

def move_old_media_to_trash_if_exists(filename: str) -> None:
    """
    Moves an existing media file to the Anki trash folder before overwriting.
    
    Args:
        filename (str): The name of the file to potentially move to trash.
    """
    # Anki media and trash paths (assuming User 1 profile)
    media_dir = os.path.expanduser("~/.local/share/Anki2/User 1/collection.media")
    trash_dir = os.path.expanduser("~/.local/share/Anki2/User 1/media.trash")
    
    # Check if the file exists in the media directory
    media_file_path = os.path.join(media_dir, filename)
    if os.path.exists(media_file_path):
        # Ensure trash directory exists
        os.makedirs(trash_dir, exist_ok=True)
        
        # Move the file to trash
        trash_file_path = os.path.join(trash_dir, filename)
        try:
            shutil.move(media_file_path, trash_file_path)
        except Exception as e:
            # If moving fails, just log it but don't stop the process
            print(f"Warning: Could not move {filename} to trash: {e}")

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
    
    # Move existing file to trash before overwriting
    move_old_media_to_trash_if_exists(name)
    
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