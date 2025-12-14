CLUB_ALIASES = {
    "barcelona": ["barca", "fc barcelona", "fcb"],
    "real madrid": ["rm", "realmadrid"],
    "manchester united": ["man utd", "man united", "manu"],
    "psg": ["paris", "paris saint germain"],
    "arsenal": ["arsenal fc"],
}

def normalize_query(query: str) -> str:
    query = query.lower().strip()

    for canonical, aliases in CLUB_ALIASES.items():
        if query == canonical:
            return canonical
        if query in aliases:
            return canonical

    return query
