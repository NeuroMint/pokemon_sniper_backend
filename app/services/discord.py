import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

def send_discord_alert(webhook_url: str, snipe: dict):
    content = (
        f"🔥 **New Snipe Detected!**\n"
        f"Card ID: {snipe['card_id']}\n"
        f"Listing ID: {snipe['listing_id']}\n"
        f"Price: ${snipe['price']}\n"
        f"Avg Price: ${snipe['avg_price']}\n"
        f"Discount: {int(snipe['discount'] * 100)}%\n"
        f"Source: {snipe['source_listing_id']}"
    )

    payload = {"content": content}
    requests.post(webhook_url, data=json.dumps(payload), headers={"Content-Type": "application/json"})
