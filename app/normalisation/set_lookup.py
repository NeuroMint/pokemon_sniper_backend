from sqlalchemy.orm import Session
from app.models.set import Set

print("[DEBUG] Loaded set_lookup.py from:", __file__)

def get_set_id(db: Session, canonical_name: str) -> int:
    canonical = canonical_name.strip()

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
