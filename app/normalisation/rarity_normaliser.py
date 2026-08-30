from app.normalisation.rarity_map import RARITY_MAP

def normalise_rarity(raw_rarity: str) -> str:
    if raw_rarity in RARITY_MAP:
        return RARITY_MAP[raw_rarity]

    return raw_rarity
