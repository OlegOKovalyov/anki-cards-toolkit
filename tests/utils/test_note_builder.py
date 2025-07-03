import pytest
from src.utils.note_builder import build_anki_note

def test_build_anki_note_minimal():
    word = "run"
    sentence = "I like to run every morning."
    highlighted = "I like to <b>run</b> every morning."
    image_url = "http://example.com/image.jpg"
    dictionary_data = {
        "definition": "move at a speed faster than a walk",
        "synonyms": "jog, sprint",
        "antonyms": "walk",
        "related": "exercise",
        "similar": "dash"
    }
    sentence_audio_ref = "tts_sentence_run.mp3"
    word_audio_ref = "tts_run.mp3"
    irregular_forms_field = "run - ran - run"
    dictionary_entry = "run (verb): move at a speed faster than a walk"
    translation_ua = "бігти"
    config = {"model_name": "Basic"}
    deck_name = "TestDeck"

    note = build_anki_note(
        word=word,
        sentence=sentence,
        highlighted=highlighted,
        image_url=image_url,
        dictionary_data=dictionary_data,
        sentence_audio_ref=sentence_audio_ref,
        word_audio_ref=word_audio_ref,
        irregular_forms_field=irregular_forms_field,
        dictionary_entry=dictionary_entry,
        translation_ua=translation_ua,
        config=config,
        deck_name=deck_name
    )

    assert note["deckName"] == deck_name
    assert note["modelName"] == config["model_name"]
    fields = note["fields"]
    assert fields["Word"] == word
    assert fields["Sentence"] == highlighted
    assert fields["Sentence_Repeated"] == sentence
    assert fields["Image"].startswith('<div style="width: 250px;')
    assert image_url in fields["Image"]
    assert fields["Definition"] == dictionary_data["definition"]
    assert fields["Synonyms"] == dictionary_data["synonyms"]
    assert fields["Antonyms"] == dictionary_data["antonyms"]
    assert fields["Related"] == dictionary_data["related"]
    assert fields["Similar"] == dictionary_data["similar"]
    assert fields["Sentence_Audio"] == sentence_audio_ref
    assert fields["Word_Audio"] == word_audio_ref
    assert fields["Irregular_Forms"] == irregular_forms_field
    assert fields["Dictionary_Entry"] == dictionary_entry
    assert fields["Translation_UA"] == translation_ua
    assert fields["Tags"] == ""
    assert note["options"] == {"allowDuplicate": False}
    assert note["tags"] == []

    # Test image field is empty if image_url is empty
    note2 = build_anki_note(
        word=word,
        sentence=sentence,
        highlighted=highlighted,
        image_url="",
        dictionary_data=dictionary_data,
        sentence_audio_ref=sentence_audio_ref,
        word_audio_ref=word_audio_ref,
        irregular_forms_field=irregular_forms_field,
        dictionary_entry=dictionary_entry,
        translation_ua=translation_ua,
        config=config,
        deck_name=deck_name
    )
    assert note2["fields"]["Image"] == "" 