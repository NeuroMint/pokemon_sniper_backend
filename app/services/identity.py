def find_or_create_identity(db, normalized):
    identity = (
        db.query(CardIdentity)
        .filter_by(
            name=normalized["name"],
            set_id=normalized["set_id"],
            number=normalized["number"],
            suffix=normalized["suffix"],
            variant_id=normalized["variant_id"],
            language=normalized["language"],
        )
        .first()
    )

    if identity:
        return identity

    identity = CardIdentity(
        name=normalized["name"],
        set_id=normalized["set_id"],
        number=normalized["number"],
        suffix=normalized["suffix"],
        variant_id=normalized["variant_id"],
        language=normalized["language"],
    )

    db.add(identity)
    db.commit()
    db.refresh(identity)
    return identity
