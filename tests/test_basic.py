import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from commitments import is_commitment  # noqa: E402
from extract import clean_text, split_sentences  # noqa: E402


def test_split_sentences():
    text = "We will cut emissions by 40% by 2030. Revenue grew strongly across all regions this year."
    assert len(split_sentences(text)) == 2


def test_clean_text_rejoins_hyphenated_words():
    assert "emissions" in clean_text("We will reduce emis-\nsions by 2030.\n12")


def test_is_commitment():
    assert is_commitment("We aim to reduce our carbon emissions by 30% by 2030.")
    assert is_commitment("We are committed to reducing waste across our operations.")
    assert not is_commitment("Revenue grew 8% to $4.2 billion in 2023.")
    assert not is_commitment("Climate change poses risks to agricultural supply chains.")
