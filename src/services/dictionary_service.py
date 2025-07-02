"""A service for fetching and consolidating data from dictionary and thesaurus APIs."""

import os
import csv
from src.utils.api_client import get_api_data

BIG_HUGE_API_KEY = os.getenv("BIG_HUGE_API_KEY")

# Load CEFR and frequency data at startup
CEFR_FREQUENCY_DATA = {}

def load_cefr_frequency_data():
    """Load CEFR and frequency data from CSV file"""
    cefr_freq_data = {}
    csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'merged_cefr_frequency.csv')
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                word = row['Word'].strip().lower()
                cefr = row['CEFR'].strip().upper()
                freq = row['Frequency'].strip()
                cefr_freq_data[word] = {'cefr': cefr, 'frequency': freq}
        print(f"✅ Loaded CEFR/frequency data for {len(cefr_freq_data)} words")
        CEFR_FREQUENCY_DATA.update(cefr_freq_data)
        return cefr_freq_data
    except Exception as e:
        print(f"⚠️ Could not load CEFR/frequency data: {str(e)}")
        CEFR_FREQUENCY_DATA.clear()
        return {}

def format_dictionary_entry(data):
    """
    Format dictionary data into a clean HTML structure for Anki card with dark theme styling.
    """
    try:
        html = []
        
        # Add CSS styles
        html.append("""
<style>
.dictionary-entry {
    text-align: left;
    line-height: 1.3;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}
.word-header {
    display: flex;
    align-items: center;
    gap: 15px;
    margin-bottom: 10px;
    justify-content: space-between;
    width: 100%;
}
.word-info {
    display: flex;
    align-items: center;
    gap: 15px;
}
.word {
    font-size: 1.5em;
    color: #ffa94d;
    font-weight: 600;
}
.cefr-freq {
    color: #868e96;
    font-size: 0.9em;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.phonetic {
    color: #adb5bd;
    font-size: 1.1em;
}
.pos {
    color: #868e96;
    font-size: 0.9em;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-top: 14px;
    margin-bottom: 4px;
}
.definition-block {
    margin-left: 20px;
    margin-bottom: 6px;
}
.definition {
    font-size: 0.85em;
    color: #ced4da;
    line-height: 1.2;
}
.example {
    margin-left: 20px;
    margin-top: 2px;
    color: #d4c4a1;
    font-style: italic;
    font-size: 0.8em;
}
.word-relations {
    margin-left: 20px;
    margin-top: 2px;
    font-size: 0.75em;
}
.synonyms {
    color: #74c0fc;
}
.antonyms {
    color: #ffa8a8;
}
.additional-relations {
    margin-left: 20px;
    margin-top: 4px;
    font-size: 0.75em;
    font-style: italic;
}
</style>
""")
        
        html.append('<div class="dictionary-entry">')
        
        # Add word, CEFR/frequency, and phonetics in header
        word = data.get("word", "").lower()
        phonetics = data.get("phonetics", [])
        phonetic_text = next((p.get("text", "") for p in phonetics if p.get("text")), "")
        
        # Get CEFR and frequency data
        cefr_freq = CEFR_FREQUENCY_DATA.get(word, {})
        cefr = cefr_freq.get('cefr', '')
        freq = cefr_freq.get('frequency', '')
        
        # Format CEFR and frequency info
        cefr_freq_text = ''
        if cefr and cefr != '?':
            cefr_freq_text = f'{cefr} ({freq})'
        elif freq:
            cefr_freq_text = f'({freq})'
        
        html.append('<div class="word-header">')
        html.append('<div class="word-info">')
        if word:
            html.append(f'<span class="word">{word}</span>')
        if phonetic_text:
            html.append(f'<span class="phonetic">{phonetic_text}</span>')
        html.append('</div>')
        if cefr_freq_text:
            html.append(f'<span class="cefr-freq">{cefr_freq_text}</span>')
        html.append('</div>')
        
        # Process each meaning
        meanings = data.get("meanings", [])
        if not meanings:
            html.append('</div>')
            return "\n".join(html)
        
        for meaning in meanings:
            pos = meaning.get("partOfSpeech", "")
            definitions = meaning.get("definitions", [])
            
            if pos:
                html.append(f'<div class="pos">{pos}</div>')
            
            if definitions:
                for i, def_item in enumerate(definitions, 1):
                    html.append('<div class="definition-block">')
                    
                    # Definition
                    definition = def_item.get("definition", "")
                    if definition:
                        html.append(f'<div class="definition"><strong>{i}.</strong> {definition}</div>')
                    
                    # Example
                    example = def_item.get("example", "")
                    if example:
                        html.append(f'<div class="example">"{example}"</div>')
                    
                    # Definition-specific synonyms
                    def_synonyms = def_item.get("synonyms", [])
                    if def_synonyms:
                        html.append(f'<div class="word-relations synonyms">• Synonyms: {", ".join(def_synonyms)}</div>')
                    
                    # Definition-specific antonyms
                    def_antonyms = def_item.get("antonyms", [])
                    if def_antonyms:
                        html.append(f'<div class="word-relations antonyms">• Antonyms: {", ".join(def_antonyms)}</div>')
                    
                    html.append('</div>')
            
            # Part of speech level synonyms/antonyms
            pos_synonyms = meaning.get("synonyms", [])
            pos_antonyms = meaning.get("antonyms", [])
            
            if pos_synonyms:
                html.append(f'<div class="additional-relations synonyms">Additional synonyms: {", ".join(pos_synonyms)}</div>')
            if pos_antonyms:
                html.append(f'<div class="additional-relations antonyms">Additional antonyms: {", ".join(pos_antonyms)}</div>')
        
        html.append('</div>')
        return "\n".join(html)
        
    except Exception as e:
        print(f"❌ Error formatting dictionary entry: {str(e)}")
        return "Error formatting dictionary entry."

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