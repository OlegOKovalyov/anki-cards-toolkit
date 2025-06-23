import re
from nltk.stem import WordNetLemmatizer

def highlight_focus_word(sentence, focus_word, pos='n'):
    """
    Highlights all occurrences of the focus word in the sentence, matching by lemma and part of speech.
    Args:
        sentence (str): The sentence to process.
        focus_word (str): The word to highlight.
        pos (str): Part of speech for lemmatization ('n', 'v', 'a', 'r'). Defaults to 'n' (noun).
    Returns:
        str: The sentence with the focus word highlighted.
    """
    lemmatizer = WordNetLemmatizer()
    focus_lemma = lemmatizer.lemmatize(focus_word.lower(), pos=pos)

    def replacer(match):
        token = match.group(0)
        token_lemma = lemmatizer.lemmatize(token.lower(), pos=pos)
        if token_lemma == focus_lemma:
            return f'<span style="color:orange;font-weight:bold">{token}</span>'
        return token

    return re.sub(r'\b\w+\b', replacer, sentence, flags=re.IGNORECASE) 