import requests
import pyperclip
import re
from gtts import gTTS
import base64
from io import BytesIO
import termios
import tty
import os
import sys
import webbrowser
import tempfile
import csv
from nltk.stem import WordNetLemmatizer
from dotenv import load_dotenv
from docs.error_messages import (
    PEXELS_API_ERRORS,
    ANKI_ERRORS,
    TTS_ERRORS,
    DICTIONARY_ERRORS,
    IMAGE_SELECTION_ERRORS,
    GENERAL_ERRORS,
    SUCCESS_MESSAGES
)
from data.irregular_verbs import irregular_verbs
from src.services.clipboard_service import get_clean_sentence_from_clipboard
from src.linguistics.pos import detect_pos_from_context, get_irregular_forms
from src.utils.highlight import highlight_focus_word
from src.services.pexels_api import fetch_pexels_images
from src.services.dictionary_service import fetch_word_data
from src.services.tts_service import generate_tts_base64
from src.services.media_service import send_media_file

# Load .env file
load_dotenv()

# == Configuration from .env ==
# MODEL_NAME refers to the name of the Note Type in Anki.
# To check or change it in Anki: open Anki → Tools → Manage Note Types.
# Your note type should be  named as VocabCard_English_UA
MODEL_NAME = os.getenv("MODEL_NAME")

# DECK_NAME is the name of the Anki deck where the new cards will be added.
# You can create or check deck names via Anki: open Anki → Decks → Add.
# The initial deck name will be Default
DECK_NAME = os.getenv("DECK_NAME")

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY") # API key for Pexels
BIG_HUGE_API_KEY = os.getenv("BIG_HUGE_API_KEY") # API key for Big Huge Thesaurus
ANKI_CONNECT_URL = os.getenv("ANKI_CONNECT_URL") # URL of the AnkiConnect server

# Path to the file where the name of the last used deck will be stored
CONFIG_FILE = os.getenv("CONFIG_FILE") # last_deck.txt

# == Check Anki connection before anything else ==
def check_anki_connect():
    """Check if AnkiConnect is available. If not, print instructions and exit immediately."""
    try:
        response = requests.get("http://localhost:8765")
        return True
    except requests.exceptions.ConnectionError:
        print("\n❌ Помилка: Не вдалося підключитися до Anki.")
        print("Будь ласка, запустіть Anki та спробуйте ще раз.")
        print("📝 Переконайтеся, що:")
        print("   1. Anki запущено")
        print("   2. Встановлено додаток AnkiConnect")
        print("   3. AnkiConnect налаштовано на порт 8765")
        sys.exit(1)

check_anki_connect()

def create_image_selection_page(images, word):
    """Create HTML page for image selection"""
    # Read the template file
    template_path = os.path.join(os.path.dirname(__file__), 'templates', 'image_selection.html')
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()
    
    # Generate the image grid HTML
    image_grid_html = ""
    for i, photo in enumerate(images, 1):
        image_grid_html += f"""
            <div class="image-container">
                <img src="{photo['src']['medium']}" alt="Image {i}">
                <div class="image-number">{i}</div>
            </div>
        """
    
    # Replace placeholders in the template
    html = template.replace('{{word}}', word)
    html = html.replace('{{image_grid}}', image_grid_html)
    
    return html

def load_last_deck():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return f.read().strip()
    return "Default"

def save_last_deck(deck_name):
    with open(CONFIG_FILE, "w") as f:
        f.write(deck_name.strip())

def get_deck_name():
    last_deck = load_last_deck()
    user_input = input(f"Введіть назву колоди [{last_deck}]: ").strip()
    deck = user_input if user_input else last_deck
    save_last_deck(deck)
    return deck

def create_deck_if_not_exists(deck_name):
    """Create a new deck in Anki if it doesn't exist"""
    payload = {
        "action": "createDeck",
        "version": 6,
        "params": {"deck": deck_name}
    }
    try:
        response = requests.post(ANKI_CONNECT_URL, json=payload, timeout=5)
        response.raise_for_status()  # Raise exception for bad status codes
        result = response.json()
        if result.get("error"):
            print(f"⚠️ Помилка створення колоди: {result['error']}")
            return False
        return True
    except requests.exceptions.ConnectionError:
        # Do not print error here; already handled at startup
        return False
    except requests.exceptions.Timeout:
        print("❌ Перевищено час очікування відповіді від Anki")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Помилка запиту до Anki: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Неочікувана помилка при створенні колоди: {str(e)}")
        return False

