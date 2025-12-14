import requests
from functools import lru_cache
from os import getenv

WC_URL = getenv("WC_URL")
CK = getenv("WC_CONSUMER_KEY")
CS = getenv("WC_CONSUMER_SECRET")

@lru_cache(maxsize=1)
def get_products():
    products = []
    page = 1
    while True:
        r = requests.get(
            f"{WC_URL}/wp-json/wc/v3/products",
            auth=(CK, CS),
            params={"per_page": 100, "page": page},
        )
        data = r.json()
        if not data:
            break
        products.extend(data)
        page += 1
    return products
