print("[DEBUG] Loaded tcg_api.py from:", __file__)

import time
import random
import os
from sqlalchemy.orm import Session
from tls_client import Session as TLS_Session

from app.services.ingestion import ingest_card
from app.services.price_ingestion import ingest_prices_for_card

class C:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    RESET = "\033[0m"

print(f"{C.MAGENTA}[SNIPER] Running file: {os.path.abspath(__file__)}{C.RESET}")

API_URL = "https://api.pokemontcg.io/v2/cards"
PAGE_SIZE = 250

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
]

def create_tls_session():
    tls = TLS_Session(
        client_identifier=random.choice([
            "chrome_131",
            "chrome_130",
            "chrome_129",
            "firefox_130",
            "safari_17_0",
        ])
    )
    print("[DEBUG] Created new TLS session with fingerprint:", tls.client_identifier)
    return tls

def fetch_cards_page(tls, page: int, retries: int = 5):
    url = f"{API_URL}?page={page}&pageSize={PAGE_SIZE}&include=tcgplayer"

    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "application/json",
        "Accept-Language": random.choice([
            "en-US,en;q=0.9",
            "en-AU,en;q=0.8",
            "en-GB,en;q=0.7",
        ]),
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Origin": "https://api.pokemontcg.io",
        "Referer": "https://api.pokemontcg.io/",
    }

    for attempt in range(1, retries + 1):
        try:
            response = tls.get(url, headers=headers)
        except Exception as e:
            print(f"{C.RED}[SNIPER] TLS error on page {page}, attempt {attempt}: {e}{C.RESET}")
            sleep = (2 ** attempt) * 0.3 + random.uniform(0.2, 0.9)
            print(f"{C.BLUE}[SNIPER] Sleeping {sleep:.2f}s...{C.RESET}")
            time.sleep(sleep)
            continue

        try:
            data = response.json()
            cards = data.get("data", [])

            if cards:
                return cards

            print(f"{C.YELLOW}[SNIPER] Empty page {page}, attempt {attempt}{C.RESET}")
            sleep = (2 ** attempt) * 0.3 + random.uniform(0.2, 0.9)
            print(f"{C.BLUE}[SNIPER] Sleeping {sleep:.2f}s...{C.RESET}")
            time.sleep(sleep)

        except Exception:
            print(f"{C.YELLOW}[SNIPER] Non‑JSON response on page {page}, attempt {attempt}{C.RESET}")
            print("[DEBUG] Raw response text:")
            print(response.text[:500])
            sleep = (2 ** attempt) * 0.3 + random.uniform(0.2, 0.9)
            print(f"{C.BLUE}[SNIPER] Sleeping {sleep:.2f}s...{C.RESET}")
            time.sleep(sleep)

    print(f"{C.RED}[SNIPER] ❌ Failed page {page} after {retries} retries{C.RESET}")
    return []


def fetch_all_cards():
    all_cards = []
    page = 1
    tls = create_tls_session()
    pages_in_batch = 0
    consecutive_empty = 0

    while page <= 2000:
        raw_cards = fetch_cards_page(tls, page)
        print(f"{C.CYAN}[SNIPER] Page {page} count: {len(raw_cards)}{C.RESET}")

        if not raw_cards:
            consecutive_empty += 1
            if consecutive_empty >= 3:
                print(f"{C.MAGENTA}[SNIPER] ⚠️ No more cards after {consecutive_empty} empty pages — stopping pagination{C.RESET}")
                print(f"{C.GREEN}[SNIPER] Total cards fetched: {len(all_cards)}{C.RESET}")
                return all_cards
            page += 1
            continue

        consecutive_empty = 0
        all_cards.extend(raw_cards)
        page += 1
        pages_in_batch += 1

        time.sleep(1.2)

        if pages_in_batch >= 5:
            print(f"{C.BLUE}[SNIPER] Cooling down before next batch...{C.RESET}")
            time.sleep(5)
            tls = create_tls_session()
            pages_in_batch = 0

    print(f"{C.GREEN}[SNIPER] Reached MAX_PAGES — stopping. Total cards fetched: {len(all_cards)}{C.RESET}")
    return all_cards


def run_tcg_api_scraper(db: Session):
    raw_cards = fetch_all_cards()

    for raw in raw_cards:
        card = ingest_card(db, raw, source="tcg_api")
        ingest_prices_for_card(db, card)
