from playwright.sync_api import sync_playwright


def fetch_forex_factory_news():

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)

        page = browser.new_page()

        page.goto(
            "https://www.forexfactory.com/calendar",
            wait_until="domcontentloaded",
            timeout=60000
        )

        print("Forex Factory OK")

        browser.close()

    return []