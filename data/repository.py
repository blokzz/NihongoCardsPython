from datetime import date
from data.models import Deck, Card
from core.exceptions import EmptyDeckError
from data.database import get_connection

def get_all_decks() -> list[Deck]:
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM decks").fetchall()
        return [Deck(id=r[0], name=r[1]) for r in rows]

def get_deck(deck_id: int) -> Deck:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM decks WHERE id = ?", (deck_id,)
        ).fetchone()
        if not row:
            raise EmptyDeckError(f"Talia o id {deck_id} nie istnieje")
        return Deck(id=row[0], name=row[1])

def save_deck(deck: Deck) -> int:
    with get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO decks (name) VALUES (?)", (deck.name,)
        )
        return cursor.lastrowid

def delete_deck(deck_id: int) -> None:
    with get_connection() as conn:
        conn.execute("DELETE FROM decks WHERE id = ?", (deck_id,))
        conn.execute("DELETE FROM cards WHERE deck_id = ?", (deck_id,))

def get_cards(deck_id: int) -> list[Card]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT id, deck_id, front, back, card_type, example, reading, correct, incorrect, interval, next_review, onyomi, kunyomi FROM cards WHERE deck_id = ?", (deck_id,)
        ).fetchall()
        return [Card(id=r[0], deck_id=r[1], front=r[2], back=r[3], card_type=r[4], example=r[5], reading=r[6], onyomi=r[11], kunyomi=r[12], correct=r[7], incorrect=r[8], interval=r[9], next_review=r[10]) for r in rows]

def get_due_cards(deck_id: int) -> list[Card]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT id, deck_id, front, back, card_type, example, reading, correct, incorrect, interval, next_review, onyomi, kunyomi FROM cards WHERE deck_id = ? AND next_review <= date('now')",
            (deck_id,)
        ).fetchall()
        return [Card(id=r[0], deck_id=r[1], front=r[2], back=r[3], card_type=r[4], example=r[5], reading=r[6], onyomi=r[11], kunyomi=r[12], correct=r[7], incorrect=r[8], interval=r[9], next_review=r[10]) for r in rows]

def save_card(card: Card) -> int:
    with get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO cards (deck_id, front, back, card_type, example, reading, onyomi, kunyomi) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (card.deck_id, card.front, card.back, card.card_type, card.example, card.reading, getattr(card, 'onyomi', None), getattr(card, 'kunyomi', None))
        )
        return cursor.lastrowid

def update_card(card: Card) -> None:
    with get_connection() as conn:
        conn.execute(
            """UPDATE cards 
               SET correct = ?, incorrect = ?, next_review = ?, interval = ?
               WHERE id = ?""",
            (card.correct, card.incorrect, card.next_review, card.interval, card.id)
        )

def update_card_details(card_id: int, front: str, back: str, card_type: str, example: str, reading: str, onyomi: str = None, kunyomi: str = None) -> None:
    with get_connection() as conn:
        conn.execute(
            """UPDATE cards 
               SET front = ?, back = ?, card_type = ?, example = ?, reading = ?, onyomi = ?, kunyomi = ?
               WHERE id = ?""",
            (front, back, card_type, example, reading, onyomi, kunyomi, card_id)
        )

def delete_card(card_id: int) -> None:
    with get_connection() as conn:
        conn.execute("DELETE FROM cards WHERE id = ?", (card_id,))

def get_progress() -> tuple[int, int]:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT xp, level FROM user_progress WHERE id = 1"
        ).fetchone()
        return (row[0], row[1]) if row else (0, 0)

def save_progress(xp: int, level: int) -> None:
    with get_connection() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO user_progress (id, xp, level) VALUES (1, ?, ?)",
            (xp, level)
        )

def get_next_card_id() -> int:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT MAX(id) FROM cards"
        ).fetchone()
        if row[0] is None:
            return 1
        return row[0] + 1

def get_card_count(deck_id: int) -> int:
    with get_connection() as conn:
        row = conn.execute("SELECT COUNT(*) FROM cards WHERE deck_id = ?", (deck_id,)).fetchone()
        return row[0] if row else 0

def get_due_card_count(deck_id: int) -> int:
    with get_connection() as conn:
        row = conn.execute("SELECT COUNT(*) FROM cards WHERE deck_id = ? AND next_review <= date('now')", (deck_id,)).fetchone()
        return row[0] if row else 0

def get_stats_all_time() -> list[tuple[date, int, int]]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT date, cards_learned, cards_reviewed FROM review_history"
        ).fetchall()
        return [ (date.fromisoformat(row[0]), row[1], row[2]) for row in rows]

def get_stats() -> tuple[int, int]:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT cards_learned, cards_reviewed FROM review_history WHERE date = date('now')"
        ).fetchone()
        return (row[0], row[1]) if row else (0, 0)

def save_stats(cards_learned: int, cards_reviewed: int) -> None:
    with get_connection() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO review_history (date, cards_learned, cards_reviewed) VALUES (date('now'), ?, ?)",
            (cards_learned, cards_reviewed)
        )