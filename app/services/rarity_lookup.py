from sqlalchemy.orm import Session
from app.models.rarity import Rarity


def get_rarity_id(db: Session, canonical_name: str):
    # Handle missing rarity safely
    if not canonical_name:
        canonical_name = "Unknown"

    is_holo = 1 if ("Holo" in canonical_name) else 0

    rarity = (
        db.query(Rarity)
        .filter_by(canonical_name=canonical_name)
        .first()
    )

    if rarity:
        return rarity.id

    new_rarity = Rarity(
        canonical_name=canonical_name,
        is_holo=is_holo
    )

    db.add(new_rarity)
    db.commit()
    db.refresh(new_rarity)

    return new_rarity.id



def _infer_tier(name: str) -> int:
    """
    Assign rarity tiers:
    1 = Common
    2 = Uncommon
    3 = Rare / Holo Rare
    4 = Ultra Rare
    5 = Secret Rare
    """

    if name == "Common":
        return 1
    if name == "Uncommon":
        return 2
    if name in ["Rare", "Holo Rare"]:
        return 3
    if name == "Ultra Rare":
        return 4
    if name == "Secret Rare":
        return 5

    return 0
