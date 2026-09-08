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

    def test_home_page_loads_the_landing_page_with_navigation(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Family recipes carry more than ingredients.", response.data)
        self.assertIn(b'href="/recipes"', response.data)
        self.assertIn(b'href="/recipes/new"', response.data)

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

    def test_create_recipe_rejects_a_blank_title(self):
        response = self.client.post(
            "/api/recipes",
            json={
                "title": "",
                "description": "A recipe without a title.",
                "prep_time": 10,
                "cook_time": 20,
                "user_id": 1,
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json(),
            {"error": "Title is required."},
        )

    def test_create_recipe_rejects_a_blank_description(self):
        response = self.client.post(
            "/api/recipes",
            json={
                "title": "Pepper Soup",
                "description": "   ",
                "prep_time": 10,
                "cook_time": 20,
                "user_id": 1,
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json(),
            {"error": "Description is required."},
        )

    def test_create_recipe_rejects_a_negative_prep_time(self):
        response = self.client.post(
            "/api/recipes",
            json={
                "title": "Pepper Soup",
                "description": "A warming soup.",
                "prep_time": -1,
                "cook_time": 20,
                "user_id": 1,
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json(),
            {"error": "Prep time must be zero or greater."},
        )

    def test_create_recipe_rejects_a_negative_cook_time(self):
        response = self.client.post(
            "/api/recipes",
            json={
                "title": "Pepper Soup",
                "description": "A Warming Soup",
                "prep_time": 10,
                "cook_time": -1,
                "user_id": 1,
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json(),
            {"error": "Cook time must be zero or greater."},
        )

    def test_create_recipe_requires_json_recipe_data(self):
        response = self.client.post("/api/recipes")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json(),
            {"error": "Recipe data is required."},
        )

    def test_create_recipe_requires_a_user(self):
        response = self.client.post(
            "/api/recipes",
            json={
                "title": "Pepper Soup",
                "description": "A warming soup.",
                "prep_time": 10,
                "cook_time": 20,
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json(),
            {"error": "User is required."},
        )

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

    def test_update_recipe_rejects_a_blank_title(self):
        response = self.client.patch(
            "/api/recipes/1",
            json={"title": "   "},
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json(),
            {"error": "Title is required."},
        )

        saved_recipe = self.client.get("/api/recipes/1").get_json()
        self.assertEqual(saved_recipe["title"], "Liberian Jollof Rice")

    def test_update_recipe_rejects_a_negative_cook_time(self):
        response = self.client.patch(
            "/api/recipes/1",
            json={"cook_time": -1},
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json(),
            {"error": "Cook time must be zero or greater."},
        )

        saved_recipe = self.client.get("/api/recipes/1").get_json()
        self.assertEqual(saved_recipe["cook_time"], 80)

    def test_update_missing_recipe_returns_json_404(self):
        response = self.client.patch(
            "/api/recipes/999",
            json={"title": "Missing Recipe"},
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.get_json(),
            {"error": "Recipe not found."},
        )

    def test_update_recipe_requires_json_recipe_data(self):
        response = self.client.patch("/api/recipes/1")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json(),
            {"error": "Recipe data is required."},
        )

    def test_ingredient_list_api_returns_reusable_ingredients(self):
        response = self.client.get("/api/ingredients")
        ingredients = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(ingredients), 14)
        self.assertIn(
            {
                "id": 1,
                "name": "Long-grain rice, rinsed",
            },
            ingredients,
        )

    def test_create_ingredient_api_adds_a_reusable_ingredient(self):
        response = self.client.post(
            "/api/ingredients",
            json={"name": "Fresh ginger"},
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.get_json(),
            {
                "id": 15,
                "name": "Fresh ginger",
            },
        )

        ingredients = self.client.get("/api/ingredients").get_json()
        self.assertIn(
            {
                "id": 15,
                "name": "Fresh ginger",
            },
            ingredients,
        )

    def test_attach_ingredient_api_adds_it_to_the_recipe(self):
        with sqlite3.connect(self.database_path) as connection:
            connection.execute(
                """
                INSERT INTO ingredient (id, name)
                VALUES (?, ?)
                """,
                (15, "Fresh ginger"),
            )

        response = self.client.post(
            "/api/recipes/1/ingredients",
            json={
                "ingredient_id": 15,
                "amount": "1",
                "unit": "tbsp",
            },
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.get_json(),
            {
                "id": 15,
                "name": "Fresh ginger",
                "amount": "1",
                "unit": "tbsp",
            },
        )

        saved_recipe = self.client.get("/api/recipes/1").get_json()
        ingredient_ids = [
            ingredient["id"]
            for ingredient in saved_recipe["ingredients"]
        ]
        self.assertIn(15, ingredient_ids)

    def test_remove_ingredient_api_removes_only_the_recipe_relationship(self):
        response = self.client.delete(
            "/api/recipes/1/ingredients/14"
        )

        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data, b"")

        saved_recipe = self.client.get("/api/recipes/1").get_json()
        ingredient_ids = [
            ingredient["id"]
            for ingredient in saved_recipe["ingredients"]
        ]
        self.assertNotIn(14, ingredient_ids)

        with sqlite3.connect(self.database_path) as connection:
            reusable_ingredient = connection.execute(
                "SELECT name FROM ingredient WHERE id = ?",
                (14,),
            ).fetchone()

        self.assertIsNotNone(reusable_ingredient)

    def test_update_recipe_ingredient_api_changes_amount_and_unit(self):
        response = self.client.patch(
            "/api/recipes/1/ingredients/1",
            json={
                "amount": "3",
                "unit": "cups",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_json(),
            {
                "id": 1,
                "name": "Long-grain rice, rinsed",
                "amount": "3",
                "unit": "cups",
            },
        )

        saved_recipe = self.client.get("/api/recipes/1").get_json()
        updated_ingredient = next(
            ingredient
            for ingredient in saved_recipe["ingredients"]
            if ingredient["id"] == 1
        )

        self.assertEqual(updated_ingredient["amount"], "3")
        self.assertEqual(updated_ingredient["unit"], "cups")

    def test_edit_recipe_page_includes_requested_recipe_id(self):
        response = self.client.get("/recipes/1/edit")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Edit Recipe", response.data)
        self.assertIn(b'data-recipe-id="1"', response.data)
        self.assertIn(b"edit_recipe.js", response.data)
        self.assertIn(b'name="cook_time"', response.data)
        self.assertIn(b"Ingredients", response.data)
        self.assertIn(b"data-ingredient-list", response.data)
        self.assertIn(b'id="ingredient-form"', response.data)
        self.assertIn(b'name="ingredient_id"', response.data)
        self.assertIn(b'name="ingredient_name"', response.data)
        self.assertIn(b'name="amount"', response.data)
        self.assertIn(b'name="unit"', response.data)

    def test_tag_relationship_api_attaches_and_removes_a_reusable_tag(self):
        with sqlite3.connect(self.database_path) as connection:
            connection.execute(
                """
                INSERT INTO tag (id, name, type)
                VALUES (?, ?, ?)
                """,
                (5, "Spicy", "flavor"),
            )

        attach_response = self.client.post(
            "/api/recipes/1/tags",
            json={"tag_id": 5},
        )

        self.assertEqual(attach_response.status_code, 201)
        self.assertEqual(
            attach_response.get_json(),
            {
                "id": 5,
                "name": "Spicy",
                "type": "flavor",
            },
        )

        remove_response = self.client.delete(
            "/api/recipes/1/tags/5"
        )
        self.assertEqual(remove_response.status_code, 204)

        saved_recipe = self.client.get("/api/recipes/1").get_json()
        tag_ids = [tag["id"] for tag in saved_recipe["tags"]]
        self.assertNotIn(5, tag_ids)

        with sqlite3.connect(self.database_path) as connection:
            reusable_tag = connection.execute(
                "SELECT name FROM tag WHERE id = ?",
                (5,),
            ).fetchone()

        self.assertIsNotNone(reusable_tag)

    def test_note_relationship_api_attaches_and_removes_a_reusable_note(self):
        with sqlite3.connect(self.database_path) as connection:
            connection.execute(
                """
                INSERT INTO note (id, title, note_type, body)
                VALUES (?, ?, ?, ?)
                """,
                (
                    5,
                    "Serving Tradition",
                    "family",
                    "Serve from one shared platter.",
                ),
            )

        attach_response = self.client.post(
            "/api/recipes/1/notes",
            json={"note_id": 5},
        )

        self.assertEqual(attach_response.status_code, 201)
        self.assertEqual(
            attach_response.get_json(),
            {
                "id": 5,
                "title": "Serving Tradition",
                "note_type": "family",
                "body": "Serve from one shared platter.",
            },
        )

        remove_response = self.client.delete(
            "/api/recipes/1/notes/5"
        )
        self.assertEqual(remove_response.status_code, 204)

        saved_recipe = self.client.get("/api/recipes/1").get_json()
        note_ids = [note["id"] for note in saved_recipe["notes"]]
        self.assertNotIn(5, note_ids)

        with sqlite3.connect(self.database_path) as connection:
            reusable_note = connection.execute(
                "SELECT title FROM note WHERE id = ?",
                (5,),
            ).fetchone()

        self.assertIsNotNone(reusable_note)

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

    def test_database_failure_returns_json_500(self):
        app = create_app(
            {
                "TESTING": True,
                "DATABASE_PATH": Path(self.temp_directory.name),
            }
        )
        client = app.test_client()

        response = client.get("/api/recipes")

        self.assertEqual(response.status_code, 500)
        self.assertEqual(
            response.get_json(),
            {"error": "A database error occurred."},
        )


if __name__ == "__main__":
    unittest.main()
