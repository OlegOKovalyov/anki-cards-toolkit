import pytest
import pyperclip
from src.services.clipboard_service import get_clean_sentence_from_clipboard

def test_get_clean_sentence_from_clipboard_basic(monkeypatch):
    # Simulate copying a sentence with various formatting issues
    raw = "“Hello,   world!”  This is a test.\nNew line.  'Quote' ∙ End."
    pyperclip.copy(raw)
    # Simulate user pressing Enter (accepts clipboard)
    monkeypatch.setattr('builtins.input', lambda prompt: "")
    cleaned = get_clean_sentence_from_clipboard()
    expected = '"Hello, world!" This is a test. New line. \'Quote\' - End.'
    assert cleaned == expected

def test_get_clean_sentence_from_clipboard_empty(monkeypatch):
    pyperclip.copy("")
    # Simulate user pressing Enter (no input) when clipboard is empty
    monkeypatch.setattr('builtins.input', lambda prompt: "")
    with pytest.raises(SystemExit):
        get_clean_sentence_from_clipboard()

def test_clipboard_sentence_user_accepts(monkeypatch):
    pyperclip.copy("Test sentence from clipboard.")
    # Simulate user pressing Enter (accepts clipboard)
    monkeypatch.setattr('builtins.input', lambda prompt: "")
    assert get_clean_sentence_from_clipboard() == "Test sentence from clipboard."

def test_clipboard_sentence_user_replaces(monkeypatch):
    pyperclip.copy("Clipboard sentence.")
    # Simulate user typing a new sentence
    monkeypatch.setattr('builtins.input', lambda prompt: "User replacement.")
    assert get_clean_sentence_from_clipboard() == "User replacement."

def test_empty_clipboard_user_enters_sentence(monkeypatch):
    pyperclip.copy("")
    # Simulate user entering a sentence when clipboard is empty
    monkeypatch.setattr('builtins.input', lambda prompt: "Manual entry.")
    assert get_clean_sentence_from_clipboard() == "Manual entry."

def test_empty_clipboard_user_enters_nothing(monkeypatch):
    pyperclip.copy("")
    # Simulate user pressing Enter (no input) when clipboard is empty
    monkeypatch.setattr('builtins.input', lambda prompt: "")
    with pytest.raises(SystemExit):
        get_clean_sentence_from_clipboard()

def test_get_clean_sentence_removes_timestamps(monkeypatch):
    pyperclip.copy("Well, we're going to give you a similar library\n21:51\nfor at least the next week...")
    monkeypatch.setattr('builtins.input', lambda prompt: "")
    cleaned = get_clean_sentence_from_clipboard()
    expected = "Well, we're going to give you a similar library for at least the next week..."
    assert cleaned == expected 