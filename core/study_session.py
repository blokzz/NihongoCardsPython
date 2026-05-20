
from data.models import Card, Deck
from data.repository import get_cards
from core.exceptions import EmptyDeckError
import time
class StudySession:
    def __init__(self, deck_id: int):
        self.cards = get_cards(deck_id)
        if not self.cards:
            raise EmptyDeckError(str(deck_id))
        self._generator = self._card_generator()
        self.current_card: Card | None = None
        self.correct = 0
        self.incorrect = 0
        self.total = len(self.cards)
        self.begin_session = time.time()

    def _card_generator(self):
        for card in self.cards:
            yield card

    def next_card(self) -> Card | None:
        try:
            self.current_card = next(self._generator)
            return self.current_card
        except StopIteration:
            self.current_card = None
            return None

    def answer(self, correct: bool) -> None:
        if correct:
            self.correct += 1
        else:
            self.incorrect += 1

    @property
    def progress(self) -> tuple[int, int, float]:
        return (self.correct + self.incorrect, self.total, time.time() - self.begin_session)

    @property
    def is_finished(self) -> bool:
        return self.current_card is None and self.correct + self.incorrect > 0