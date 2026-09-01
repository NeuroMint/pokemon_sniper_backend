from app.normalisation.set_map import SET_NAME_MAP

def normalise_set(raw_set_name: str) -> str:
    """
    Convert raw API set name into canonical set name.
    Falls back to the raw value if no mapping exists.
    """

    if not raw_set_name:
        return "Unknown Set"

    canonical = SET_NAME_MAP.get(raw_set_name)
    return canonical if canonical else raw_set_name
