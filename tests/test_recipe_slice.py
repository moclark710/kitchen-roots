import sqlite3
import tempfile
import unittest
from pathlib import Path

from app import create_app


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = (ROOT / "database" / "schema.sql").read_text(encoding="utf-8")
SEED = (ROOT / "database" / "seeds" / "jollof_rice.sql").read_text(
    encoding="utf-8"
)


class RecipeDetailSliceTests(unittest.TestCase):
    def setUp(self):
        self.temp_directory = tempfile.TemporaryDirectory()
        self.database_path = Path(self.temp_directory.name) / "test.db"

        with sqlite3.connect(self.database_path) as connection:
            connection.execute("PRAGMA foreign_keys = ON")
            connection.executescript(SCHEMA)
            connection.executescript(SEED)

        app = create_app(
            {"TESTING": True, "DATABASE_PATH": self.database_path}
        )
        self.client = app.test_client()

    def tearDown(self):
        self.temp_directory.cleanup()

    def test_recipe_api_returns_the_complete_seeded_recipe(self):
        response = self.client.get("/api/recipes/1")
        recipe = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(recipe["title"], "Liberian Jollof Rice")
        self.assertEqual(recipe["prep_time"], 20)
        self.assertEqual(recipe["cook_time"], 80)

        self.assertEqual(recipe["user"]["name"], "KrugehCooks")
        self.assertEqual(len(recipe["ingredients"]), 14)
        self.assertEqual(len(recipe["steps"]), 9)
        self.assertEqual(len(recipe["tags"]), 4)
        self.assertEqual(len(recipe["notes"]), 4)
        self.assertEqual(
            [step["step_number"] for step in recipe["steps"]],
            list(range(1, 10)),
        )

    def test_missing_recipe_returns_json_404(self):
        response = self.client.get("/api/recipes/999")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"error": "Recipe not found."})

    def test_home_page_loads_the_recipe_frontend(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Kitchen Roots", response.data)
        self.assertIn(b"recipe.js", response.data)

    def test_recipe_list_api_returns_recipe_summaries(self):
        response = self.client.get("/api/recipes")
        recipes = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(recipes), 1)
        self.assertEqual(recipes[0]["title"], "Liberian Jollof Rice")
        self.assertEqual(recipes[0]["user"]["name"], "KrugehCooks")
        self.assertNotIn("ingredients", recipes[0])
        self.assertEqual(recipes[0]["cook_time"], 80)

    def test_recipe_collection_page_loads_the_collection_frontend(self):
        response = self.client.get("/recipes")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Loading recipes...", response.data)
        self.assertIn(b"recipes.js", response.data)
        self.assertIn(b'href="/recipes/new"', response.data)


    def test_recipe_detail_page_includes_requested_recipe_id(self):
        response = self.client.get("/recipes/1")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'data-recipe-id="1"', response.data)
        self.assertIn(b'href="/recipes/1/edit"', response.data)
        self.assertIn(b"data-delete-button", response.data)

    def test_create_recipe_api_adds_a_recipe(self):
        response = self.client.post(
            "/api/recipes",
            json={
                "title": "Pepper Soup",
                "description": "A warming West African soup.",
                "prep_time": 45,
                "cook_time": 70,
                "user_id": 1,
            },
        )
        recipe = response.get_json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(recipe["title"], "Pepper Soup")
        self.assertEqual(recipe["description"], "A warming West African soup.")
        self.assertEqual(recipe["prep_time"], 45)
        self.assertEqual(recipe["cook_time"], 70)
        self.assertEqual(recipe["tier"], "free")
        self.assertEqual(recipe["user"]["id"], 1)

    def test_new_recipe_page_loads_the_form(self):
        response = self.client.get("/recipes/new")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Add a Recipe", response.data)
        self.assertIn(b'recipe-form', response.data)
        self.assertIn(b"create_recipe.js", response.data)
        self.assertIn(b'name="cook_time"', response.data)

    def test_update_recipe_api_changes_the_saved_recipe(self):
        response = self.client.patch(
            "/api/recipes/1",
            json={
                "title": "Updated Liberian Jollof Rice",
                "prep_time": 60,
                "cook_time": 90,
            },
        )
        updated_recipe = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            updated_recipe["title"],
            "Updated Liberian Jollof Rice",
        )
        self.assertEqual(updated_recipe["prep_time"], 60)
        self.assertEqual(updated_recipe["cook_time"], 90)

        saved_response = self.client.get("/api/recipes/1")
        saved_recipe = saved_response.get_json()

        self.assertEqual(
            saved_recipe["title"],
            "Updated Liberian Jollof Rice",
        )
        self.assertEqual(saved_recipe["prep_time"], 60)
        self.assertEqual(saved_recipe["cook_time"], 90)

    def test_edit_recipe_page_includes_requested_recipe_id(self):
        response = self.client.get("/recipes/1/edit")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Edit Recipe", response.data)
        self.assertIn(b'data-recipe-id="1"', response.data)
        self.assertIn(b"edit_recipe.js", response.data)
        self.assertIn(b'name="cook_time"', response.data)

    def test_delete_recipe_api_removes_the_recipe(self):
        response = self.client.delete("/api/recipes/1")

        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data, b"")

        missing_response = self.client.get("/api/recipes/1")

        self.assertEqual(missing_response.status_code, 404)

    def test_delete_missing_recipe_returns_json_404(self):
        response = self.client.delete("/api/recipes/999")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.get_json(),
            {"error": "Recipe not found."},
        )

if __name__ == "__main__":
    unittest.main()
