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

# == Налаштування ==
MODEL_NAME = "VocabCard_English_UA"
DECK_NAME = "Default"

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
sentence = re.sub(r'\s+', ' ', pyperclip.paste().replace('\n', ' ')).strip()
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

# == Пошук зображення через DuckDuckGo ==
# def get_image_url(query):
#    try:
#        with DDGS() as ddgs:
#            results = ddgs.images(query)
#            for r in results:
#                return r["image"]
#    except Exception as e:
#        print(f"❌ Не вдалося знайти зображення: {e}")
#        return ""

'''
def get_image_url(word):
    """
    Повертає посилання на перше релевантне зображення зі словом.
    Джерело: Google Images через DuckDuckGo (без API)
    """
    search_url = f"https://duckduckgo.com/?q={word}+english+definition&iax=images&ia=images"
    headers = {'User-Agent': 'Mozilla/5.0'}

    try:
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        img_tags = soup.find_all('img')

        # Пошук першого валідного зображення
        for img in img_tags:
            src = img.get('src')
            if src and src.startswith("http"):
                return src

        return None  # Якщо не знайдено

    except Exception as e:
        print(f"[Error] Failed to fetch image for '{word}':", e)
        return None
'''        

PEXELS_API_KEY = 'R6T2MCrfCrNxu5SrXkO2OSapt8kJTwl4GYTFmEnSHQturYOKztFJAqXU'

def get_image_url(word):
    url = f"https://api.pexels.com/v1/search?query={word}&per_page=1"
    headers = {
        "Authorization": PEXELS_API_KEY
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    if data["photos"]:
        return data["photos"][0]["src"]["medium"]
    else:
        return ""                

image_url = get_image_url(word)

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
