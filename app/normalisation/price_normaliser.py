from typing import Any, Dict

def normalise_listing(raw: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "price": float(raw["price"]),
        "currency": raw.get("currency", "USD"),
        "condition": raw.get("condition", "Unknown"),
        "seller": raw.get("seller", "Unknown"),
        "source_listing_id": raw.get("source_id"),
    }
