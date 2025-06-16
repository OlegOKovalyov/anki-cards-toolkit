import requests
import pyperclip
import json
import re
from duckduckgo_search import DDGS
from gtts import gTTS
import base64
from io import BytesIO
import requests
from bs4 import BeautifulSoup
import termios
import tty
import os
import sys
import webbrowser
import tempfile
import html
import csv
from dotenv import load_dotenv
import os

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


def fetch_pexels_images(query):
    """Fetch images from Pexels API"""
    url = f"https://api.pexels.com/v1/search?query={query}&per_page=16"
    headers = {
        "Authorization": PEXELS_API_KEY
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data.get("photos", [])
        else:
            print(f"❌ Помилка отримання зображень: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Виняток при отриманні зображень: {e}")
        return []

def create_image_selection_page(images, word):
    """Create HTML page for image selection"""
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Вибір зображення для '{word}'</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
                background-color: #1a1a1a;
                color: #e0e0e0;
            }}
            .image-grid {{
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 20px;
                max-width: 1200px;
                margin: 0 auto;
            }}
            .image-container {{
                position: relative;
                aspect-ratio: 1;
                border-radius: 8px;
                overflow: hidden;
                box-shadow: 0 2px 4px rgba(0,0,0,0.3);
                transition: transform 0.2s;
                background-color: #2a2a2a;
            }}
            .image-container:hover {{
                transform: scale(1.02);
                box-shadow: 0 4px 8px rgba(0,0,0,0.4);
            }}
            .image-container img {{
                width: 100%;
                height: 100%;
                object-fit: cover;
            }}
            .image-number {{
                position: absolute;
                top: 10px;
                left: 10px;
                background-color: rgba(0,0,0,0.8);
                color: #ffa94d;
                padding: 5px 10px;
                border-radius: 4px;
                font-weight: bold;
            }}
            .instructions {{
                text-align: center;
                margin: 20px 0;
                padding: 20px;
                background-color: #2a2a2a;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.2);
            }}
            h1 {{
                text-align: center;
                color: #ffffff;
                margin-bottom: 20px;
            }}
            .instructions p {{
                margin: 10px 0;
                color: #e0e0e0;
            }}
            .orange {{
                color: #ffa94d;
            }}
        </style>
    </head>
    <body>
        <h1>Вибір зображення для '<span class="orange">{word}</span>'</h1>
        <div class="instructions">
            <p>👀 Перегляньте зображення нижче та запам'ятайте номер (1-16) бажаного зображення.</p>
            <p>Поверніться до терміналу для вибору.</p>
        </div>
        <div class="image-grid">
    """
    
    for i, photo in enumerate(images, 1):
        html += f"""
            <div class="image-container">
                <img src="{photo['src']['medium']}" alt="Image {i}">
                <div class="image-number">{i}</div>
            </div>
        """
    
    html += """
        </div>
    </body>
    </html>
    """
    
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
    payload = {
        "action": "createDeck",
        "version": 6,
        "params": {"deck": deck_name}
    }
    response = requests.post(ANKI_CONNECT_URL, json=payload).json()
    # Якщо deck вже існує, Anki не повертає помилку — все ок.

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
        print("Зображень не знайдено.")
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
                print(f"❌ Будь ласка, введіть число від 1 до {len(images)}")
        except ValueError:
            print("❌ Будь ласка, введіть правильне число")

def detect_pos_from_context(word, sentence):
    """Simple rule-based POS detection"""
    word = word.lower()
    sentence = sentence.lower()
    
    # Find the word and its surrounding context
    word_pattern = re.compile(r'\b' + re.escape(word) + r'\w*\b')
    match = word_pattern.search(sentence)
    if not match:
        return None
        
    words = sentence.split()
    word_index = None
    for i, w in enumerate(words):
        if word in w:
            word_index = i
            break
            
    if word_index is None:
        return None
        
    # Simple rules for POS detection
    # Check for adjective
    if word.endswith(('able', 'ible', 'al', 'ful', 'ic', 'ive', 'less', 'ous')):
        return "adjective"
    
    # Check for adverb
    if word.endswith('ly'):
        return "adverb"
    
    # Check for verb
    if word_index > 0:
        prev_word = words[word_index - 1]
        if prev_word in ['to', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can']:
            return "verb"
    
    # Check for common verb endings
    if word.endswith(('ate', 'ize', 'ise', 'ify')):
        return "verb"
    
    # Default to noun if no other patterns match
    return "noun"

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

def fetch_dictionary_data(word, requested_pos=None):
    """
    Fetch word data from dictionary API with optional POS filtering.
    When POS is specified, returns only definitions, synonyms, and antonyms
    from that specific part of speech, but always returns the full dictionary entry.
    """
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"❌ Помилка: слово '{word}' не знайдено у словнику.")
            return None
            
        data = response.json()[0]
        meanings = data.get("meanings", [])
        
        # Always format full dictionary entry regardless of POS
        dictionary_entry = format_dictionary_entry(data)
        
        # For other fields, filter by POS if specified
        if requested_pos:
            matching_meanings = [m for m in meanings if m.get("partOfSpeech") == requested_pos]
            if matching_meanings:
                meaning = matching_meanings[0]
            else:
                print(f"⚠️ Визначення для частини мови '{requested_pos}' не знайдено.")
                return None
        else:
            meaning = meanings[0] if meanings else None
            
        if not meaning:
            return None
            
        definitions = meaning.get("definitions", [])
        if not definitions:
            return None
            
        # Get thesaurus data
        thes_data = fetch_thesaurus_data(word, requested_pos)
            
        return {
            "definition": definitions[0].get("definition", ""),
            "example": definitions[0].get("example", ""),
            "synonyms": format_word_list(thes_data["synonyms"]),
            "antonyms": format_word_list(thes_data["antonyms"]),
            "related": format_word_list(thes_data["related"]),
            "similar": format_word_list(thes_data["similar"]),
            "partOfSpeech": meaning.get("partOfSpeech", ""),
            "dictionary_entry": dictionary_entry  # This now contains the full dictionary entry
        }
        
    except Exception as e:
        print(f"❌ Виняток при отриманні даних зі словника: {e}")
        return None

# == Зчитуємо речення з буфера ==
# sentence = re.sub(r'\s+', ' ', pyperclip.paste().replace('\n', ' ')).strip()
# print(f"\n📋 Скопійоване речення:\n{sentence}\n")

deck_name = "Default"
deck_name = get_deck_name()
create_deck_if_not_exists(deck_name)

# == Зчитуємо речення з буфера і очищуємо ==
raw_text = pyperclip.paste()

# Обробка:
# 1. Видаляємо перенесення з дефісом (generos-\nity → generosity)
# 2. Прибираємо всі переноси рядків (залишки)
# 3. Прибираємо зайві пробіли перед розділовими знаками
# 4. Заміна декількох пробілів на один
import re
sentence = raw_text
sentence = re.sub(r'-\s*\n\s*', '', sentence)       # перенос із дефісом
sentence = re.sub(r'\s*\n\s*', ' ', sentence)        # звичайні переноси
sentence = re.sub(r'\s+([.,:;!?])', r'\1', sentence) # пробіл перед пунктуацією
sentence = re.sub(r'\s{2,}', ' ', sentence)          # подвійні пробіли
sentence = sentence.strip()

print(f"\n📋 Скопійоване речення:\n{sentence}\n")


# == Запит слова ==
word = input("🔤 Введи слово, яке хочеш вивчати: ").strip().lower()

# Detect part of speech and show it in the prompt
detected_pos = detect_pos_from_context(word, sentence) or "noun"
pos = input(f"📝 Частина мови [{detected_pos}] [Натисни Enter для підтвердження або поміняй (noun/verb/adjective/adverb)]: ").strip().lower()
if not pos:
    pos = detected_pos

# Get dictionary data with POS
data = fetch_dictionary_data(word, pos)
if not data:
    exit(1)

# == Підсвічення слова в реченні ==
highlighted = re.sub(
    rf'\b({re.escape(word)}\w*)\b',
    r'<span style="color:orange;font-weight:bold">\1</span>',
    sentence,
    count=1,
    flags=re.IGNORECASE
)

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
def generate_tts_base64(text):
    try:
        tts = gTTS(text)
        buffer = BytesIO()
        tts.write_to_fp(buffer)
        buffer.seek(0)
        encoded = base64.b64encode(buffer.read()).decode('utf-8')
        return f"[sound:tts_{word}.mp3]", encoded
    except requests.exceptions.ConnectionError:
        print("\n❌ Помилка: Не вдалося підключитися до сервісу TTS. Перевірте підключення до інтернету.")
        return None, None
    except Exception as e:
        print(f"\n❌ Помилка при генерації TTS: {str(e)}")
        return None, None

word_audio_ref, word_audio_data = generate_tts_base64(word)
if word_audio_ref is None or word_audio_data is None:
    print("ℹ️ Пропускаємо створення картки через помилку TTS. Спробуйте наступне речення.")
    exit(0)

sentence_audio_ref, sentence_audio_data = generate_tts_base64(sentence)
if sentence_audio_ref is None or sentence_audio_data is None:
    print("ℹ️ Пропускаємо створення картки через помилку TTS. Спробуйте наступне речення.")
    exit(0)

# == Додавання мультимедійних файлів до Anki ==
def check_anki_connect():
    """Check if AnkiConnect is available"""
    try:
        response = requests.get("http://localhost:8765")
        return True
    except requests.exceptions.ConnectionError:
        print("\n❌ Помилка: Не вдалося підключитися до Anki.")
        print("📝 Переконайтеся, що:")
        print("   1. Anki запущено")
        print("   2. Встановлено додаток AnkiConnect")
        print("   3. AnkiConnect налаштовано на порт 8765")
        return False

def send_media_file(name, b64_data):
    """Send media file to Anki with error handling"""
    try:
        result = requests.post("http://localhost:8765", json={
            "action": "storeMediaFile",
            "version": 6,
            "params": {
                "filename": name,
                "data": b64_data
            }
        }, timeout=5).json()
        
        if result.get("error"):
            print(f"⚠️ Помилка додавання {name}: {result['error']}")
            return False
        else:
            print(f"📁 Файл {name} збережено")
            return True
            
    except requests.exceptions.ConnectionError:
        print(f"⚠️ Не вдалося зберегти {name}: немає зʼєднання з Anki")
        return False
    except Exception as e:
        print(f"⚠️ Помилка при збереженні {name}: {str(e)}")
        return False

# Before sending files to Anki, check connection
anki_available = check_anki_connect()

if word_audio_data:
    if anki_available:
        send_media_file(f"tts_{word}.mp3", word_audio_data)
    else:
        print("⚠️ Аудіо файл не буде збережено через відсутність зʼєднання з Anki")

if sentence_audio_data:
    if anki_available:
        send_media_file(f"tts_sentence_{word}.mp3", sentence_audio_data)
    else:
        print("⚠️ Аудіо файл речення не буде збережено через відсутність зʼєднання з Anki")

# == Запит українського перекладу ==
print("\n📝 Введіть український переклад:")
translation_ua = input("🔤 Введіть слова перекладу (розділяйте комами): ").strip()

# == Формування картки ==
if anki_available:
    note = {
        "deckName": deck_name,
        "modelName": MODEL_NAME,
        "fields": {
            "Word": word,
            "Front": "",
            "Back": "",
            "Image": f'<div style="width: 250px; height: 250px; margin: 0 auto; overflow: hidden; display: flex; align-items: center; justify-content: center;"><img src="{image_url}" style="width: 100%; height: 100%; object-fit: contain;"></div>' if image_url else "",
            "Definition": data["definition"],
            "Synonyms": data["synonyms"],
            "Antonyms": data["antonyms"],
            "Related": data["related"],
            "Similar": data["similar"],
            "Sentence": highlighted,
            "Sentence_Repeated": sentence,
            "Sentence_Audio": "[sound:tts_sentence_{0}.mp3]".format(word) if sentence_audio_data else "",
            "Word_Audio": word_audio_ref,
            "Dictionary_Entry": data["dictionary_entry"],
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
else:
    print("\n⚠️ Картку не було додано через відсутність зʼєднання з Anki")
    print("💡 Щоб додати картку пізніше:")
    print(f"   1. Запустіть Anki")
    print(f"   2. Переконайтеся, що встановлено AnkiConnect")
    print(f"   3. Запустіть скрипт знову")
