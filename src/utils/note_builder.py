from src.services.anki_service import add_note
from docs.messages import CARD_CONSTRUCTION_SUBMISSION

def build_anki_note(
    word: str,
    sentence: str,
    highlighted: str,
    image_url: str,
    dictionary_data: dict,
    sentence_audio_ref: str,
    word_audio_ref: str,
    irregular_forms_field: str,
    dictionary_entry: str,
    translation_ua: str,
    config: dict,
    deck_name: str
) -> dict:
    """
    Build the Anki note dictionary for submission to AnkiConnect.
    All field names and HTML formatting are preserved as in generate_card.py.
    """
    return {
        "deckName": deck_name,
        "modelName": config["model_name"],
        "fields": {
            "Word": word,
            "Front": "",
            "Back": "",
            "Image": f'<div style="width: 250px; height: 250px; margin: 0 auto; overflow: hidden; display: flex; align-items: center; justify-content: center;"><img src="{image_url}" style="width: 100%; height: 100%; object-fit: contain;"></div>' if image_url else "",
            "Definition": dictionary_data["definition"],
            "Synonyms": dictionary_data["synonyms"],
            "Antonyms": dictionary_data["antonyms"],
            "Related": dictionary_data["related"],
            "Similar": dictionary_data["similar"],
            "Sentence": highlighted,
            "Sentence_Repeated": sentence,
            "Sentence_Audio": sentence_audio_ref,
            "Word_Audio": word_audio_ref,
            "Irregular_Forms": irregular_forms_field,
            "Dictionary_Entry": dictionary_entry,
            "Translation_UA": translation_ua,
            "Tags": ""
        },
        "options": {
            "allowDuplicate": False
        },
        "tags": []
    }

def submit_note_to_anki(**card_data):
    """
    Build the Anki note and submit it to AnkiConnect, handling errors and printing results.
    Accepts all card fields as keyword arguments.
    """
    note = build_anki_note(**card_data)
    try:
        result = add_note(note)
        print(CARD_CONSTRUCTION_SUBMISSION["card_added"].format(card_id=result['result']))
    except Exception as e:
        print(CARD_CONSTRUCTION_SUBMISSION["exception"].format(error=str(e))) 