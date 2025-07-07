"""A service for retrieving and cleaning text from the system clipboard."""

import pyperclip
import re
import sys

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
        # Replace curly double quotes with straight quotes
        sentence = sentence.replace('“', '"').replace('”', '"')
        # Replace curly single quotes with straight quotes
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
        user_input = input(f"📋 Скопійоване речення:\n{clipboard_sentence}\nВсе вірно? [Натисніть Enter при згоді або введіть заново]: ").strip()
        if user_input:
            sentence = user_input.strip()
        else:
            sentence = clipboard_sentence
    else:
        sentence = input("Буфер обміну порожній. Будь ласка, введіть речення тут: ").strip()

    if not sentence:
        print("Речення не було надано. Можливо, виникла проблема з буфером обміну або вашим введеним даних. Вихід.")
        sys.exit(1)

    return sentence 