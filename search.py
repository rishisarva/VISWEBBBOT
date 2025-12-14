from rapidfuzz import fuzz

def extract_sizes(product):
    sizes = []
    for attr in product.get("attributes", []):
        if attr["name"].lower() == "size":
            sizes = attr["options"]
    return sizes

def rank_products(products, query_obj):
    results = []

    for p in products:
        title = p["name"].lower()
        score = fuzz.partial_ratio(query_obj["value"], title)

        if query_obj["type"] == "player" and query_obj["value"] in title:
            score += 30
        if query_obj["type"] == "club" and query_obj["value"] in title:
            score += 20

        if score > 60:
            results.append((score, p))

    results.sort(reverse=True, key=lambda x: x[0])
    return [p for _, p in results]
