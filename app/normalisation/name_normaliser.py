import re

def normalise_name(name: str) -> str:
    """
    Clean and standardise card names for consistent identity matching.
    Removes extra whitespace, punctuation, and normalises casing.
    """
    if not name:
        return None

    # Trim whitespace and convert to lowercase
    cleaned = name.strip().lower()

    # Remove special characters (like dashes, apostrophes, etc.)
    cleaned = re.sub(r"[^a-z0-9\s]", "", cleaned)

    # Collapse multiple spaces
    cleaned = re.sub(r"\s+", " ", cleaned)

    return cleaned
