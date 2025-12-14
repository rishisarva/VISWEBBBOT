import requests

WC_API_URL = "https://visionsjersey.com/wp-json/wc/v3/products"
WC_KEY = "YOUR_CONSUMER_KEY"
WC_SECRET = "YOUR_CONSUMER_SECRET"

def fetch_products(search_term, limit=5):
    params = {
        "search": search_term,
        "per_page": limit,
        "consumer_key": WC_KEY,
        "consumer_secret": WC_SECRET
    }

    response = requests.get(WC_API_URL, params=params)
    response.raise_for_status()
    return response.json()
