import os
import requests

# Load your Sandbox user token
EBAY_SANDBOX_TOKEN = os.getenv("EBAY_SANDBOX_TOKEN")

# Sandbox Browse API endpoint
BROWSE_URL = "https://api.sandbox.ebay.com/buy/browse/v1/item_summary/search"


def get_token():
    """
    Sandbox Browse API requires a USER TOKEN, not client_credentials.
    We simply return the long sandbox token from the .env file.
    """
    return EBAY_SANDBOX_TOKEN


def search_ebay_prices(card_name: str, set_name: str | None = None):
    """
    Search eBay using the official Browse API (Sandbox).
    Returns clean price objects compatible with your ingestion pipeline.
    """

    token = get_token()

    query = card_name
    if set_name:
        query += f" {set_name}"

    params = {
        "q": query,
        "limit": 50,
        "filter": "buyingOptions:{FIXED_PRICE}",
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    resp = requests.get(BROWSE_URL, params=params, headers=headers)
    resp.raise_for_status()

    data = resp.json()
    results = []

    for item in data.get("itemSummaries", []):
        price_info = item.get("price", {})
        seller_info = item.get("seller", {})

        results.append({
            "price": float(price_info.get("value", 0)),
            "currency": price_info.get("currency", "AUD"),
            "condition": item.get("condition", "unknown"),
            "seller": seller_info.get("username", "ebay"),
            "source_listing_id": item.get("itemId"),
        })

    return results
