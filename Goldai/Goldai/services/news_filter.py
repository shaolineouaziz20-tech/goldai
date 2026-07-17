USD_EVENTS = [
    "FOMC",
    "Federal",
    "Fed",
    "Powell",
    "CPI",
    "Core CPI",
    "PPI",
    "Core PPI",
    "PCE",
    "Core PCE",
    "NFP",
    "Non-Farm",
    "Retail Sales",
    "GDP",
    "Unemployment",
    "Interest Rate",
    "ISM",
    "PMI"
]


def is_gold_news(event_name):

    event = event_name.lower()

    for keyword in USD_EVENTS:

        if keyword.lower() in event:
            return True

    return False