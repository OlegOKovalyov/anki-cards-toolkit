import pytest
from src.utils.highlight import highlight_focus_word

@pytest.mark.parametrize("sentence, focus_word, pos, expected", [
    (
        "These invaders were destructive in their conquests.",
        "conquest",
        'n',
        "These invaders were destructive in their <span style=\"color:orange;font-weight:bold\">conquests</span>."
    ),
    (
        "She runs and he ran.",
        "run",
        'v',
        "She <span style=\"color:orange;font-weight:bold\">runs</span> and he <span style=\"color:orange;font-weight:bold\">ran</span>."
    ),
    (
        "It was a beautiful, beautiful day.",
        "beautiful",
        'a',
        "It was a <span style=\"color:orange;font-weight:bold\">beautiful</span>, <span style=\"color:orange;font-weight:bold\">beautiful</span> day."
    ),
])
def test_highlight_focus_word(sentence, focus_word, pos, expected):
    assert highlight_focus_word(sentence, focus_word, pos) == expected 