"""A service for retrieving and cleaning text from the system clipboard."""

import pyperclip
import re
import sys
from src.locales.loader import get_message
from src.cli.colors import cyan

def get_clean_sentence_from_clipboard():
    """
    Improved UX for retrieving a sentence from the clipboard or user input.
    1. Try to get and clean the clipboard content.
    2. If clipboard is not empty, show it and ask for confirmation or replacement.
    3. If clipboard is empty, prompt the user to enter a sentence.
    4. If after both attempts the sentence is still empty, print an error and exit.
    5. Return the final sentence.
    """
    def clean(sentence):
        # Remove hyphenated line breaks (e.g., generos-\nity → generosity)
        sentence = re.sub(r'-\s*\n\s*', '', sentence)
        # Remove all line breaks
        sentence = re.sub(r'\s*\n\s*', ' ', sentence)
        # Remove timestamp patterns like mm:ss or h:mm:ss
        sentence = re.sub(r"\b\d{1,2}:\d{2}(?::\d{2})?\b", '', sentence)
        # Remove extra spaces before punctuation
        sentence = re.sub(r'\s+([.,:;!?])', r'\1', sentence)
        # Restore curly quote cleaning
        sentence = sentence.replace('“', '"').replace('”', '"')
        sentence = sentence.replace('‘', "'").replace('’', "'")
        # Replace middle dot with dash
        sentence = sentence.replace('∙', '-')
        # Remove carriage returns
        sentence = sentence.replace('\r', '')
        # Replace multiple spaces with one (do this last)
        sentence = re.sub(r'\s{2,}', ' ', sentence)
        return sentence.strip()

    clipboard_sentence = clean(pyperclip.paste())

    if clipboard_sentence:
        user_input = input(get_message("USER_INTERACTION_INPUT_VALIDATION.clipboard_sentence_prompt", clipboard_sentence=cyan(clipboard_sentence))).strip()
        if user_input:
            sentence = user_input.strip()
        else:
            sentence = clipboard_sentence
    else:
        sentence = input(get_message("USER_INTERACTION_INPUT_VALIDATION.clipboard_empty_prompt")).strip()

    if not sentence:
        print(get_message("USER_INTERACTION_INPUT_VALIDATION.sentence_not_provided"))
        sys.exit(1)

    return sentence 