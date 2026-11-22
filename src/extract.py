"""Step 1: turn a sustainability report PDF into a list of sentences."""

import re

import pdfplumber


def read_pdf(path):
    """Return a list of (page_number, text) for each page."""
    pages = []
    with pdfplumber.open(path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            pages.append((i, page.extract_text() or ""))
    return pages


def clean_text(text):
    """Join lines that were wrapped by the PDF layout and drop obvious noise."""
    text = re.sub(r"\(cid:\d+\)", " ", text)       # unmapped glyphs (often bullets)
    text = re.sub(r"-\n(?=[a-z])", "", text)        # re-join hyphenated words
    lines = [ln.strip() for ln in text.splitlines()]
    lines = [ln for ln in lines if ln and not ln.isdigit()]  # drop page numbers
    return " ".join(lines)


def split_sentences(text):
    """Simple rule-based splitter: break after . ! ? when followed by a capital letter.

    TODO: handle abbreviations like "e.g." and "Inc.", bullet lists without
    periods, and section headings that get glued onto the next sentence.
    """
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z])", text)
    return [p.strip() for p in parts if len(p.split()) >= 5]


def pdf_to_sentences(path):
    """Return a list of (page_number, sentence)."""
    result = []
    for page_num, text in read_pdf(path):
        for sentence in split_sentences(clean_text(text)):
            result.append((page_num, sentence))
    return result
