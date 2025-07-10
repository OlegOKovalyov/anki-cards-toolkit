"""A service for fetching and consolidating data from dictionary and thesaurus APIs."""

import csv
import sys
from src.utils.api_client import get_api_data
from docs.messages import DATA_GATHERING_PROCESSING
from src.ui.html_templates import render_dictionary_html
from src.services.cefr_data import CEFR_FREQUENCY_DATA
from src.config import settings

BIG_HUGE_API_KEY = settings.BIG_HUGE_API_KEY

# Load CEFR and frequency data at startup


def format_dictionary_entry(data):
    """
    Format dictionary data (list of entries) into a clean HTML structure for Anki card with dark theme styling.
    Accepts either a list (multi-entry) or a single dict (legacy/single-entry).
    """
    try:
        return render_dictionary_html(data)
    except Exception as e:
        print(DATA_GATHERING_PROCESSING["dict_format_error"].format(error=str(e)))
        return DATA_GATHERING_PROCESSING["dict_format_generic"]

def _fetch_dictionary_api_data(word: str):
    """Fetch raw word data from the DictionaryAPI."""
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    data = get_api_data(url)
    if not data:
        print(DATA_GATHERING_PROCESSING["dict_fetch_error"].format(word=word))
        return None
    return data

def _fetch_thesaurus_api_data(word: str):
    """Fetch raw thesaurus data from Big Huge Thesaurus."""
    if not BIG_HUGE_API_KEY:
        print(DATA_GATHERING_PROCESSING["thesaurus_key_missing"])
        return None
    url = f"https://words.bighugelabs.com/api/2/{BIG_HUGE_API_KEY}/{word}/json"
    print(DATA_GATHERING_PROCESSING["thesaurus_query"].format(word=word))
    data = get_api_data(url)
    if data:
        print(DATA_GATHERING_PROCESSING["thesaurus_success"])
    return data

def _process_thesaurus_data(thesaurus_data, requested_pos=None):
    """Extracts synonyms, antonyms, etc., from raw thesaurus data for a given POS."""
    if not thesaurus_data:
        return {"synonyms": [], "antonyms": [], "related": [], "similar": []}

    pos_mapping = {"noun": "noun", "verb": "verb", "adjective": "adjective", "adverb": "adverb"}
    all_synonyms, all_antonyms, all_related, all_similar = [], [], [], []

    def extract_from_section(pos_section):
        if isinstance(pos_section, dict):
            all_synonyms.extend(pos_section.get('syn', []))
            all_antonyms.extend(pos_section.get('ant', []))
            all_related.extend(pos_section.get('rel', []))
            all_similar.extend(pos_section.get('sim', []))

    if requested_pos and requested_pos in pos_mapping:
        pos_data = thesaurus_data.get(pos_mapping[requested_pos], {})
        extract_from_section(pos_data)
    else:
        for pos_section in thesaurus_data.values():
            extract_from_section(pos_section)

    def deduplicate(lst):
        seen = set()
        return [x for x in lst if not (x in seen or seen.add(x))]

    return {
        "synonyms": deduplicate(all_synonyms),
        "antonyms": deduplicate(all_antonyms),
        "related": deduplicate(all_related),
        "similar": deduplicate(all_similar)
    }

def format_word_list(words):
    """Format a list of words, returning empty string if no words found."""
    return ", ".join(words) if words else ""

def fetch_word_data(word: str, requested_pos: str = None):
    """
    Fetches and processes word data from both Dictionary and Thesaurus APIs.
    Returns a structured dictionary for the Anki card.
    Exits if no dictionary data is found.
    """
    dictionary_data = _fetch_dictionary_api_data(word)
    if not dictionary_data:
        print(DATA_GATHERING_PROCESSING["dict_fetch_error"].format(word=word))
        sys.exit(1)

    thesaurus_data = _fetch_thesaurus_api_data(word)
    processed_thesaurus = _process_thesaurus_data(thesaurus_data, requested_pos)

    # Handle both list (multi-entry) and dict (legacy) for backward compatibility
    if isinstance(dictionary_data, dict):
        entries = [dictionary_data]
    elif isinstance(dictionary_data, list):
        entries = dictionary_data
    else:
        print(DATA_GATHERING_PROCESSING["dict_invalid_format"])
        return None

    # Aggregate all meanings from all entries
    all_meanings = []
    for entry in entries:
        all_meanings.extend(entry.get("meanings", []))

    target_meaning = None
    if requested_pos:
        for m in all_meanings:
            if m.get("partOfSpeech") == requested_pos:
                target_meaning = m
                break
        if not target_meaning:
            print(DATA_GATHERING_PROCESSING["dict_pos_not_found"].format(requested_pos=requested_pos))
            target_meaning = all_meanings[0] if all_meanings else {}
    else:
        target_meaning = all_meanings[0] if all_meanings else {}

    definitions = target_meaning.get("definitions", [{}])

    return {
        "definition": definitions[0].get("definition", ""),
        "example": definitions[0].get("example", ""),
        "synonyms": format_word_list(processed_thesaurus["synonyms"]),
        "antonyms": format_word_list(processed_thesaurus["antonyms"]),
        "related": format_word_list(processed_thesaurus["related"]),
        "similar": format_word_list(processed_thesaurus["similar"]),
        "partOfSpeech": target_meaning.get("partOfSpeech", ""),
        "dictionary_api_response": dictionary_data
    } 