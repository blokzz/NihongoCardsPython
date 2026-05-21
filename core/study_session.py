
from datetime import date, timedelta
from data.repository import update_card
from data.models import Card, Deck
from data.repository import get_cards
from core.exceptions import EmptyDeckError
import time

class StudySession:
    def __init__(self, deck_id: int, max_cards: int = 10):
        self.cards = get_cards(deck_id)
        if not self.cards:
            raise EmptyDeckError(str(deck_id))
        self.max_cards = min(max_cards, len(self.cards))
        self.queue = list(self.cards[:self.max_cards])
        self._generator = self._card_generator()
        self.current_card: Card | None = None
        self.correct = 0
        self.incorrect = 0
        self.total = self.max_cards
        self.begin_session = time.time()

    def _card_generator(self):
        while self.queue:
            yield self.queue.pop(0)

    def next_card(self) -> Card | None:
        elapsed = time.time() - self.begin_session
        if elapsed >= 600:
            self.current_card = None
            return None

        try:
            self.current_card = next(self._generator)
            return self.current_card
        except StopIteration:
            self.current_card = None
            return None

    def answer(self, rating: int) -> None:
        if not self.current_card:
            return
        if rating == 0:
            is_correct = False
            new_interval = 1
        elif rating == 3:
            is_correct = True
            new_interval = max(1, int(self.current_card.interval * 1.2))
        elif rating == 2:
            is_correct = True
            new_interval = max(2, int(self.current_card.interval * 2.0))
        elif rating == 1:
            is_correct = True
            new_interval = max(4, int(self.current_card.interval * 3.5))
        else:
            is_correct = False
            new_interval = 1

        if is_correct:
            self.correct += 1
            self.current_card.correct += 1
        else:
            self.incorrect += 1
            self.current_card.incorrect += 1

        self.current_card.interval = new_interval
        next_review_date = date.today() + timedelta(days=new_interval)
        self.current_card.next_review = next_review_date.strftime("%Y-%m-%d")

        update_card(self.current_card)

        if rating == 0 or rating == 3:
            if rating == 0:
                self.current_card.session_fails = getattr(self.current_card, 'session_fails', 0) + 1
            else:
                self.current_card.session_hards = getattr(self.current_card, 'session_hards', 0) + 1

            fails = getattr(self.current_card, 'session_fails', 0)
            hards = getattr(self.current_card, 'session_hards', 0)
            priority = fails * 2 + hards

            queue_len = len(self.queue)
            if queue_len <= 1:
                self.queue.append(self.current_card)
            else:
                insert_idx = max(1, queue_len - priority)
                self.queue.insert(insert_idx, self.current_card)
            self.total += 1

    @property
    def progress(self) -> tuple[int, int, float]:
        return (self.correct + self.incorrect, self.total, time.time() - self.begin_session)

    @property
    def is_finished(self) -> bool:
        return self.current_card is None and self.correct + self.incorrect > 0