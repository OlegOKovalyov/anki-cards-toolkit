import pyperclip
import re

def get_clean_sentence_from_clipboard():
    """
    Reads the clipboard content and cleans the sentence by:
      - Removing \n and \r
      - Replacing curly double quotes (“ and ”) with straight ones ("),
      - Replacing curly single quotes (‘ and ’) with straight ones ('),
      - Replacing the middle dot (∙) with a dash (-)
    Returns the cleaned sentence as a string.
    """
    sentence = pyperclip.paste()
    # Remove hyphenated line breaks (e.g., generos-\nity → generosity)
    sentence = re.sub(r'-\s*\n\s*', '', sentence)
    # Remove all line breaks
    sentence = re.sub(r'\s*\n\s*', ' ', sentence)
    # Remove extra spaces before punctuation
    sentence = re.sub(r'\s+([.,:;!?])', r'\1', sentence)
    # Replace multiple spaces with one
    sentence = re.sub(r'\s{2,}', ' ', sentence)
    # Replace curly double quotes with straight quotes
    sentence = sentence.replace('“', '"').replace('”', '"')
    # Replace curly single quotes with straight quotes
    sentence = sentence.replace('‘', "'").replace('’', "'")
    # Replace middle dot with dash
    sentence = sentence.replace('∙', '-')
    # Remove carriage returns
    sentence = sentence.replace('\r', '')
    return sentence.strip() 