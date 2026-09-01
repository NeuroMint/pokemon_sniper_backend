import re

def extract_number(card_number: str) -> str | None:
    """
    Extract the numeric portion of a card number.
    Examples:
        '045/165' → '045'
        '45a'     → '45'
        '123'     → '123'
    """
    if not card_number:
        return None

    match = re.search(r"\d+", card_number)
    return match.group(0) if match else None


def extract_suffix(card_number: str) -> str | None:
    """
    Extract the alphabetical suffix from a card number.
    Examples:
        '45a' → 'a'
        '123b' → 'b'
        '045/165' → None
    """
    if not card_number:
        return None

    match = re.search(r"[A-Za-z]+$", card_number)
    return match.group(0) if match else None
