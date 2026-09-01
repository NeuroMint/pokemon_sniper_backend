from sqlalchemy.orm import Session
from app.models.card_identity import CardIdentity


def find_or_create_identity(db: Session, normalized: dict) -> CardIdentity:
    """
    Deduplicate cards by canonical identity fields.
    Identity = (name, set, number, suffix, variant, language)
    """

    identity = (
        db.query(CardIdentity)
        .filter_by(
            name=normalized["name"],
            set_id=normalized["set_id"],
            number=normalized["number"],
            suffix=normalized["suffix"],
            variant_id=normalized["variant_id"],
            language_id=normalized["language_id"],
        )
        .first()
    )

    if identity:
        return identity

    identity = CardIdentity(
        name=normalized["name"],
        canonical_name=normalized["canonical_name"],
        set_id=normalized["set_id"],
        rarity_id=normalized["rarity_id"],
        variant_id=normalized["variant_id"],
        language_id=normalized["language_id"],
        number=normalized["number"],
        suffix=normalized["suffix"],
    )

    db.add(identity)
    db.commit()
    db.refresh(identity)

    return identity
