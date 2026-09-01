from sqlalchemy.orm import Session
from app.models.language import Language


def get_language_id(db: Session, language_code: str) -> int:
    """
    Resolve a language ID from a language code (e.g., 'EN').
    Auto‑creates the language if missing.
    """

    canonical = language_code.lower().strip()

    # Look up existing language
    language = (
        db.query(Language)
        .filter_by(canonical_name=canonical)
        .first()
    )

    # Create if missing
    if not language:
        language = Language(
            canonical_name=canonical,
            display_name="English" if canonical == "en" else canonical.upper()
        )
        db.add(language)
        db.commit()
        db.refresh(language)

    return language.id
