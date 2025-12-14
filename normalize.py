import re
from rapidfuzz import fuzz

KNOWN_CLUBS = [
    "barcelona", "real madrid", "manchester united", "manchester city",
    "arsenal", "liverpool", "chelsea", "psg", "juventus", "bayern"
]

KNOWN_PLAYERS = [
    "messi", "ronaldo", "neymar", "mbappe", "haaland", "benzema"
]

def normalize_query(query):
    q = query.lower()

    for club in KNOWN_CLUBS:
        if fuzz.partial_ratio(q, club) > 70:
            return {"type": "club", "value": club}

    for player in KNOWN_PLAYERS:
        if fuzz.partial_ratio(q, player) > 70:
            return {"type": "player", "value": player}

    return {"type": "unknown", "value": q}
