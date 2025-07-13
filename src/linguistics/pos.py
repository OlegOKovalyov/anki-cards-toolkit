"""
POS (Part of Speech) detection and other linguistic utilities.
"""

import sys
import os
import nltk
from nltk import pos_tag, word_tokenize
from nltk.stem import WordNetLemmatizer
import re
from src.locales.loader import get_message

# Add project root to path to allow absolute imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from data.irregular_verbs import irregular_verbs


def detect_pos_from_context(word, sentence):
    """
    Optimized POS detection: fast suffix check, then NLTK tagging, then lemmatization, with early return. Irregular verb logic removed.
    Args:
        word (str): The word to detect POS for
        sentence (str): The sentence containing the word
    Returns:
        str: "noun", "verb", "adjective", "adverb", or None if not detected
    """
    try:
        lemmatizer = WordNetLemmatizer()
        word = word.lower().strip()
        sentence = sentence.strip()

        # 1. Fast suffix-based detection (early return if confident)
        if word.endswith(('able', 'ible', 'al', 'ful', 'ic', 'ive', 'less', 'ous')):
            return 'adjective'
        elif word.endswith('ly'):
            return 'adverb'
        elif word.endswith(('ate', 'ize', 'ise', 'ify')):
            return 'verb'

        # 2. NLTK tokenization and POS tagging
        tokens = word_tokenize(sentence)
        tagged = pos_tag(tokens)
        for token, tag in tagged:
            if token.lower() == word:
                if tag.startswith('VB'):
                    return 'verb'
                elif tag.startswith('JJ'):
                    return 'adjective'
                elif tag.startswith('RB'):
                    return 'adverb'
                elif tag.startswith('NN'):
                    return 'noun'

        # 3. Lemmatization-based inference (for verbs)
        word_lemma = lemmatizer.lemmatize(word, pos='v')
        for token, tag in tagged:
            token_lemma = lemmatizer.lemmatize(token.lower(), pos='v')
            if token_lemma == word_lemma and tag.startswith('VB'):
                return 'verb'

        # 4. Default to noun if no other patterns match
        return 'noun'

    except Exception as e:
        print(get_message("USER_INTERACTION_INPUT_VALIDATION.pos_detection_error", error=str(e)))
        return _fallback_pos_detection(word, sentence)


def _fallback_pos_detection(word, sentence):
    """
    Fallback POS detection using simple rules when NLTK fails.
    
    Args:
        word (str): The word to detect POS for
        sentence (str): The sentence containing the word
        
    Returns:
        str: "noun", "verb", "adjective", "adverb", or None if not detected
    """
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


def get_irregular_forms(word: str) -> str:
    """
    Returns a formatted string of irregular verb forms (e.g., 'flee - fled - fled') if the word is an irregular verb.
    If the word is not an irregular verb, returns an empty string.

    Args:
        word (str): The word to check
    Returns:
        str: Formatted irregular forms or empty string
    """
    key = word.lower()
    forms = irregular_verbs.get(key)
    if forms:
        return " - ".join(forms)
    return ""
