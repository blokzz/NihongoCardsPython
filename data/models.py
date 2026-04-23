from datetime import date
class Card:
    def __init__(self, id: int, front: str, back: str, next_review: date):
        self.id = id
        self.front = front
        self.back = back
        self.next_review = next_review

class Deck:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
        # self.cards = cards
