import re

ALIASES = {
    "barca": "barcelona",
    "man utd": "manchester united",
    "man united": "manchester united",
    "psg": "paris saint germain",
    "rm": "real madrid",
}

def normalize(text: str):
    text = text.lower()
    text = re.sub(r"[^a-z\s]", "", text)

    for k, v in ALIASES.items():
        if k in text:
            return v

    return text.strip()
