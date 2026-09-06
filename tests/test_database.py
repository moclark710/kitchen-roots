import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from database import init_db


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = (ROOT / "database" / "schema.sql").read_text(encoding="utf-8")
SEED = (ROOT / "database" / "seeds" / "jollof_rice.sql").read_text(
    encoding="utf-8"
)


class DatabaseTests(unittest.TestCase):
    def setUp(self):
        self.connection = sqlite3.connect(":memory:")
        self.connection.execute("PRAGMA foreign_keys = ON")
        self.connection.executescript(SCHEMA)

    def tearDown(self):
        self.connection.close()

    def seed(self):
        self.connection.executescript(SEED)

    def test_schema_creates_all_uml_tables(self):
        tables = {
            row[0]
            for row in self.connection.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            )
        }
        self.assertTrue(
            {
                "user",
                "recipe",
                "recipe_step",
                "ingredient",
                "recipe_ingredient",
                "tag",
                "recipe_tag",
                "note",
                "recipe_note",
            }.issubset(tables)
        )

    def test_schema_columns_match_the_uml(self):
        expected_columns = {
            "user": {"id", "name", "email", "tier"},
            "recipe": {
                "id",
                "title",
                "description",
                "user_id",
                "cook_time",
                "prep_time",
                "tier",
            },
            "recipe_step": {"id", "recipe_id", "step_number", "instruction"},
            "ingredient": {"id", "name"},
            "recipe_ingredient": {"recipe_id", "ingredient_id", "amount", "unit"},
            "tag": {"id", "name", "type"},
            "recipe_tag": {"recipe_id", "tag_id"},
            "note": {"id", "title", "note_type", "body"},
            "recipe_note": {"recipe_id", "note_id"},
        }

        for table, expected in expected_columns.items():
            with self.subTest(table=table):
                actual = {
                    row[1]
                    for row in self.connection.execute(f"PRAGMA table_info({table})")
                }
                self.assertEqual(actual, expected)

    def test_initializer_creates_and_seeds_an_empty_database(self):
        with tempfile.TemporaryDirectory() as temp_directory:
            database_path = Path(temp_directory) / "kitchen_roots.db"
            with patch.object(init_db, "DATABASE_PATH", database_path):
                init_db.initialize_database(seed=True)

            with sqlite3.connect(database_path) as connection:
                self.assertEqual(
                    connection.execute("SELECT COUNT(*) FROM recipe").fetchone()[0],
                    1,
                )
                self.assertEqual(
                    connection.execute("SELECT COUNT(*) FROM recipe_step").fetchone()[0],
                    9,
                )

    def test_seed_contains_complete_jollof_recipe(self):
        self.seed()
        title = self.connection.execute("SELECT title FROM recipe").fetchone()[0]
        note_types = {
            row[0] for row in self.connection.execute("SELECT note_type FROM note")
        }

        self.assertEqual(title, "Liberian Jollof Rice")
        self.assertEqual(
            self.connection.execute("SELECT COUNT(*) FROM recipe_ingredient").fetchone()[0],
            14,
        )
        self.assertEqual(
            self.connection.execute("SELECT COUNT(*) FROM recipe_step").fetchone()[0],
            9,
        )
        self.assertEqual(
            self.connection.execute("SELECT COUNT(*) FROM recipe_tag").fetchone()[0],
            4,
        )
        self.assertEqual(note_types, {"family", "region", "technical", "heritage"})

    def test_recipe_ingredient_stores_amount_and_unit(self):
        self.seed()
        amount, unit = self.connection.execute(
            """
            SELECT ri.amount, ri.unit
            FROM recipe_ingredient AS ri
            JOIN ingredient AS i ON i.id = ri.ingredient_id
            WHERE i.name = 'Long-grain rice, rinsed'
            """
        ).fetchone()
        self.assertEqual((amount, unit), ("2", "cups"))

    def test_foreign_keys_reject_orphaned_relationships(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.connection.execute(
                "INSERT INTO recipe_tag (recipe_id, tag_id) VALUES (999, 999)"
            )

    def test_join_tables_reject_duplicate_relationships(self):
        self.seed()
        statements = (
            "INSERT INTO recipe_ingredient VALUES (1, 1, '3', 'cups')",
            "INSERT INTO recipe_tag VALUES (1, 1)",
            "INSERT INTO recipe_note VALUES (1, 1)",
        )
        for statement in statements:
            with self.subTest(statement=statement):
                with self.assertRaises(sqlite3.IntegrityError):
                    self.connection.execute(statement)

    def test_recipe_steps_are_ordered_and_unique(self):
        self.seed()
        step_numbers = [
            row[0]
            for row in self.connection.execute(
                "SELECT step_number FROM recipe_step ORDER BY step_number"
            )
        ]
        self.assertEqual(step_numbers, list(range(1, 10)))
        with self.assertRaises(sqlite3.IntegrityError):
            self.connection.execute(
                "INSERT INTO recipe_step VALUES (10, 1, 1, 'Duplicate step')"
            )

    def test_deleting_recipe_cascades_only_relationship_data(self):
        self.seed()
        self.connection.execute("DELETE FROM recipe WHERE id = 1")

        for table in ("recipe_step", "recipe_ingredient", "recipe_tag", "recipe_note"):
            with self.subTest(table=table):
                self.assertEqual(
                    self.connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0],
                    0,
                )
        for table in ("ingredient", "tag", "note"):
            with self.subTest(table=table):
                self.assertGreater(
                    self.connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0],
                    0,
                )

    def test_deleting_reusable_records_removes_only_their_links(self):
        self.seed()
        cases = (
            ("ingredient", "recipe_ingredient", "ingredient_id"),
            ("tag", "recipe_tag", "tag_id"),
            ("note", "recipe_note", "note_id"),
        )
        for record_table, join_table, foreign_key in cases:
            with self.subTest(record_table=record_table):
                self.connection.execute(f"DELETE FROM {record_table} WHERE id = 1")
                self.assertEqual(
                    self.connection.execute(
                        f"SELECT COUNT(*) FROM {join_table} WHERE {foreign_key} = 1"
                    ).fetchone()[0],
                    0,
                )

    def test_note_can_be_reused_across_recipes(self):
        self.seed()
        self.connection.execute(
            """
            INSERT INTO recipe (id, title, description, user_id, prep_time)
            VALUES (2, 'Leftover Jollof', 'A second recipe', 1, 10)
            """
        )
        self.connection.execute("INSERT INTO recipe_note VALUES (2, 1)")
        linked_recipe_count = self.connection.execute(
            "SELECT COUNT(*) FROM recipe_note WHERE note_id = 1"
        ).fetchone()[0]
        self.assertEqual(linked_recipe_count, 2)


if __name__ == "__main__":
    unittest.main()
