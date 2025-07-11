# 🃏 anki-cards-toolkit

<img src="https://raw.githubusercontent.com/OlegOKovalyov/anki-cards-toolkit/main/anki-flashcard.png" alt="Anki Flashcard Toolkit Logo" width="200"/>

## 🧭 Project Overview

This toolkit automates the creation of rich Anki flashcards for English vocabulary learning. It integrates pronunciation, imagery, CEFR level, and frequency ranking for focused memorization.

The core workflow:
- Reads a sentence from the clipboard
- Allows selecting a **focus word**
- Automatically generates pronunciation audio (TTS)
- Embeds a relevant image using Pexels free online media library
- Adds CEFR level and frequency category next to the focus word
- Outputs a ready-to-use HTML front and back template for the Anki card


## 🔧 Installation

Clone the repository and set up a virtual environment:

```bash
git clone https://github.com/OlegOKovalyov/anki-cards-toolkit.git
cd anki-cards-toolkit
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
> Make sure to activate the virtual environment every time you work on the project.

### 🐉 Python Virtual Environment

It is recommended to work in a virtual environment to keep dependencies isolated from your system Python.

✅ Create a virtual environment:
```bash
python3 -m venv venv
```
✅ Activate the environment:

• Linux/macOS:
```bash
source venv/bin/activate
```
• Windows:

```bash
venv\Scripts\activate
```
After activation, your terminal should show (venv) at the beginning of the prompt.

### 🔈 Generating Silent Audio for Flashcards

To enable a natural-sounding pause between the sentence and the target word in each flashcard's audio playback, you need to generate a silent audio file. Run the following script to create a 1-second silent MP3:

```bash
python scripts/generate_silence.py
```
This will generate a file named silence_1sec.mp3, which will be placed automatically into Anki’s media folder (typically located at ~/.local/share/Anki2/User 1/collection.media/ or similar, depending on your system). This file will be used as part of the audio sequence for each card.

### 🔤 NLTK resources

This project uses NLTK lemmatization (WordNet).  
After installing dependencies, run the following once:

```bash
python scripts/install_nltk_data.py
```

### 🔑 Pexels API Key (Optional, for image support)

If you want to automatically fetch relevant images for your cards from Pexels.com, you need to obtain a free API key:

1. Go to https://www.pexels.com/api/ and create an account (or log in).
2. Click "**Get API Key**" and copy your personal key.
3. Open the .env file and replace the placeholder value of your_pexels_api_key with your actual key:
```py
PEXELS_API_KEY = 'your_actual_pexels_api_key_here'
```
4. Save the file.
💡 If you skip this step, image support will be disabled and your cards will be created without accompanying pictures.

### 🔑 Get a Big Huge Thesaurus API Key

This tool uses the Big Huge Thesaurus API to fetch synonyms, related terms, similar words, and antonyms for the selected vocabulary word.

To use this functionality:

1. Visit https://words.bighugelabs.com/site/api.
2. Sign up or log in to your account.
3. Generate a free API key (you will receive a string similar to 7d4eb...9ab01).
4. Open the file generate_card.py.
5. In the .env file, replace the placeholder your_big_huge_thesaurus_key with your actual API key:
```py
BIG_HUGE_API_KEY = 'your_api_key_here'  # Big Huge Thesaurus API key
```
Without this key, word associations (synonyms, antonyms, etc.) will not be retrieved.

### 🔐 Environment Configuration

Before running the project, you need to create a `.env` file in the root directory.

This file should contain the following settings:

```
MODEL_NAME=VocabCard_English_UA
DECK_NAME=Default
PEXELS_API_KEY=your_pexels_api_key
BIG_HUGE_API_KEY=your_big_huge_thesaurus_key
ANKI_CONNECT_URL=http://localhost:8765
CONFIG_FILE=last_deck.txt
```

> ⚠️ Do not include quotes around values.

The `.env` file should not be committed to version control. It is ignored by `.gitignore` for security.

The project uses the [`python-dotenv`](https://pypi.org/project/python-dotenv/) library to load this configuration.


### 🔇 Optional: Generating a Custom Silence MP3

If you want to customize the duration of the pause, you can edit the script scripts/generate_silence.py by changing the duration_ms parameter, which is specified in milliseconds. For example:

```py
generate_silence(duration_ms=2000)  # creates a 2-second silence
```

You can run the script again after modifying the value to regenerate the file with the new duration.

### 🧩 Using the Card Templates in Anki

To ensure that the generated Anki flashcards are displayed correctly, the project includes two HTML template files located in the /templates directory:

    front_template.html: Defines the front side of the flashcard.

    back_template.html: Defines the back side of the flashcard.

These templates are intended for use with a custom card type in Anki. We recommend creating a new card type based on the default Basic type and naming it something like VocabCard_English_UA. You can do this by navigating to: Anki → Browse → Cards (Ctrl+L) → Front Template / Back Template. Copy the contents of front_template.html and back_template.html into the corresponding sections of your newly created card type.

>Note: The back_template.html file includes a short silent audio clip before playing the focus word’s audio. This is done by inserting the following block:

```html
<div style="display: none;">
  <!-- Adding a silent audio file to create a pause -->
  [sound:silence_1sec.mp3]
