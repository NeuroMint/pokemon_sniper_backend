from app.database import SessionLocal
from app.models.card import Card
from app.models.set import Set
from app.normalisation.set_map import SET_NAME_MAP

def repair_sets():
    db = SessionLocal()

    cards = db.query(Card).all()
    print(f"[REPAIR] Loaded {len(cards)} cards")

    fixed = 0
    skipped = 0

    for card in cards:
        try:
            raw = card.identity.set.canonical_name
        except:
            skipped += 1
            continue

        if not raw:
            skipped += 1
            continue

        canonical = SET_NAME_MAP.get(raw.strip(), raw.strip())

        existing_set = (
            db.query(Set)
            .filter_by(canonical_name=canonical)
            .first()
        )

        if not existing_set:
            existing_set = Set(canonical_name=canonical)
            db.add(existing_set)
            db.commit()
            db.refresh(existing_set)

        card.set_id = existing_set.id
        db.add(card)
        fixed += 1

    db.commit()
    print(f"[REPAIR] Fixed {fixed} cards, skipped {skipped}")
    print("[REPAIR] Done.")

if __name__ == "__main__":
    repair_sets()
