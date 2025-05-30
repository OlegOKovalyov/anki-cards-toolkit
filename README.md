# anki-cards-toolkit

This tool automates the creation of Anki cards based on a copied sentence.

## Features

- Reads text from clipboard
- Allows selecting a focus word
- Uses TTS to generate pronunciation audio
- Searches and embeds an image (DuckDuckGo)
- Outputs HTML front template for Anki card

## Installation

Clone the repo and set up a virtual environment:

```bash
git clone https://github.com/YOUR-USERNAME/anki-cards-toolkit.git
cd anki-cards-toolkit
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
