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

# == Налаштування ==
MODEL_NAME = "VocabCard_English_UA"
DECK_NAME = "Default"
PEXELS_API_KEY = 'R6T2MCrfCrNxu5SrXkO2OSapt8kJTwl4GYTFmEnSHQturYOKztFJAqXU'

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

def create_image_gallery(images, word):
    """Create a temporary HTML file with image gallery"""
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Вибір зображення для '{word}'</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
                background: #f5f5f5;
            }}
            .gallery {{
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 20px;
                margin-top: 20px;
            }}
            .image-container {{
                background: white;
                padding: 15px;
                border-radius: 8px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }}
            .image-container img {{
                width: 100%;
                height: 250px;
                object-fit: cover;
                border-radius: 4px;
            }}
            .image-info {{
                margin-top: 10px;
                font-size: 14px;
                color: #666;
            }}
            h1 {{
                color: #333;
                text-align: center;
            }}
            .instructions {{
                text-align: center;
                margin: 20px 0;
                padding: 15px;
                background: #e9ecef;
                border-radius: 8px;
            }}
        </style>
    </head>
    <body>
        <h1>Вибір зображення для '{word}'</h1>
        <div class="instructions">
            <p>👀 Перегляньте зображення нижче та запам'ятайте номер (1-6) бажаного зображення.</p>
            <p>Поверніться до терміналу для вибору.</p>
        </div>
        <div class="gallery">
    """
    
    for i, image in enumerate(images, 1):
        html_content += f"""
            <div class="image-container">
                <img src="{html.escape(image['url'])}" alt="Варіант {i}">
                <div class="image-info">
                    <strong>Зображення {i}</strong><br>
                    Автор: {html.escape(image['photographer'])}<br>
                    <a href="{html.escape(image['pexels_url'])}" target="_blank">Переглянути на Pexels</a>
                </div>
            </div>
        """
    
    html_content += """
        </div>
    </body>
    </html>
    """
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.html', mode='w', encoding='utf-8') as f:
        f.write(html_content)
        return f.name

def fetch_images(word, num_images=6):
    """Fetch multiple images from Pexels"""
    url = f"https://api.pexels.com/v1/search?query={word}&per_page={num_images}"
    headers = {
        "Authorization": PEXELS_API_KEY
    }
    try:
        response = requests.get(url)
        data = response.json()
        if data.get("photos"):
            return [
                {
                    "url": photo["src"]["medium"],
                    "photographer": photo["photographer"],
                    "pexels_url": photo["url"]
                }
                for photo in data["photos"]
            ]
        return []
    except Exception as e:
        print(f"❌ Error fetching images: {e}")
        return []

def select_image(images, word):
    """Interactive image selection interface with visual preview"""
    if not images:
        print("Зображень не знайдено.")
        return None
    
    # Create and open gallery
    gallery_path = create_image_gallery(images, word)
    webbrowser.open('file://' + os.path.abspath(gallery_path))
    
    while True:
        try:
            choice = input("\n🔢 Введіть номер зображення (1-6) або натисніть Enter для пропуску: ").strip()
            
            if not choice:  # Skip image selection
                os.unlink(gallery_path)
                return None
                
            choice = int(choice)
            if 1 <= choice <= len(images):
                os.unlink(gallery_path)
                return images[choice - 1]['url']
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

def fetch_dictionary_data(word, requested_pos=None):
    """Fetch word data from dictionary API with optional POS filtering"""
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"❌ Помилка: слово '{word}' не знайдено у словнику.")
            return None
            
        data = response.json()[0]
        meanings = data.get("meanings", [])
        
        # If POS is specified, try to find matching definition
        if requested_pos:
            matching_meanings = [m for m in meanings if m.get("partOfSpeech") == requested_pos]
            if matching_meanings:
                meaning = matching_meanings[0]
            else:
                meaning = meanings[0] if meanings else None
                if meaning:
                    print(f"⚠️ Використовую визначення для частини мови: {meaning.get('partOfSpeech')}")
        else:
            meaning = meanings[0] if meanings else None
            
        if not meaning:
            return None
            
        definitions = meaning.get("definitions", [])
        if not definitions:
            return None
            
        return {
            "definition": definitions[0].get("definition", ""),
            "example": definitions[0].get("example", ""),
            "synonyms": ", ".join(definitions[0].get("synonyms", [])[:5]),
            "partOfSpeech": meaning.get("partOfSpeech", "")
        }
        
    except Exception as e:
        print(f"❌ Виняток: {e}")
        return None

# == Зчитуємо речення з буфера ==
# sentence = re.sub(r'\s+', ' ', pyperclip.paste().replace('\n', ' ')).strip()
# print(f"\n📋 Скопійоване речення:\n{sentence}\n")

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
images = fetch_images(word)
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
def send_media_file(name, b64_data):
    result = requests.post("http://localhost:8765", json={
        "action": "storeMediaFile",
        "version": 6,
        "params": {
            "filename": name,
            "data": b64_data
        }
    }).json()
    if result.get("error"):
        print(f"❌ Помилка додавання {name}: {result['error']}")
    else:
        print(f"📁 Файл {name} збережено")

if word_audio_data:
    send_media_file(f"tts_{word}.mp3", word_audio_data)
if sentence_audio_data:
    send_media_file(f"tts_sentence_{word}.mp3", sentence_audio_data)

# == Формування картки ==
note = {
    "deckName": DECK_NAME,
    "modelName": MODEL_NAME,
    "fields": {
        "Word": word,
        "Front": "",
        "Back": "",
        "Image": f'<img src="{image_url}">' if image_url else "",
        "Definition": data["definition"],
        "Sentence": highlighted,
        "Sentence_Repeated": sentence,
        "Sentence_Audio": "[sound:tts_sentence_{0}.mp3]".format(word) if sentence_audio_data else "",
        "Word_Audio": word_audio_ref,
        "Dictionary_Entry": "",
        "Translation_UA": "",
        "Tags": ""
    },
    "options": {
        "allowDuplicate": False
    },
    "tags": []
}

# == Надсилання до AnkiConnect ==
result = requests.post("http://localhost:8765", json={
    "action": "addNote",
    "version": 6,
    "params": {"note": note}
}).json()

if result.get("error") is None:
    print(f"✅ Картку додано: ID = {result['result']}")
else:
    print(f"❌ Помилка: {result['error']}")
