# woo.py
import requests

def fetch_products(query, wc_url, wc_key, wc_secret, limit=5):
    url = f"{wc_url}/wp-json/wc/v3/products"
    params = {
        "search": query,
        "per_page": limit,
        "consumer_key": wc_key,
        "consumer_secret": wc_secret,
    }
    r = requests.get(url, params=params, timeout=15)
    r.raise_for_status()
    return r.json()
