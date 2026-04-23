import sqlite3
from pathlib import Path

DB_PATH = Path("data/flashcards.db")

def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(exist_ok=True)
    return sqlite3.connect(DB_PATH)

def init_db() -> None:
    with get_connection() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS decks (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                name        TEXT NOT NULL,
                created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS cards (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                deck_id     INTEGER NOT NULL REFERENCES decks(id),
                card_type   TEXT NOT NULL,
                front       TEXT NOT NULL,
                back        TEXT NOT NULL,
                example     TEXT,
                reading     TEXT,
                correct     INTEGER DEFAULT 0,
                incorrect   INTEGER DEFAULT 0,
                interval    INTEGER DEFAULT 1,
                next_review DATE DEFAULT CURRENT_DATE
            );

            CREATE TABLE IF NOT EXISTS user_progress (
                id      INTEGER PRIMARY KEY,
                xp      INTEGER DEFAULT 0,
                level   INTEGER DEFAULT 0
            );
        """)