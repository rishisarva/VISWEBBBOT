import re
from rapidfuzz import fuzz

COMMON_CLUB_WORDS = [
    "barcelona", "barca",
    "real madrid", "madrid",
    "manchester united", "man utd", "man united",
    "arsenal",
    "chelsea",
    "liverpool",
    "psg", "paris",
    "juventus",
    "bayern",
    "ac milan", "inter",
]

def clean(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9 ]', '', text)
    return text.strip()

def detect_club_from_title(title):
    title_clean = clean(title)
    best_match = None
    best_score = 0

    for club in COMMON_CLUB_WORDS:
        score = fuzz.partial_ratio(title_clean, club)
        if score > best_score:
            best_score = score
            best_match = club

    return best_match if best_score > 60 else None


def group_by_club(products):
    grouped = {}

    for p in products:
        club = detect_club_from_title(p["name"])
        if not club:
            continue

        grouped.setdefault(club, []).append(p)

    return grouped
