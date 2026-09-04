import argparse
import sqlite3
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = Path(__file__).resolve().parent / "schema.sql"
SEED_PATH = Path(__file__).resolve().parent / "seeds" / "jollof_rice.sql"
DATABASE_PATH = PROJECT_ROOT / "instance" / "kitchen_roots.db"


def initialize_database(seed=False):
    DATABASE_PATH.parent.mkdir(exist_ok=True)

    schema = SCHEMA_PATH.read_text(encoding="utf-8")

    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute("PRAGMA foreign_keys = ON;")
        connection.executescript(schema)
        if seed:
            recipe_count = connection.execute("SELECT COUNT(*) FROM recipe").fetchone()[0]
            if recipe_count == 0:
                connection.executescript(SEED_PATH.read_text(encoding="utf-8"))

    print(f"Database initialized at {DATABASE_PATH}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Initialize the Kitchen Roots database.")
    parser.add_argument(
        "--seed",
        action="store_true",
        help="load the Jollof Rice development data when the recipe table is empty",
    )
    args = parser.parse_args()
    initialize_database(seed=args.seed)
