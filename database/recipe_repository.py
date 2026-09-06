import sqlite3


def list_recipes(database_path):
    """Return summary info for every recipe."""
    with sqlite3.connect(database_path) as connection:
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")

        recipes = connection.execute(
            """
            SELECT
                recipe.id,
                recipe.title,
                recipe.description,
                recipe.prep_time,
                recipe.cook_time,
                recipe.tier,
                user.id AS user_id,
                user.name AS user_name
            FROM recipe
            JOIN user ON user.id = recipe.user_id
            ORDER BY recipe.title
            """
        ).fetchall()

    return [
        {
            "id": recipe["id"],
            "title": recipe["title"],
            "description": recipe["description"],
            "cook_time": recipe["cook_time"],
            "prep_time": recipe["prep_time"],
            "tier": recipe["tier"],
            "user": {
                "id": recipe["user_id"],
                "name": recipe["user_name"],
            },
        }
        for recipe in recipes
    ]


def get_recipe(database_path, recipe_id):
    """Return one complete recipe as a dictionary, or None when it does not exist."""
    with sqlite3.connect(database_path) as connection:
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")

        recipe = connection.execute(
            """
            SELECT
                recipe.id,
                recipe.title,
                recipe.description,
                recipe.prep_time,
                recipe.cook_time,
                recipe.tier,
                user.id AS user_id,
                user.name AS user_name
            FROM recipe
            JOIN user ON user.id = recipe.user_id
            WHERE recipe.id = ?
            """,
            (recipe_id,),
        ).fetchone()

        if recipe is None:
            return None

        ingredients = connection.execute(
            """
            SELECT ingredient.id, ingredient.name,
                   recipe_ingredient.amount, recipe_ingredient.unit
            FROM recipe_ingredient
            JOIN ingredient ON ingredient.id = recipe_ingredient.ingredient_id
            WHERE recipe_ingredient.recipe_id = ?
            ORDER BY ingredient.id
            """,
            (recipe_id,),
        ).fetchall()

        steps = connection.execute(
            """
            SELECT id, step_number, instruction
            FROM recipe_step
            WHERE recipe_id = ?
            ORDER BY step_number
            """,
            (recipe_id,),
        ).fetchall()

        tags = connection.execute(
            """
            SELECT tag.id, tag.name, tag.type
            FROM recipe_tag
            JOIN tag ON tag.id = recipe_tag.tag_id
            WHERE recipe_tag.recipe_id = ?
            ORDER BY tag.id
            """,
            (recipe_id,),
        ).fetchall()

        notes = connection.execute(
            """
            SELECT note.id, note.title, note.note_type, note.body
            FROM recipe_note
            JOIN note ON note.id = recipe_note.note_id
            WHERE recipe_note.recipe_id = ?
            ORDER BY note.id
            """,
            (recipe_id,),
        ).fetchall()

    return {
        "id": recipe["id"],
        "title": recipe["title"],
        "description": recipe["description"],
        "prep_time": recipe["prep_time"],
        "cook_time": recipe["cook_time"],
        "tier": recipe["tier"],
        "user": {"id": recipe["user_id"], "name": recipe["user_name"]},
        "ingredients": [dict(row) for row in ingredients],
        "steps": [dict(row) for row in steps],
        "tags": [dict(row) for row in tags],
        "notes": [dict(row) for row in notes],
    }


def create_recipe(database_path, recipe_data):
    """Create a recipe and return its complete saved representation."""
    with sqlite3.connect(database_path) as connection:
        connection.execute("PRAGMA foreign_keys = ON")

        cursor = connection.execute(
            """
            INSERT INTO recipe (
                title,
                description,
                user_id,
                prep_time,
                cook_time
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                recipe_data["title"],
                recipe_data["description"],
                recipe_data["user_id"],
                recipe_data["prep_time"],
                recipe_data["cook_time"],
            ),
        )

        recipe_id = cursor.lastrowid

    return get_recipe(database_path, recipe_id)


def update_recipe(database_path, recipe_id, recipe_data):
    """Update a recipe and return it, or None when it does not exist."""
    with sqlite3.connect(database_path) as connection:
        connection.execute("PRAGMA foreign_keys = ON")

        cursor = connection.execute(
            """
            UPDATE recipe
            SET
                title = COALESCE(?, title),
                description = COALESCE(?, description),
                user_id = COALESCE(?, user_id),
                prep_time = COALESCE(?, prep_time),
                cook_time = COALESCE(?, cook_time),
                tier = COALESCE(?, tier)
            WHERE id = ?
            """,
            (
                recipe_data.get("title"),
                recipe_data.get("description"),
                recipe_data.get("user_id"),
                recipe_data.get("prep_time"),
                recipe_data.get("cook_time"),
                recipe_data.get("tier"),
                recipe_id,
            ),
        )

        if cursor.rowcount == 0:
            return None

    return get_recipe(database_path, recipe_id)
