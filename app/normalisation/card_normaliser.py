from app.normalisation.set_normaliser import normalise_set
from app.normalisation.set_lookup import get_set_id

from app.normalisation.rarity_normaliser import normalise_rarity
from app.services.rarity_lookup import get_rarity_id

from app.normalisation.variant_normaliser import normalise_variant
from app.services.variant_lookup import get_variant_id

from app.normalisation.number_extractor import extract_number, extract_suffix
from app.normalisation.name_normaliser import normalise_name




def normalise_card(raw, db):
    # 1. Canonical set → set_id
    canonical_set = normalise_set(raw.get("set", {}).get("name", "Unknown Set"))
    set_id = get_set_id(db, canonical_set)

    # 2. Canonical rarity → rarity_id
    canonical_rarity = normalise_rarity(raw["rarity"])
    rarity_id = get_rarity_id(db, canonical_rarity)

    # 3. Canonical variant → variant_id
    canonical_variant = normalise_variant(raw.get("subtypes", []))
    variant_id = get_variant_id(db, canonical_variant)

    return {
        "name": normalise_name(raw["name"]),
        "set_id": set_id,
        "rarity_id": rarity_id,
        "variant_id": variant_id,
        "number": extract_number(raw["number"]),
        "suffix": extract_suffix(raw["number"]),
        "language": "EN",
        "image_large": raw["images"]["large"],
        "image_small": raw["images"]["small"],
    }
