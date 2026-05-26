from datetime import date
class Card:
    def __init__(self, id: int, front: str, back: str, card_type: str, deck_id: int, 
                 next_review: str = None, example: str = None, reading: str = None, 
                 onyomi: str = None, kunyomi: str = None,
                 correct: int = 0, incorrect: int = 0, interval: int = 1):
        self.id = id
        self.front = front
        self.back = back
        self.card_type = card_type
        self.deck_id = deck_id
        self.next_review = next_review
        self.example = example
        self.reading = reading
        self.onyomi = onyomi
        self.kunyomi = kunyomi
        self.correct = correct
        self.incorrect = incorrect
        self.interval = interval

class Deck:
    def __init__(self, id: int, name: str, cards: list = []):
        self.id = id
        self.name = name
        self.cards = cards
