import re

def extract_number(card_number: str) -> str:
    """Extract numeric part from card number like '045/165' or '45a'."""
    match = re.search(r"\d+", card_number)
    return match.group(0) if match else None


def extract_suffix(card_number: str) -> str:
    """Extract suffix (like 'a', 'b', etc.) from card number."""
    match = re.search(r"[A-Za-z]+$", card_number)
    return match.group(0) if match else None
