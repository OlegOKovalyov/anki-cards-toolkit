from src.linguistics.pos import detect_pos_from_context
from docs.messages import USER_INTERACTION_INPUT_VALIDATION

def get_confirmed_pos(word, sentence) -> str:
    """
    Detects the part of speech for a word in context and asks the user to confirm or override it.
    Returns the confirmed part of speech as a string.
    """
    detected = detect_pos_from_context(word, sentence) or "noun"
    user_input = input(USER_INTERACTION_INPUT_VALIDATION["pos_prompt"].format(detected_pos=detected)).strip().lower()
    return user_input if user_input else detected 