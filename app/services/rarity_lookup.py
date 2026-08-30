from app.models.rarity import Rarity

def get_rarity_id(db, canonical_name: str) -> int:
    rarity = db.query(Rarity).filter_by(canonical_name=canonical_name).first()

    if rarity:
        return rarity.id

    new_rarity = Rarity(
        canonical_name=canonical_name,
        tier=_infer_tier(canonical_name),
        is_holo=1 if "Holo" in canonical_name else 0,
        is_ultra=1 if "Ultra" in canonical_name else 0,
        is_secret=1 if "Secret" in canonical_name else 0,
    )

    db.add(new_rarity)
    db.commit()
    db.refresh(new_rarity)
    return new_rarity.id


def _infer_tier(name: str) -> int:
    if name == "Common": return 1
    if name == "Uncommon": return 2
    if name in ["Rare", "Holo Rare"]: return 3
    if name == "Ultra Rare": return 4
    if name == "Secret Rare": return 5
    return 0