def load_cefr_frequency_data():
    """Load CEFR and frequency data from CSV file"""
    cefr_freq_data = {}
    csv_path = os.path.join(os.path.dirname(__file__), 'data', 'merged_cefr_frequency.csv')
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                word = row['Word'].strip().lower()
                cefr = row['CEFR'].strip().upper()
                freq = row['Frequency'].strip()
                cefr_freq_data[word] = {'cefr': cefr, 'frequency': freq}
        print(f"✅ Loaded CEFR/frequency data for {len(cefr_freq_data)} words")
        return cefr_freq_data
    except Exception as e:
        print(f"⚠️ Could not load CEFR/frequency data: {str(e)}")
        return {}

# Load CEFR and frequency data at startup
CEFR_FREQUENCY_DATA = load_cefr_frequency_data()

def get_char():
    """Get a single character from standard input"""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def select_image(images, word):
    """Interactive image selection interface with visual preview"""
    if not images:
        print(IMAGE_SELECTION_ERRORS['no_images'])
        return None
    
    # Create and open selection page
    html_content = create_image_selection_page(images, word)
    with tempfile.NamedTemporaryFile(delete=False, suffix='.html', mode='w', encoding='utf-8') as f:
        f.write(html_content)
        gallery_path = f.name
    webbrowser.open('file://' + os.path.abspath(gallery_path))
    
    while True:
        try:
            choice = input("\n🔢 Введіть номер зображення (1-16) або натисніть Enter для пропуску: ").strip()
            
            if not choice:  # Skip image selection
                os.unlink(gallery_path)
                return None
                
            choice = int(choice)
            if 1 <= choice <= len(images):
                os.unlink(gallery_path)
                return images[choice - 1]['src']['medium']
            else:
                print(IMAGE_SELECTION_ERRORS['invalid_number'].format(max=len(images)))
        except ValueError:
            print(IMAGE_SELECTION_ERRORS['invalid_input'])

def fetch_thesaurus_data(word, pos=None):
    """
    Fetch all lexical relationships from Big Huge Thesaurus for specific part of speech.
    Returns a dictionary containing synonyms, antonyms, related words, and similar words.
    """
    url = f"https://words.bighugelabs.com/api/2/{BIG_HUGE_API_KEY}/{word}/json"
    
    # Map our POS to Big Huge Thesaurus format
    pos_mapping = {
        "noun": "noun",
        "verb": "verb",
        "adjective": "adjective",
        "adverb": "adverb"
    }
    
    try:
        print(f"\n🔍 Запит до Big Huge Thesaurus для слова '{word}'...")
        response = requests.get(url)
        
        if response.status_code != 200:
            print(f"⚠️ Thesaurus: Не вдалося отримати дані для '{word}'")
            print(f"📡 Код відповіді: {response.status_code}")
            return {
                "synonyms": [],
                "antonyms": [],
                "related": [],
                "similar": []
            }
            
        data = response.json()
        print("✅ Отримано відповідь від Big Huge Thesaurus")
        
        # Debug: print available parts of speech in response
        print(f"📚 Доступні частини мови: {', '.join(data.keys())}")
        
        # Initialize result containers
        all_synonyms = []
        all_antonyms = []
        all_related = []
        all_similar = []
        
        # If POS is specified, only look in that section
        if pos and pos in pos_mapping:
            mapped_pos = pos_mapping[pos]
            pos_data = data.get(mapped_pos, {})
            
            if pos_data:
                all_synonyms.extend(pos_data.get('syn', []))
                all_antonyms.extend(pos_data.get('ant', []))
                all_related.extend(pos_data.get('rel', []))
                all_similar.extend(pos_data.get('sim', []))
        else:
            # If no POS specified or not found, gather from all parts of speech
            for pos_section in data.values():
                if isinstance(pos_section, dict):
                    all_synonyms.extend(pos_section.get('syn', []))
                    all_antonyms.extend(pos_section.get('ant', []))
                    all_related.extend(pos_section.get('rel', []))
                    all_similar.extend(pos_section.get('sim', []))
        
        # Remove duplicates while preserving order
        def deduplicate(lst):
            seen = set()
            return [x for x in lst if not (x in seen or seen.add(x))]
        
        result = {
            "synonyms": deduplicate(all_synonyms),
            "antonyms": deduplicate(all_antonyms),
            "related": deduplicate(all_related),
            "similar": deduplicate(all_similar)
        }
        
        # Debug output
        print("\n📝 Знайдені зв'язки:")
        for key, values in result.items():
            if values:
                print(f"   {key.capitalize()}: {len(values)} слів")
                print(f"   Приклад: {', '.join(values[:5])}...")
        
        return result
        
    except Exception as e:
        print(f"❌ Помилка Thesaurus API: {str(e)}")
        return {
            "synonyms": [],
            "antonyms": [],
            "related": [],
            "similar": []
        }

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

