import os
from src.utils.api_client import get_api_data

BIG_HUGE_API_KEY = os.getenv("BIG_HUGE_API_KEY")

def _fetch_dictionary_api_data(word: str):
    """Fetch raw word data from the DictionaryAPI."""
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    data = get_api_data(url)
    return data[0] if data else None

def _fetch_thesaurus_api_data(word: str):
    """Fetch raw thesaurus data from Big Huge Thesaurus."""
    if not BIG_HUGE_API_KEY:
        print("❌ BIG_HUGE_API_KEY не знайдено. Перевірте ваш .env файл.")
        return None
    url = f"https://words.bighugelabs.com/api/2/{BIG_HUGE_API_KEY}/{word}/json"
    print(f"\n🔍 Запит до Big Huge Thesaurus для слова '{word}'...")
    data = get_api_data(url)
    if data:
        print("✅ Отримано відповідь від Big Huge Thesaurus")
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
    """
    dictionary_data = _fetch_dictionary_api_data(word)
    if not dictionary_data:
        print(f"❌ Не вдалося отримати дані зі словника для '{word}'.")
        return None

    thesaurus_data = _fetch_thesaurus_api_data(word)
    processed_thesaurus = _process_thesaurus_data(thesaurus_data, requested_pos)

    meanings = dictionary_data.get("meanings", [])
    target_meaning = None

    if requested_pos:
        for m in meanings:
            if m.get("partOfSpeech") == requested_pos:
                target_meaning = m
                break
        if not target_meaning:
            print(f"⚠️ Визначення для '{requested_pos}' не знайдено. Використовується перше доступне.")
            target_meaning = meanings[0] if meanings else {}
    else:
        target_meaning = meanings[0] if meanings else {}

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