</div>
```
This allows for a natural pause between the sentence and the word pronunciation, improving listening and memorization.

### ⚠️ Required Fields

In addition to customizing the templates, you must manually create the following fields for your custom card type in Anki. Without these fields, the templates and generated data will not work correctly.

Here is the full list of fields used by the project, in the recommended order:

1. `Front` *(default Basic field — keep it)*
2. `Back` *(default Basic field — keep it)*
3. `Sentence`
4. `Sentence_Audio`
5. `Definition`
6. `Synonyms`
7. `Related`
8. `Similar`
9. `Antonyms`
10. `Sentence_Repeated`
11. `Image`
12. `Word`
13. `Irregular_Forms` *(used only if the focus word is an irregular verb)*
14. `Word_Audio`
15. `Dictionary_Entry`
16. `Translation_UA`

To add these fields:
1. Open Anki.
2. Go to **Browse** → **Cards**.
3. Click **Fields…**.
4. Add each field manually in the order shown above.

Anki will automatically ignore empty fields when displaying cards, so optional content (such as `Irregular_Forms`) will not interfere with the card appearance.

> ⚠️ Important:
> When setting up the card fields in Anki (Browse → Card Types → VocabCard_English_UA → Fields), make sure that the first field in the >list >is one that is always filled, such as Word or Sentence.
> Anki uses the first field to determine whether a note is empty. If this field is blank, the note will be rejected with the error:
```
cannot create note because it is empty
```
> Fields like Front or Back are often left empty in this toolkit and should not be placed first in the list. It would be best to put the focus word **Word** field as the first field.


### 🗂️ Deck Selection and Persistence

Starting from version 1.0.0, the toolkit supports dynamic deck selection during card creation.  
When generating a new card, the script will now:

1. Prompt the user for a target Anki deck name. You have to type it manually because the sentence for the card is on the clipboard. You can't copy-paste it.
2. Suggest the previously used deck as default (stored in `last_deck.txt`).
3. Automatically create the deck if it does not exist.

This allows you to group your flashcards by topic or lesson (e.g., `History - Chapter 01`, `English - Mood Food`) without modifying the script.

💡 To skip retyping the same deck name each time, just press `Enter` — the previous name will be reused.

## 📸 Screenshots

Below are examples of a vocabulary flashcard generated by the project:

**Front side**: anki-cards-toolkit/docs/front-card-example.jpg - 
Contains the sentence with the target word highlighted and audio playback.

**Back side**: anki-cards-toolkit/docs/back-card-example.jpg -
Includes the sentence again, an image, the target word, dictionary entry with transcription, definitions, synonyms, related, similar, antonyms, and a Ukrainian translation.

## 🧑‍💻 User Interaction Workflow

Here is a sample interaction between the user and the script:
```bash
(venv) olegkovalyov/anki-cards-toolkit$ python3 generate_card.py
```
```
✅ Loaded CEFR/frequency data for 172782 words
Введіть назву колоди [Chapter 6: The Word of Islam]: 
📋 Скопійоване речення:
Roman history is the story of the Romans’ conquest of Italy and the entire Mediterranean world.
🔤 Введи слово, яке хочеш вивчати: conquest
📝 Частина мови [noun] [Натисни Enter для підтвердження або поміняй (noun/verb/adjective/adverb)]: 
🔍 Запит до Big Huge Thesaurus для слова 'conquest'...
✅ Отримано відповідь від Big Huge Thesaurus
📚 Доступні частини мови: noun
📝 Знайдені зв'язки:
   Synonyms: 8 слів
   Приклад: conquering, subjection, subjugation, seduction, capture...
🔍 Пошук відповідних зображень...

