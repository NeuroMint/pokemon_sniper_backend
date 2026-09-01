from sqlalchemy.orm import Session
from datetime import datetime

from app.models.card import Card
from app.models.ingestion_logs import IngestionLog

# NEW imports
from app.normalisation.card_normaliser import normalise_card
from app.services.identity import find_or_create_identity


def log_ingestion(db: Session, source: str, status: str, message: str):
    log = IngestionLog(
        source=source,
        status=status,
        message=message,
        created_at=datetime.utcnow()
    )
    db.add(log)
    db.commit()


def ingest_card(db: Session, raw_card: dict, source: str = "unknown"):
    """
    NEW INGESTION PIPELINE
    --------------------------------
    Scraper → normalise → identity → insert → log → return
    """
    try:
        # 1. Normalise raw scraped data
        normalized = normalise_card(raw_card, db)

        # 2. Resolve card identity (deduplication)
        identity = find_or_create_identity(db, normalized)

        # 3. Insert card instance (linked to identity)
        new_card = Card(
            identity_id=identity.id,

            # Basic fields
            name=normalized["name"],
            card_number=normalized["card_number"],  # FIXED

            # Canonical fields
            number=normalized["number"],
            suffix=normalized["suffix"],

            # Foreign keys
            set_id=normalized["set_id"],
            rarity_id=normalized["rarity_id"],
            variant_id=normalized["variant_id"],
            language_id=normalized["language_id"],

            # Images
            image_large=normalized["image_large"],
            image_small=normalized["image_small"],

            # Source
            source=source,
        )

        db.add(new_card)
        db.commit()
        db.refresh(new_card)

        # 4. Log success
        log_ingestion(db, source, "success", f"Inserted card {new_card.id}")
        print(f"[INGESTED] {normalized['name']} from {source}")

        return new_card

    except Exception as e:
        # Log failure with card name if possible
        name = raw_card.get("name", "UNKNOWN")
        log_ingestion(db, source, "error", f"{name}: {e}")
        raise
