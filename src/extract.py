"""Step 1: turn a sustainability report PDF into a list of sentences."""

import re

import pymupdf


def read_pdf(path):
    """Return a list of (page_number, [text blocks]) for each page.

    PyMuPDF groups text into blocks (paragraphs, bullet items, table cells),
    so columns in multi-column layouts stay separate instead of being
    read straight across the page.
    """
    pages = []
    with pymupdf.open(path) as doc:
        for i, page in enumerate(doc, start=1):
            blocks = page.get_text("blocks")
            texts = [b[4] for b in blocks if b[6] == 0]  # b[6] == 0 means a text block (not an image)
            pages.append((i, texts))
    return pages


def clean_text(text):
    """Join lines that were wrapped by the PDF layout and drop obvious noise."""
    text = re.sub(r"-\n(?=[a-z])", "", text)        # re-join hyphenated words
    lines = [ln.strip() for ln in text.splitlines()]
    lines = [ln for ln in lines if ln and not ln.isdigit()]  # drop page numbers
    return " ".join(lines)


def split_sentences(text):
    """Simple rule-based splitter: break after . ! ? when followed by a capital letter.

    TODO: handle abbreviations like "e.g." and "Inc."
    """
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z])", text)
    return [p.strip() for p in parts if len(p.split()) >= 5]


def pdf_to_sentences(path, max_words=60):
    """Return a list of (page_number, sentence).

    Each text block is split on bullet characters and then into sentences.
    Anything longer than max_words is almost always a table or a run of
    merged bullets, so it is dropped.
    """
    result = []
    for page_num, blocks in read_pdf(path):
        for block in blocks:
            for piece in re.split(r"\s*[•●▪]\s*", clean_text(block)):
                for sentence in split_sentences(piece):
                    if len(sentence.split()) <= max_words:
                        result.append((page_num, sentence))
    return result
