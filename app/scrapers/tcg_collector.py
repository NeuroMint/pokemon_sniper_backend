import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.tcgcollector.com.au"

def fetch_tcg_collectors_prices(card_name: str, set_name: str | None = None):
    query = card_name
    if set_name:
        query += f" {set_name}"

    url = f"{BASE_URL}/search?q={query}"
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    prices = []

    # TODO: adjust selectors once you inspect the page structure
    for row in soup.select(".price-row"):
        price_text = row.select_one(".price").get_text(strip=True)
        condition_text = row.select_one(".condition").get_text(strip=True)

        # convert "$12.50" → 12.50
        price = float(price_text.replace("$", "").replace(",", ""))

        prices.append({
            "price": price,
            "currency": "AUD",
            "condition": condition_text,
            "seller": "tcgcollector",
            "source_listing_id": row.get("data-id", None),
        })

    return prices
