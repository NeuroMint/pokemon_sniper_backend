import requests
import unicodedata
import time
from bs4 import BeautifulSoup
import os

BASE_URL = "https://www.ebay.com.au/sch/i.html"

EBAY_CLIENT_ID = os.getenv("EBAY_CLIENT_ID")
EBAY_CLIENT_SECRET = os.getenv("EBAY_CLIENT_SECRET")


def normalize_query(text: str) -> str:
    """
    Convert unicode → ASCII, remove punctuation that breaks eBay search,
    and ensure the query is safe for Cloudflare.
    """
    # Normalize unicode (é → e, — → -, etc.)
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")

    # Replace problematic punctuation
    text = text.replace("—", " ")
    text = text.replace("-", " ")
    text = text.replace("  ", " ")

    return text.strip()


def fetch_ebay_au_prices(card_name: str, set_name: str | None = None):
    # Normalize search query
    query = normalize_query(card_name)
    if set_name:
        query += f" {normalize_query(set_name)}"

    params = {
        "_nkw": query,
        "_sacat": 0,
        "LH_Sold": "1",      # sold listings = real market price
        "LH_Complete": "1",  # completed listings
    }

    # Browser headers to bypass Cloudflare bot detection
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
    }

    # Retry logic for 403 / Cloudflare blocks
    for attempt in range(3):
        resp = requests.get(BASE_URL, params=params, headers=headers, timeout=10)

        if resp.status_code == 200:
            break

        print(f"[WARN] eBay AU returned {resp.status_code} for query '{query}' (attempt {attempt+1}/3)")
        time.sleep(1)

    # If still blocked after retries
    if resp.status_code != 200:
        print(f"[SKIP] eBay AU blocked query '{query}' after 3 attempts")
        return []

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
