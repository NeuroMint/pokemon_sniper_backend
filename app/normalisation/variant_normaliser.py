from app.normalisation.variant_map import VARIANT_MAP

def normalise_variant(subtypes: list[str]) -> str:

    if not subtypes:
        return None

    for subtype in subtypes:
        if subtype in VARIANT_MAP:
            return VARIANT_MAP[subtype]

    # fallback: return first subtype
    return subtypes[0]
