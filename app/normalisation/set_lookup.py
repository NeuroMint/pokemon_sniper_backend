from sqlalchemy.orm import Session
from app.models.set import Set
from app.normalisation.set_map import SET_NAME_MAP

print("[DEBUG] Loaded set_lookup.py from:", __file__)

def get_set_id(db: Session, raw_set_name: str) -> int:
    """
    Convert raw TCG API set name into canonical set name,
    then resolve or create the Set row.
    """

    if not raw_set_name:
        return None

    canonical = SET_NAME_MAP.get(raw_set_name.strip(), raw_set_name.strip())

    existing = (
        db.query(Set)
        .filter_by(canonical_name=canonical)
        .first()
    )

    if existing:
        return existing.id

    new_set = Set(
        canonical_name=canonical
    )

    db.add(new_set)
    db.commit()
    db.refresh(new_set)

    return new_set.id
