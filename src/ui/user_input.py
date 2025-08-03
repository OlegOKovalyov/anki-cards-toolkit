import sys
import os
from src.linguistics.pos import detect_pos_from_context
from src.locales.loader import get_message

def is_duplicate_word(word: str) -> bool:
    """
    Checks if a word already exists in the Anki collection by looking for audio files.
    
    Args:
        word (str): The word to check for duplicates.
        
    Returns:
        bool: True if the word already exists, False otherwise.
    """
    # Check for the existence of tts_sentence_{word}.mp3 in Anki media directory
    media_dir = os.path.expanduser("~/.local/share/Anki2/User 1/collection.media")
    audio_file = os.path.join(media_dir, f"tts_sentence_{word}.mp3")
    
    return os.path.exists(audio_file)

def get_confirmed_pos(word, sentence) -> str:
    """
    Detects the part of speech for a word in context and asks the user to confirm or override it.
    Also checks for duplicate words and prompts for a different word if needed.
    Returns the confirmed part of speech as a string.
    """
    # Check for duplicate word first
    while is_duplicate_word(word):
        print(get_message("USER_INTERACTION_INPUT_VALIDATION.duplicate_word_warning"))
        new_word = input(get_message("USER_INTERACTION_INPUT_VALIDATION.duplicate_word_prompt")).strip().lower()
        
        if not new_word:
            print("Exiting...")
            sys.exit(0)
        
        word = new_word
    
    # Proceed with POS detection for the valid word
    detected = detect_pos_from_context(word, sentence) or "noun"
    user_input = input(get_message("USER_INTERACTION_INPUT_VALIDATION.pos_prompt", detected_pos=detected)).strip().lower()
    return user_input if user_input else detected 