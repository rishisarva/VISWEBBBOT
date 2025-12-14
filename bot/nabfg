from rapidfuzz import fuzz
from normalize import normalize

def search_products(products, query, limit=5):
    q = normalize(query)
    scored = []

    for p in products:
        title = normalize(p["name"])
        score = fuzz.partial_ratio(q, title)
        if score > 60:
            scored.append((score, p))

    scored.sort(reverse=True, key=lambda x: x[0])
    return [p for _, p in scored[:limit]]
