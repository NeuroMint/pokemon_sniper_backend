from app.models.variant import Variant

def get_variant_id(db, canonical_name: str) -> int | None:
    if canonical_name is None:
        return None

    variant = db.query(Variant).filter_by(canonical_name=canonical_name).first()

    if variant:
        return variant.id

    new_variant = Variant(
        canonical_name=canonical_name,
        category=_infer_category(canonical_name)
    )

    db.add(new_variant)
    db.commit()
    db.refresh(new_variant)
    return new_variant.id


def _infer_category(name: str) -> str:
    if name in ["GX", "V", "VSTAR", "VMAX", "EX", "BREAK", "Radiant Pokémon"]:
        return "pokemon"
    if name in ["Full Art", "Trainer Gallery", "Tag Team"]:
        return "trainer"
    return "pokemon"
