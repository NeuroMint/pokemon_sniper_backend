from app.normalisation.set_normaliser import normalise_set
from app.services.set_lookup import get_set_id

def normalise_card(raw):
    return {
        "name": normalise_name(raw["name"]),
        "set_id": normalise_set(raw["set"]["name"]),
        "rarity_id": normalise_rarity(raw["rarity"]),
        "variant_id": normalise_variant(raw.get("subtypes", [])),
        "number": extract_number(raw["number"]),
        "suffix": extract_suffix(raw["number"]),
        "language": "EN",
        "image_large": raw["images"]["large"],
        "image_small": raw["images"]["small"],
    }
