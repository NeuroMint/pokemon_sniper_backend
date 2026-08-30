from app.normalisation.set_map import SET_NAME_MAP

def normalise_set(raw_set_name: str) -> str:
    """
    Convert raw API set name into canonical set name.
    """
    if raw_set_name in SET_NAME_MAP:
        return SET_NAME_MAP[raw_set_name]

    # fallback: return raw name as-is
    return raw_set_name
