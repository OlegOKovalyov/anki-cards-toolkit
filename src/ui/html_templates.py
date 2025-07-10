from src.services.cefr_data import CEFR_FREQUENCY_DATA
import os

# Load dictionary CSS at runtime
CSS_PATH = os.path.join(os.path.dirname(__file__), "css", "dictionary.css")
with open(CSS_PATH, encoding="utf-8") as f:
    DICTIONARY_CSS = f"<style>\n{f.read()}\n</style>"


def render_dictionary_html(dictionary_data: dict) -> str:
    """
    Render dictionary data as HTML for the Anki card, using DICTIONARY_CSS for styling.
    Accepts either a list (multi-entry) or a single dict (legacy/single-entry).
    """
    if isinstance(dictionary_data, dict):
        entries = [dictionary_data]
    elif isinstance(dictionary_data, list):
        entries = dictionary_data
    else:
        return "Invalid dictionary data format."

    html = [DICTIONARY_CSS]
    html.append('<div class="dictionary-entry">')

    # Use the first entry for word and phonetic info
    first_entry = entries[0] if entries else {}
    word = first_entry.get("word", "").lower()
    phonetics = first_entry.get("phonetics", [])
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

    # Group all meanings by partOfSpeech across all entries
    pos_groups = {}
    for entry in entries:
        for meaning in entry.get("meanings", []):
            pos = meaning.get("partOfSpeech", "")
            if not pos:
                continue
            if pos not in pos_groups:
                pos_groups[pos] = []
            pos_groups[pos].append(meaning)

    if not pos_groups:
        html.append('</div>')
        return "\n".join(html)

    # For each part of speech, aggregate definitions from all entries
    for pos, meanings in pos_groups.items():
        html.append(f'<div class="pos">{pos}</div>')
        def_counter = 1
        for meaning in meanings:
            definitions = meaning.get("definitions", [])
            for def_item in definitions:
                html.append('<div class="definition-block">')
                definition = def_item.get("definition", "")
                if definition:
                    html.append(f'<div class="definition"><strong>{def_counter}.</strong> {definition}</div>')
                    def_counter += 1
                example = def_item.get("example", "")
                if example:
                    html.append(f'<div class="example">"{example}"</div>')
                def_synonyms = def_item.get("synonyms", [])
                if def_synonyms:
                    html.append(f'<div class="word-relations synonyms">• Synonyms: {", ".join(def_synonyms)}</div>')
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