import time
import random
import os
from sqlalchemy.orm import Session
from tls_client import Session as TLS_Session

from app.services.ingestion import ingest_card
from app.services.price_ingestion import ingest_prices_for_card

# --- Colour Class ---
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


def fetch_cards_page(page: int, retries: int = 5):
    url = f"{API_URL}?page={page}&pageSize={PAGE_SIZE}&include=tcgplayer"

    for attempt in range(1, retries + 1):

        # --- Rotate TLS fingerprint ---
        session = TLS_Session(
            client_identifier=random.choice([
                "chrome_127",
                "chrome_126",
                "chrome_125",
                "firefox_128",
            ])
        )

        # --- Rotate headers ---
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept-Language": random.choice([
                "en-US,en;q=0.9",
                "en-AU,en;q=0.8",
                "en-GB,en;q=0.7",
            ]),
            "Accept-Encoding": "gzip, deflate, br",
            "sec-ch-ua": '"Chromium";v="127", "Not=A?Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": random.choice(["Windows", "macOS", "Linux"]),
            "sec-fetch-site": "none",
            "sec-fetch-mode": "navigate",
            "sec-fetch-user": "?1",
            "sec-fetch-dest": "document",
        }

        # --- TLS-client request with retry ---
        try:
            response = session.get(url, headers=headers)

        except Exception as e:
            print(f"{C.RED}[SNIPER] TLS-client error on page {page}, attempt {attempt}: {e}{C.RESET}")

            backoff = (2 ** attempt) * 0.3
            jitter = random.uniform(0.2, 0.9)
            sleep_time = backoff + jitter

            print(f"{C.BLUE}[SNIPER] Sleeping {sleep_time:.2f}s before retrying page {page}...{C.RESET}")
            time.sleep(sleep_time)
            continue

        # --- JSON parsing ---
        try:
            data = response.json()
            return data.get("data", [])

        except Exception:
            print(f"{C.YELLOW}[SNIPER] Non‑JSON response on page {page}, attempt {attempt}{C.RESET}")

            backoff = (2 ** attempt) * 0.3
            jitter = random.uniform(0.2, 0.9)
            sleep_time = backoff + jitter

            print(f"{C.BLUE}[SNIPER] Sleeping {sleep_time:.2f}s before retrying page {page}...{C.RESET}")
            time.sleep(sleep_time)

    print(f"{C.RED}[SNIPER] ❌ Failed to fetch page {page} after {retries} retries{C.RESET}")
    return []


def fetch_all_cards():
    all_cards = []
    page = 1

    while True:
        raw_cards = fetch_cards_page(page)
        print(f"{C.CYAN}[SNIPER] Page {page} count: {len(raw_cards)}{C.RESET}")

        if not raw_cards:
            print(f"{C.MAGENTA}[SNIPER] ⚠️ No more cards returned — stopping pagination{C.RESET}")
            break

        all_cards.extend(raw_cards)
        page += 1

    print(f"{C.GREEN}[SNIPER] Total cards fetched: {len(all_cards)}{C.RESET}")
    return all_cards


def run_tcg_api_scraper(db: Session):
    raw_cards = fetch_all_cards()

    for raw in raw_cards:
        card = ingest_card(db, raw, source="tcg_api")
        ingest_prices_for_card(db, card)
