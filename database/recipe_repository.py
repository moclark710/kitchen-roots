import sqlite3


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
        "tier": recipe["tier"],
        "user": {"id": recipe["user_id"], "name": recipe["user_name"]},
        "ingredients": [dict(row) for row in ingredients],
        "steps": [dict(row) for row in steps],
        "tags": [dict(row) for row in tags],
        "notes": [dict(row) for row in notes],
    }
