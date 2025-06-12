# anki-cards-toolkit

<img src="https://raw.githubusercontent.com/OlegOKovalyov/anki-cards-toolkit/main/anki-flashcard.png" alt="Anki Flashcard Toolkit Logo" width="200"/>

## Project Overview

This toolkit automates the creation of rich Anki flashcards for English vocabulary learning. It integrates pronunciation, imagery, CEFR level, and frequency ranking for focused memorization.

The core workflow:
- Reads a sentence from the clipboard
- Allows selecting a **focus word**
- Automatically generates pronunciation audio (TTS)
- Embeds a relevant image using DuckDuckGo search
- Adds CEFR level and frequency category next to the focus word
- Outputs a ready-to-use HTML front template for the Anki card


## Installation

Clone the repository and set up a virtual environment:

```bash
git clone https://github.com/OlegOKovalyov/anki-cards-toolkit.git
cd anki-cards-toolkit
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

To enable a natural-sounding pause between the sentence and the target word in each flashcard's audio playback, you need to generate a silent audio file. Run the following script to create a 1-second silent MP3:

```bash
python scripts/generate_silence.py
```

This will generate a file named silence_1sec.mp3, which will be placed automatically into Anki’s media folder (typically located at ~/.local/share/Anki2/User 1/collection.media/ or similar, depending on your system). This file will be used as part of the audio sequence for each card.

### Optional: Generating a Custom Silence MP3

If you want to customize the duration of the pause, you can edit the script scripts/generate_silence.py by changing the duration_ms parameter, which is specified in milliseconds. For example:

```py
generate_silence(duration_ms=2000)  # creates a 2-second silence
```

You can run the script again after modifying the value to regenerate the file with the new duration.

### Using the Card Templates in Anki

To ensure that the generated Anki flashcards are displayed correctly, the project includes two HTML template files located in the /templates directory:

    front_template.html: Defines the front side of the flashcard.

    back_template.html: Defines the back side of the flashcard.

These templates are intended for use with a custom card type in Anki. We recommend creating a new card type based on the default Basic type and naming it something like VocabCard_English_UA. You can do this by navigating to: Anki → Browse → Cards (Ctrl+L) → Front Template / Back Template. Copy the contents of front_template.html and back_template.html into the corresponding sections of your newly created card type.

Note: The back_template.html file includes a short silent audio clip before playing the focus word’s audio. This is done by inserting the following block:

```html
<div style="display: none;">
  <!-- Adding a silent audio file to create a pause -->
  [sound:silence_1sec.mp3]
</div>
```

This allows for a natural pause between the sentence and the word pronunciation, improving listening and memorization.

## Running the tool

```bash
source venv/bin/activate
python generate_card.py
```

## CEFR & Frequency integration

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

## License

This project is distributed under the MIT License. See LICENSE for more information.

Data provided by Maximax67/Words-CEFR-Dataset is used under the terms of its original license, with thanks to the author.
