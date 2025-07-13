"""A service for generating text-to-speech audio using Google TTS."""

import base64
from io import BytesIO
from gtts import gTTS
import requests
from src.locales.loader import get_message
import sys

def generate_tts_base64(text: str, filename_prefix: str, exit_on_error: bool = True) -> tuple[str | None, str | None]:
    """
    Generates base64-encoded audio from text using Google TTS.

    Args:
        text (str): The text to convert to speech.
        filename_prefix (str): A prefix (like the word being studied) to create a unique filename.
        exit_on_error (bool): If True, print error and exit on failure. If False, just return (None, None).

    Returns:
        A tuple containing the Anki sound reference string and the base64-encoded data,
        or (None, None) if an error occurs.
    """
    try:
        tts = gTTS(text)
        buffer = BytesIO()
        tts.write_to_fp(buffer)
        buffer.seek(0)
        encoded_data = base64.b64encode(buffer.read()).decode('utf-8')
        sound_ref = f"[sound:tts_{filename_prefix}.mp3]"
        return sound_ref, encoded_data
    except requests.exceptions.ConnectionError:
        print(get_message("TTS_ERRORS.connection"))
        if exit_on_error:
            print(get_message("TTS_ERRORS.skip_card"))
            sys.exit(1)
        return None, None
    except Exception as e:
        print(get_message("TTS_ERRORS.generation", error=str(e)))
        if exit_on_error:
            print(get_message("TTS_ERRORS.skip_card"))
            sys.exit(1)
        return None, None 