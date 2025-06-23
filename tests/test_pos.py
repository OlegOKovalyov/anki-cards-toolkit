import pytest
from src.linguistics.pos import detect_pos_from_context

@pytest.mark.parametrize("word,sentence,expected", [
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
])
def test_detect_pos(word, sentence, expected):
    assert detect_pos_from_context(word, sentence) == expected 