from datetime import date
class Card:
    def __init__(self, id: int, front: str, back: str, card_type: str, deck_id: int, next_review: date = None , example: str = None, reading: str = None):
        self.id = id
        self.front = front
        self.back = back
        self.card_type = card_type
        self.deck_id = deck_id
        self.next_review = next_review
        self.example = example
        self.reading = reading

class Deck:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
        # self.cards = cards
