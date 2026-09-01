from app.normalisation.variant_map import VARIANT_MAP

def normalise_variant(subtypes: list[str]) -> str | None:
    """
    Convert raw API subtypes into canonical variant names.
    Returns None if no variant applies.
    """

    if not subtypes:
        return None

    # Prefer canonical mappings
    for subtype in subtypes:
        if subtype in VARIANT_MAP:
            return VARIANT_MAP[subtype]

    # Fallback: return first subtype as-is
    return subtypes[0]
