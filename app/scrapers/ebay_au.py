import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.ebay.com.au/sch/i.html"

def fetch_ebay_au_prices(card_name: str, set_name: str | None = None):
    query = card_name
    if set_name:
        query += f" {set_name}"

    params = {
        "_nkw": query,
        "_sacat": 0,
        "LH_Sold": "1",      # sold listings = real market price
        "LH_Complete": "1",  # completed listings
    }

    resp = requests.get(BASE_URL, params=params, timeout=10)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    prices = []

    # EBay AU sold listings selector
    items = soup.select(".s-item")

    for item in items:
        price_el = item.select_one(".s-item__price")
        title_el = item.select_one(".s-item__title")
        link_el = item.select_one(".s-item__link")

        if not price_el or not title_el or not link_el:
            continue

        price_text = price_el.get_text(strip=True)

        # Convert "$12.50" → 12.50
        try:
            price = float(price_text.replace("$", "").replace(",", ""))
        except:
            continue

        listing_id = link_el.get("href")

        prices.append({
            "price": price,
            "currency": "AUD",
            "condition": "sold",  # EBay sold listings = real market
            "seller": "ebay_au",
            "source_listing_id": listing_id,
        })

    return prices
