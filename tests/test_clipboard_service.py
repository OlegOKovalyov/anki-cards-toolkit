import pytest
import pyperclip
from src.services.clipboard_service import get_clean_sentence_from_clipboard

def test_get_clean_sentence_from_clipboard_basic():
    # Simulate copying a sentence with various formatting issues
    raw = "“Hello,   world!”  This is a test.\nNew line.  'Quote' ∙ End."
    pyperclip.copy(raw)
    cleaned = get_clean_sentence_from_clipboard()
    expected = '"Hello, world!" This is a test. New line. \'Quote\' - End.'
    assert cleaned == expected

def test_get_clean_sentence_from_clipboard_empty():
    pyperclip.copy("")
    cleaned = get_clean_sentence_from_clipboard()
    assert cleaned == "" 