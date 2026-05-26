import json
import re
from data.models import Card , Deck
from data.repository import save_card , save_deck , get_next_card_id
from utils import log_errors
from core.exceptions import *

@log_errors
def import_from_json(path: str) -> Deck:
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
        _validate_json(data)
        deck_id = save_deck(Deck(id = None , name=data['name']))
        for card_data in data['cards']:
            card = Card(
                id = get_next_card_id(),
                deck_id=deck_id,
                front=card_data['front'],
                back=card_data['back'],
                card_type=card_data.get('card_type' , 'Word'),
                example=card_data.get('example' , ""),
                reading=card_data.get('reading' , ""),
                onyomi=card_data.get('onyomi'),
                kunyomi=card_data.get('kunyomi')
            )
            save_card(card)
        return deck_id



def _validate_json(data: dict) -> None:
    japanese = re.compile(r'[\u3040-\u309f\u30a0-\u30ff\u4e00-\u9fff]')
    
    if "name" not in data:
        raise InvalidJsonError("name")
    if "cards" not in data:
        raise InvalidJsonError("cards")
        
    allowed_types = {"Kanji", "Kana", "Word", "Sentence"}
    
    for card in data["cards"]:
        if "front" not in card or "back" not in card:
            raise InvalidJsonError("front/back")
        if not japanese.search(card["front"]):
            raise InvalidCardError("front", card["front"])
            
        card_type = card.get("card_type", "Word")
        if card_type not in allowed_types:
            raise InvalidFormatError(f"Card type '{card_type}' is not supported. Supported types: {allowed_types}")