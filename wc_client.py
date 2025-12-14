import requests
import os

WC_URL = os.getenv("WC_URL")
WC_KEY = os.getenv("WC_KEY")
WC_SECRET = os.getenv("WC_SECRET")

def fetch_products():
    url = f"{WC_URL}/wp-json/wc/v3/products"
    r = requests.get(url, auth=(WC_KEY, WC_SECRET), params={"per_page": 100})
    r.raise_for_status()
    return r.json()
