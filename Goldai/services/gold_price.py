import requests

def get_gold_price():
    try:
        url = "https://api.gold-api.com/price/XAU"

        response = requests.get(url, timeout=10)

        data = response.json()

        return round(data["price"], 2)

    except Exception:
        return None