🔍 Sending request to Pexels API...
📡 Status code: 200
✅ Found 6 images
Знайдено 6 зображень. Відкриваю попередній перегляд у браузері...

🔢 Введіть номер зображення (1–6) або натисніть Enter для пропуску: 2
✅ Зображення успішно вибрано.
📁 Файл tts_conquest.mp3 збережено
📁 Файл tts_sentence_conquest.mp3 збережено

📝 Введіть український переклад:
🔤 Введіть слова перекладу (розділяйте комами): завоювання, підкорення
✅ Картку додано: ID = 1749913745076
```

## ▶️ Running the tool

Before using this tool to generate Anki flashcards, make sure the following prerequisites are met:

### 1. Install Anki

Download and install the Anki application from the official website:  
👉 https://apps.ankiweb.net/

Anki must be running in the background while you use this script to send cards.

### 2. Install the AnkiConnect Add-on

This tool uses [AnkiConnect](https://github.com/FooSoft/anki-connect) to communicate with the Anki app.

To install AnkiConnect:

1. Open Anki
2. Go to `Tools` → `Add-ons` → `Get Add-ons…`
3. Paste the following code:  
   `2055492159`
4. Click "OK" and restart Anki

After installation, AnkiConnect will automatically listen for connections at `http://localhost:8765`.

### 3. Make Sure Anki is Running

Before launching the `generate_card.py` script, ensure that:
- Anki is running
- AnkiConnect is enabled
- You are connected to the internet (for dictionary and image lookups)

If Anki is not running or AnkiConnect is not installed, the script will fail with a `ConnectionRefusedError`.

```bash
source venv/bin/activate
python generate_card.py
```
## 🌐 Internet Usage, Anki Profile, Audio & Images

