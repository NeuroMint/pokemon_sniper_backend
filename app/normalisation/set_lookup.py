from app.models.set import Set

def get_set_id(db, canonical_name: str) -> int:
    """
    Returns set_id for a canonical set name.
    Creates the set if missing.
    """
    existing = db.query(Set).filter_by(canonical_name=canonical_name).first()

    if existing:
        return existing.id

    new_set = Set(canonical_name=canonical_name)
    db.add(new_set)
    db.commit()
    db.refresh(new_set)
    return new_set.id
