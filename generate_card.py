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

# == Зчитуємо речення з буфера ==
sentence = re.sub(r'\s+', ' ', pyperclip.paste().replace('\n', ' ')).strip()
print(f"\n📋 Скопійоване речення:\n{sentence}\n")

# == Запит слова ==
word = input("🔤 Введи слово, яке хочеш вивчати: ").strip().lower()

# == Отримати визначення, приклад, синоніми ==
def fetch_dictionary_data(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"❌ Помилка: слово '{word}' не знайдено у словнику.")
            return None
        data = response.json()[0]
        meanings = data.get("meanings", [])
        definition = ""
        example = ""
        synonyms = []

        for meaning in meanings:
            defs = meaning.get("definitions", [])
            if defs:
                definition = defs[0].get("definition", "")
                example = defs[0].get("example", "")
                synonyms = defs[0].get("synonyms", [])
                break

        return {
            "definition": definition,
            "example": example,
            "synonyms": ", ".join(synonyms[:5]) if synonyms else ""
        }
    except Exception as e:
        print(f"❌ Виняток: {e}")
        return None

data = fetch_dictionary_data(word)
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
