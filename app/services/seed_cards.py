from database import SessionLocal
from app.models.card import Card

cards_to_add = [
    {
        "name": "Charizard VMAX",
        "set": "Shining Fates",
        "number": "SV107",
        "rarity": "Secret Rare",
        "language": "EN",
        "variant": "Full Art"
    },
    {
        "name": "Mew ex",
        "set": "151",
        "number": "205/165",
        "rarity": "Secret Rare",
        "language": "EN",
        "variant": "Alt Art"
    }
]

def seed():
    db = SessionLocal()
    for c in cards_to_add:
        card = Card(**c)
        db.add(card)
    db.commit()
    db.close()
