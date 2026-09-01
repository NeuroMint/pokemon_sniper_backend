from sqlalchemy.orm import Session
from app.models.variant import Variant


def get_variant_id(db: Session, canonical_name: str) -> int | None:
    """
    Resolve a variant ID from a canonical variant name.
    Auto‑creates the variant if missing.
    """

    if canonical_name is None:
        return None

    variant = (
        db.query(Variant)
        .filter_by(canonical_name=canonical_name)
        .first()
    )

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
    """
    Categorise variants into pokemon / trainer.
    """
    pokemon_variants = {
        "GX", "V", "VSTAR", "VMAX", "EX", "BREAK", "Radiant Pokémon"
    }

    trainer_variants = {
        "Full Art", "Trainer Gallery", "Tag Team"
    }

    if name in pokemon_variants:
        return "pokemon"

    if name in trainer_variants:
        return "trainer"

    return "pokemon"
