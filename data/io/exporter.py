import os
import json
from utils import log_errors
from data.repository import get_deck, get_cards

@log_errors
def export_to_json(path: str, deck_id: int) -> None:
    deck = get_deck(deck_id)
    cards = get_cards(deck_id)

    data = {
        "name": deck.name,
        "cards": []
    }
    
    for card in cards:
        card_dict = {
            k: v for k, v in [
                ("front", card.front),
                ("back", card.back),
                ("card_type", card.card_type),
                ("example", card.example or ""),
                ("reading", card.reading or ""),
                ("onyomi", getattr(card, "onyomi", None)),
                ("kunyomi", getattr(card, "kunyomi", None)),
            ] if v is not None
        }
        data["cards"].append(card_dict)
    
    dir_name = os.path.dirname(path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
        
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)