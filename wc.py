import requests
import os

WC_KEY = os.getenv("WC_KEY")
WC_SECRET = os.getenv("WC_SECRET")
WC_URL = os.getenv("WC_URL")

def fetch_products():
    url = f"{WC_URL}/wp-json/wc/v3/products"
    params = {
        "per_page": 100,
        "status": "publish"
    }
    r = requests.get(url, auth=(WC_KEY, WC_SECRET), params=params)
    r.raise_for_status()
    return r.json()
