"""Step 2: keep only sentences that look like environmental commitments.

A sentence counts if it mentions an environmental topic AND uses
forward-looking commitment language. This is a first version, and the
word lists will need tuning once I look at real reports.
"""

import re

TOPIC_WORDS = [
    "emission", "carbon", "co2", "greenhouse", "ghg", "climate", "net zero",
    "net-zero", "renewable", "energy", "waste", "recycl", "plastic",
    "packaging", "water", "scope 1", "scope 2", "scope 3",
    "deforestation", "methane", "netzero", "fuel", "electricity", "biodiversity",
]

COMMITMENT_PATTERNS = [
    r"\bwe (will|aim to|plan to|intend to|commit to|strive to|seek to|hope to)\b",
    r"\b(are|is|remain) committed to\b",
    r"\b(our|the) (goal|target|ambition|commitment) (is|of|to)\b",
    r"\bby 20[2-9]\d\b",
    r"\bcontinue to\b",
]


SKIP_WORDS = ["scenario", "rcp", "ssp", "ipcc", "projected to"]


def is_commitment(sentence):
    s = sentence.lower()
    if any(word in s for word in SKIP_WORDS):  # climate scenario descriptions, not pledges
        return False
    has_topic = any(word in s for word in TOPIC_WORDS)
    has_commitment = any(re.search(p, s) for p in COMMITMENT_PATTERNS)
    return has_topic and has_commitment