def format_word_list(words):
    """Format a list of words, returning empty string if no words found."""
    return ", ".join(words) if words else ""

# == Deck get/creation ==
deck_name = "Default"
deck_name = get_deck_name()
create_deck_if_not_exists(deck_name)

# == Read the sentence from the buffer and clear it ==
# (No need to check Anki connection here anymore)
sentence = get_clean_sentence_from_clipboard()
print(f"\n📋 Скопійоване речення:\n{sentence}\n")

# == Word query ==
word = input("🔤 Введи слово, яке хочеш вивчати: ").strip().lower()

# Detect part of speech and show it in the prompt
detected_pos = detect_pos_from_context(word, sentence) or "noun"
pos = input(f"📝 Частина мови [{detected_pos}] [Натисни Enter для підтвердження або поміняй (noun/verb/adjective/adverb)]: ").strip().lower()
if not pos:
    pos = detected_pos

# Get dictionary data with POS
dictionary_data = fetch_word_data(word, pos)
if not dictionary_data:
    exit(1)

# == Highlight a word in a sentence ==
pos_map = {'noun': 'n', 'verb': 'v', 'adjective': 'a', 'adverb': 'r'}
highlighted = highlight_focus_word(sentence, word, pos=pos_map.get(pos, 'n'))

# == Image Selection ==
print("\n🔍 Пошук відповідних зображень...")
images = fetch_pexels_images(word)
if images:
    print(f"Знайдено {len(images)} зображень. Відкриваю попередній перегляд у браузері...")
    image_url = select_image(images, word)
    if image_url:
        print("✅ Зображення успішно вибрано.")
    else:
        print("⚠️ Зображення не вибрано. Продовжую без зображення.")
else:
    print("⚠️ Зображень не знайдено. Продовжую без зображення.")
    image_url = ""

# == Генерація озвучки (mp3 в base64) ==
word_audio_ref, word_audio_data = generate_tts_base64(word, word)
if word_audio_ref is None or word_audio_data is None:
    print("ℹ️ Пропускаємо створення картки через помилку TTS. Спробуйте наступне речення.")
    exit(0)

sentence_audio_ref, sentence_audio_data = generate_tts_base64(sentence, f"sentence_{word}")
if sentence_audio_ref is None or sentence_audio_data is None:
    print("ℹ️ Пропускаємо створення картки через помилку TTS. Спробуйте наступне речення.")
    exit(0)

# == Додавання мультимедійних файлів до Anki ==
# Before sending files to Anki, check connection
# anki_available = True  # Already checked at the start, so always True

if word_audio_data:
    send_media_file(f"tts_{word}.mp3", word_audio_data)

if sentence_audio_data:
    send_media_file(f"tts_sentence_{word}.mp3", sentence_audio_data)

# == Отримуємо всі форми неправильного дієслова ==
forms = get_irregular_forms(word)
if forms:
    irregular_forms_field = " - ".join(forms)  # Наприклад, "flee - fled - fled"
else:
    irregular_forms_field = ""

# == Запит українського перекладу ==
print("\n📝 Введіть український переклад:")
translation_ua = input("🔤 Введіть слова перекладу (розділяйте комами): ").strip()

# Format the full dictionary entry for the card
dictionary_entry = format_dictionary_entry(dictionary_data["dictionary_api_response"])

# == Формування картки ==
note = {
    "deckName": deck_name,
    "modelName": MODEL_NAME,
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

try:
    result = requests.post("http://localhost:8765", json={
        "action": "addNote",
        "version": 6,
        "params": {"note": note}
    }, timeout=5).json()

    if result.get("error") is None:
        print(f"✅ Картку додано: ID = {result['result']}")
    else:
        print(f"❌ Помилка додавання картки: {result['error']}")
        
except requests.exceptions.ConnectionError:
    print("❌ Не вдалося додати картку: немає зʼєднання з Anki")
except Exception as e:
    print(f"❌ Помилка при додаванні картки: {str(e)}")
