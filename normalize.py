# normalize.py

ALIASES = {
    "barca": "barcelona",
    "fc barcelona": "barcelona",
    "man utd": "manchester united",
    "man united": "manchester united",
    "manu": "manchester united",
    "psg": "paris saint germain",
    "rm": "real madrid",
}

def normalize_query(text: str) -> str:
    text = text.lower().strip()
    return ALIASES.get(text, text)
