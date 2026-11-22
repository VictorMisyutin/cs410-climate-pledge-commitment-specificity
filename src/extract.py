import re

import pymupdf


def read_pdf(path):
    pages = []

    with pymupdf.open(path) as doc:
        for i, page in enumerate(doc, start=1):
            blocks = page.get_text("blocks")
            texts = [b[4] for b in blocks if b[6] == 0]
            pages.append((i, texts))

    return pages


def clean_text(text):
    text = re.sub(r"-\n(?=[a-z])", "", text)
    lines = [ln.strip() for ln in text.splitlines()]
    lines = [ln for ln in lines if ln and not ln.isdigit()]
    return " ".join(lines)


def split_sentences(text):
    # TODO: handle abbreviations like "e.g." and "Inc."
    
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z])", text)
    return [p.strip() for p in parts if len(p.split()) >= 5]


def pdf_to_sentences(path, max_words=60):
    result = []
    
    for page_num, blocks in read_pdf(path):
        for block in blocks:
            for piece in re.split(r"\s*[•●▪]\s*", clean_text(block)):
                for sentence in split_sentences(piece):
                    if len(sentence.split()) <= max_words:
                        result.append((page_num, sentence))

    return result

