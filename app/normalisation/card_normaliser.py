from app.normalisation.set_normaliser import normalise_set
from app.normalisation.set_lookup import get_set_id

from app.normalisation.rarity_normaliser import normalise_rarity
from app.services.rarity_lookup import get_rarity_id

from app.normalisation.variant_normaliser import normalise_variant
from app.services.variant_lookup import get_variant_id

from app.normalisation.number_extractor import extract_number, extract_suffix
from app.normalisation.name_normaliser import normalise_name

from app.services.language_lookup import get_language_id


def normalise_card(raw: dict, db):
    # --- Set ---
    raw_set_name = raw.get("set", {}).get("name", "Unknown Set")
    canonical_set = normalise_set(raw_set_name)
    set_id = get_set_id(db, canonical_set)

    # --- Rarity ---
    raw_rarity = raw.get("rarity")
    canonical_rarity = normalise_rarity(raw_rarity)
    rarity_id = get_rarity_id(db, canonical_rarity)

    # --- Variant ---
    raw_subtypes = raw.get("subtypes", [])
    canonical_variant = normalise_variant(raw_subtypes)
    variant_id = get_variant_id(db, canonical_variant)

    # --- Name ---
    name = normalise_name(raw.get("name", ""))
    canonical_name = name  # already lowercase + cleaned

    # --- Language ---
    language = "EN"
    language_id = get_language_id(db, language)

    # --- Number + Suffix ---
    raw_number = raw.get("number", "")
    number = extract_number(raw_number)
    suffix = extract_suffix(raw_number)

    # --- Card Number (full raw number) ---
    card_number = raw_number

    # --- Images ---
    images = raw.get("images", {})
    image_large = images.get("large")
    image_small = images.get("small")

    return {
        "name": name,
        "canonical_name": canonical_name,

        "set_id": set_id,
        "rarity_id": rarity_id,
        "variant_id": variant_id,

        "language": language,
        "language_id": language_id,

        "number": number,
        "suffix": suffix,
        "card_number": card_number,

        "image_large": image_large,
        "image_small": image_small,
    }
