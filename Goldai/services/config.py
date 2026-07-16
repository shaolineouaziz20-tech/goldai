from services.forex_factory import fetch_forex_factory_news


def fetch_news():

    try:
        return fetch_forex_factory_news()

    except Exception as e:
        print("News Engine Error:", e)
        return []