This project is designed to work **online**. An active internet connection is required for the following features:
- Fetching word definitions, synonyms, and related words from the Big Huge Thesaurus API
- Retrieving image suggestions from [Pexels](https://www.pexels.com/)
- Text-to-Speech (TTS) audio generation

### 👤 Anki Profile: `User 1`

By default, when Anki is installed and launched for the first time, it automatically creates a profile named **`User 1`**.  
All generated media files (images, audio, etc.) will be stored under this profile in the following directory:

• Linux/macOS::
```bash
~/.local/share/Anki2/User 1/
```

• Windows:
```bash
C:\Users\<YourUsername>\AppData\Roaming\Anki2\User 1\
```
If you change your Anki profile name, the directory will also change. To rename or manage profiles, refer to the official Anki documentation on profiles. This toolkit assumes the default profile User 1 is used.

### 🔉 Local Audio Generation (TTS)

The application uses Text-to-Speech (TTS) technology to generate audio files for:

- the vocabulary word
- the example sentence

> TTS is a system that converts written text into spoken audio.
> In this project, audio is generated using the gTTS (Google Text-to-Speech) Python library.

Two audio files are created for each card:

- tts_<word>.mp3
- tts_sentence_<word>.mp3

They are saved locally to:
```bash
~/.local/share/Anki2/User 1/collection.media/
```
If a card is deleted or replaced, audio files may temporarily move to:
```bash
~/.local/share/Anki2/User 1/collection.media/media.trash/
```

### 🖼️ Online Image Embedding from Pexels

Images are embedded into Anki cards using direct URLs from the Pexels image platform.
Images are not downloaded or stored locally. For example:
```html
<div style="width: 250px; height: 250px; margin: 0 auto; overflow: hidden; display: flex; align-items: center; justify-content: center;">
    <img src="https://images.pexels.com/photos/946337/pexels-photo-946337.jpeg?auto=compress&amp;cs=tinysrgb&amp;h=350" style="width: 100%; height: 100%; object-fit: contain;">
</div>
```
Since images are loaded from external sources, an active internet connection is required to display them during card reviews in Anki.

### ✏️ Manually Replacing Images

If you are not satisfied with the automatically chosen image, you can manually replace it:
1. Open Anki and locate the card.
2. Click Edit to open the card content.
3. Replace the current <img src="..."> tag with any other publicly accessible image URL to the question mark.
• For example:
```html
<img src="https://www.example.com/your-custom-image.png">
```
Your custom image will now be shown in reviews instead of the original Pexels image.

## 🧠 CEFR & Frequency integration

The project supports adding both CEFR levels (A1–C2) and word frequency category (1–9) to each word used in the flashcard. The relevant merged dataset is stored in data/merged_cefr_frequency.csv and is used by the card generation script to enrich flashcards with this metadata.

To regenerate or update this merged file (e.g. if the source CSVs change), use the script merge_cefr_and_frequency.py located in data/. This script combines CEFR and frequency information into a single file.

The input CSVs required for this are:

    data/word_list_cefr.csv

    data/valid_words_sorted_by_frequency.csv

These files were obtained from the open-source project:

Maximax67 / Words-CEFR-Dataset
GitHub link: https://github.com/Maximax67/Words-CEFR-Dataset/tree/main
Author: Bielikov Maksym

We thank the author for providing this valuable dataset under a permissive open-source license.
According to the license, data from this repository may be reused, modified, and distributed with attribution.

To manually download these files if not present:

```bash
cd data/
wget https://raw.githubusercontent.com/Maximax67/Words-CEFR-Dataset/main/csv/word_list_cefr.csv
wget https://raw.githubusercontent.com/Maximax67/Words-CEFR-Dataset/main/csv/valid_words_sorted_by_frequency.csv
```

Then run:

```bash
python3 merge_cefr_and_frequency.py
```

The script will generate merged_cefr_frequency.csv with the structure:

```csv
Word,CEFR,Frequency
abandon,B2,4
about,A1,2
acquaintance,?,6
```
Where:

    CEFR is the Common European Framework level (A1–C2) or ? if not found

    Frequency is a category from 1 (most frequent) to 9 (least frequent), calculated based on a 172,000-word frequency list using the following ranges:

| Category | Frequency Range     |
| -------- | ------------------- |
| 1        | 10,000 – 17,000     |
| 2        | 17,000 – 30,000     |
| 3        | 30,000 – 50,000     |
| 4        | 50,000 – 100,000    |
| 5        | 100,000 – 170,000   |
| 6        | 170,000 – 300,000   |
| 7        | 300,000 – 800,000   |
| 8        | 800,000 – 3,000,000 |
| 9        | 3,000,000 and above |

The merge_cefr_and_frequency.py script is designed to be run from within the data/ directory and expects the two CSV files to be located in the same folder.    

Note: the input CSV files and the script for merging are intended to be kept in the local repository only and are not committed to GitHub. Only the generated merged_cefr_frequency.csv is stored in the repository. The source CSVs and merging script are kept locally and excluded from version control.


# 📘 Best Practices for Using This Toolkit with Anki

To make the most of your vocabulary learning with Anki and this toolkit, consider the following workflow and usage tips:

## 🧱 Card Creation Guidelines

1. Start by **copying a sentence** to the clipboard from any learning source — such as a textbook, PDF, movie, TV series, podcast, or article.

2. Then run the script from the terminal. It will first **prompt you to enter a deck name**:

   • If you press Enter, it will use the last deck name you entered.

   • If you're starting a new topic, type the new deck name manually.

   • **Important:** After copying a sentence, do **not copy anything else** (like the deck name) — or the script will pick up the wrong text. Always type the deck name manually.

3. The script will then display the sentence you copied and ask you to **enter the focus word** (the word you're learning from that sentence).

4. Cards are generated using the predefined note type VocabCard_English_UA, which includes:

        The full sentence

        Word translation and definition

        CEFR level and frequency

        Audio and silence gap

🗂 Examples of deck names:

        English File - Intermediate - Unit 2

        Movie - The Matrix

        TV Series - Breaking Bad

        Podcast - VOA Learning English

        History - Chapter 03 - Ancient Egypt

Organizing decks by source makes it easier to review contextually and stay focused.

## ✅ Card Review Strategy

1. In Anki, click "**Study Now**" to review cards from your chosen deck.

2. After reading the sentence and recalling or checking the meaning of the target word, click "**Show Answer**".

3.  Then evaluate your recall accuracy by selecting:

    **Again** if you forgot the word or struggled

    **Hard** if you barely remembered

    **Good** if you recalled it correctly with some effort

    **Easy** if it was instant and effortless

This feedback helps Anki’s spaced repetition algorithm optimize your future reviews.

## 🔁 How Often to Create and Review

• Aim to generate **5–10 new cards per day**.

• Review your **due cards daily**, even if no new cards are added.

• Focus on quality over quantity: meaningful, real-world context matters more than isolated words.


## 📜 License

This project is distributed under the MIT License. See LICENSE for more information.

Data provided by Maximax67/Words-CEFR-Dataset is used under the terms of its original license, with thanks to the author.
