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
            "front": card.front,
            "back": card.back,
            "card_type": card.card_type,
            "example": card.example or "",
            "reading": card.reading or "",
        }
        if getattr(card, "onyomi", None) is not None:
            card_dict["onyomi"] = card.onyomi
        if getattr(card, "kunyomi", None) is not None:
            card_dict["kunyomi"] = card.kunyomi
        data["cards"].append(card_dict)
    
    dir_name = os.path.dirname(path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
        
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)