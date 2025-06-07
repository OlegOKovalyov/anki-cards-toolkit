# anki-cards-toolkit

<img src="https://raw.githubusercontent.com/OlegOKovalyov/anki-cards-toolkit/main/anki-flashcard.png" alt="Anki Flashcard Toolkit Logo" width="200"/>


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
