from app.normalisation.rarity_map import RARITY_MAP

def normalise_rarity(raw_rarity: str) -> str:
    """
    Convert raw API rarity values into canonical rarity names.
    Falls back to the raw value if no mapping exists.
    """

    if not raw_rarity:
        return None

    canonical = RARITY_MAP.get(raw_rarity)
    return canonical if canonical else raw_rarity
