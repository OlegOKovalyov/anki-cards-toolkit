"""
POS (Part of Speech) detection and other linguistic utilities.
"""

import sys
import os
import nltk
from nltk import pos_tag, word_tokenize
from nltk.stem import WordNetLemmatizer
import re

# Add project root to path to allow absolute imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from data.irregular_verbs import irregular_verbs


def detect_pos_from_context(word, sentence):
    """
    Improved POS detection using NLTK's pos_tag() for more accurate tagging.
    Handles irregular verbs, inflected forms, and complex sentence structures.
    
    Args:
        word (str): The word to detect POS for
        sentence (str): The sentence containing the word
        
    Returns:
        str: "noun", "verb", "adjective", "adverb", or None if not detected
    """
    try:
        # Initialize NLTK components
        lemmatizer = WordNetLemmatizer()
        
        # Clean and prepare the word and sentence
        word = word.lower().strip()
        sentence = sentence.strip()
        
        # Tokenize the sentence
        tokens = word_tokenize(sentence)
        
        # Get POS tags for all tokens
        tagged = pos_tag(tokens)
        
        # First pass: look for exact word match (case-insensitive)
        for token, tag in tagged:
            if token.lower() == word:
                # Map Penn Treebank tags to our categories
                if tag.startswith('VB'):  # VB, VBD, VBG, VBN, VBP, VBZ
                    return 'verb'
                elif tag.startswith('JJ'):  # JJ, JJR, JJS
                    return 'adjective'
                elif tag.startswith('RB'):  # RB, RBR, RBS
                    return 'adverb'
                elif tag.startswith('NN'):  # NN, NNS, NNP, NNPS
                    return 'noun'
        
        # Second pass: check for lemmatized forms (for irregular verbs)
        word_lemma = lemmatizer.lemmatize(word, pos='v')  # Try verb lemmatization first
        
        for token, tag in tagged:
            token_lemma = lemmatizer.lemmatize(token.lower(), pos='v')
            if token_lemma == word_lemma:
                if tag.startswith('VB'):
                    return 'verb'
        
        # Third pass: check irregular verb forms
        irregular_forms = get_irregular_forms(word)
        if irregular_forms:
            # Check if any form of this irregular verb appears in the sentence
            for token, tag in tagged:
                if token.lower() in irregular_forms and tag.startswith('VB'):
                    return 'verb'
        
        # Fourth pass: check if the word is a form of an irregular verb
        for base_form, forms in irregular_verbs.items():
            if word in forms:
                # Check if this form appears as a verb in the sentence
                for token, tag in tagged:
                    if token.lower() == word and tag.startswith('VB'):
                        return 'verb'
        
        # Fifth pass: fallback to suffix-based detection for edge cases
        if word.endswith(('able', 'ible', 'al', 'ful', 'ic', 'ive', 'less', 'ous')):
            return 'adjective'
        elif word.endswith('ly'):
            return 'adverb'
        elif word.endswith(('ate', 'ize', 'ise', 'ify')):
            return 'verb'
        
        # Default to noun if no other patterns match
        return 'noun'
        
    except Exception as e:
        print(f"⚠️ Помилка при визначенні частини мови: {str(e)}")
        # Fallback to simple rule-based detection
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


def get_irregular_forms(word):
    """
    Returns a list of irregular verb forms if the word is an infinitive.
    If the word is not an irregular verb, returns None.
    
    Args:
        word (str): The word to check
        
    Returns:
        list or None: List of irregular verb forms or None
    """
    # Lower case for reliable search
    key = word.lower()
    return irregular_verbs.get(key)


def test_pos_detection():
    """Test function for POS detection with various examples"""
    test_cases = [
        ("fled", "He fled from danger", "verb"),
        ("ran", "She ran quickly", "verb"),
        ("took", "He took the book", "verb"),
        ("beautiful", "A beautiful flower", "adjective"),
        ("quickly", "She ran quickly", "adverb"),
        ("book", "I read a book", "noun"),
        ("running", "He is running fast", "verb"),
        ("happy", "She is happy", "adjective"),
        ("slowly", "He walks slowly", "adverb"),
        ("house", "The house is big", "noun"),
    ]
    
    print("🧪 Testing POS Detection:")
    print("=" * 50)
    
    for word, sentence, expected in test_cases:
        result = detect_pos_from_context(word, sentence)
        status = "✅" if result == expected else "❌"
        print(f"{status} '{word}' in '{sentence}' -> {result} (expected: {expected})")
    
    print("=" * 50)


if __name__ == "__main__":
    # Ensure NLTK data is available for standalone script execution
    try:
        nltk.download('punkt', quiet=True)
        nltk.download('punkt_tab', quiet=True)
        nltk.download('averaged_perceptron_tagger', quiet=True)
        nltk.download('averaged_perceptron_tagger_eng', quiet=True)
        nltk.download('wordnet', quiet=True)
        nltk.download('omw-1.4', quiet=True)
    except Exception as e:
        print(f"⚠️ Could not download NLTK data for testing: {e}")

    # Run tests
    test_pos_detection() 