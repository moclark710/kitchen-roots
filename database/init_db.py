import sqlite3
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = Path(__file__).resolve().parent / "schema.sql"
DATABASE_PATH = PROJECT_ROOT / "instance" / "kitchen_roots.db"


def initialize_database():
    DATABASE_PATH.parent.mkdir(exist_ok=True)

    schema = SCHEMA_PATH.read_text(encoding="utf-8")

    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute("PRAGMA foreign_keys = ON;")
        connection.executescript(schema)

    print(f"Database initialized at {DATABASE_PATH}")


if __name__ == "__main__":
    initialize_database()