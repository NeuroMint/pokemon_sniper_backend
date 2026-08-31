import time
import random
import requests
import os
from sqlalchemy.orm import Session

from app.services.ingestion import ingest_card
from app.services.price_ingestion import ingest_prices_for_card

print("RUNNING FILE:", os.path.abspath(__file__))

API_URL = "https://api.pokemontcg.io/v2/cards"
PAGE_SIZE = 250


def fetch_cards_page(page: int, retries: int = 3600):
    url = f"{API_URL}?page={page}&pageSize={PAGE_SIZE}"

    for attempt in range(1, retries + 1):
        headers = {
            "User-Agent": f"Mozilla/5.0 (ScraperBot-{random.randint(1000,9999)})"
        }

        response = requests.get(url, headers=headers)

        try:
            data = response.json()
            return data.get("data", [])
        except Exception:
            print(f"TCG API returned non‑JSON response on page {page}, attempt {attempt}")

            backoff = (2 ** attempt) * 0.3
            jitter = random.uniform(0.1, 0.4)
            sleep_time = backoff + jitter

            print(f"Sleeping {sleep_time:.2f}s before retrying page {page}...")
            time.sleep(sleep_time)

    print(f"❌ Failed to fetch page {page} after {retries} retries")
    return []


def fetch_all_cards():
    all_cards = []
    page = 1

    while True:
        raw_cards = fetch_cards_page(page)
        print(f"Page {page} count:", len(raw_cards))

        if not raw_cards:
            print("⚠️ No more cards returned — stopping pagination")
            break

        all_cards.extend(raw_cards)
        page += 1

    print(f"Total cards fetched: {len(all_cards)}")
    return all_cards


def fetch_listings_for_card(card_data: dict) -> list[dict]:
    prices = card_data.get("tcgplayer", {}).get("prices", {})
    listings = []

    for variant, price_info in prices.items():
        market_price = price_info.get("market")
        if market_price:
            listings.append({
                "price": market_price,
                "currency": "USD",
                "condition": variant,
                "seller": "tcgplayer",
                "source_listing_id": f"{card_data.get('id')}-{variant}"
            })

    return listings


def run_tcg_api_scraper(db: Session):
    raw_cards = fetch_all_cards()

    for raw in raw_cards:
        normalized = {
            "name": raw.get("name"),
            "set_name": raw.get("set", {}).get("name"),
            "card_number": raw.get("number"),
            "rarity": raw.get("rarity"),
            "language": "EN",
            "variant": raw.get("subtypes", [None])[0],
            "image_url": raw.get("images", {}).get("large")
        }

        card = ingest_card(db, normalized, source="tcg_api")

        # ⭐ This is the correct connection between scraper → ingestion
        ingest_prices_for_card(db, card, raw)
