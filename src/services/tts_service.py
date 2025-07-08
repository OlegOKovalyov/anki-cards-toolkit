"""A service for generating text-to-speech audio using Google TTS."""

import base64
from io import BytesIO
from gtts import gTTS
import requests
from docs.messages import TTS_ERRORS

def generate_tts_base64(text: str, filename_prefix: str) -> tuple[str | None, str | None]:
    """
    Generates base64-encoded audio from text using Google TTS.

    Args:
        text (str): The text to convert to speech.
        filename_prefix (str): A prefix (like the word being studied) to create a unique filename.

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
        print(TTS_ERRORS['connection'])
        return None, None
    except Exception as e:
        print(TTS_ERRORS['generation'].format(error=str(e)))
        return None, None 