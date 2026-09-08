import sqlite3


def list_recipes(database_path, tag_id=None, search=None):
    """Return recipe summaries, optionally filtered by tag and title."""
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
            WHERE (
                ? IS NULL
                OR EXISTS (
                    SELECT 1
                    FROM recipe_tag
                    WHERE recipe_tag.recipe_id = recipe.id
                      AND recipe_tag.tag_id = ?
                )
            )
              AND (? IS NULL OR recipe.title LIKE ?)
            ORDER BY recipe.title
            """,
            (
                tag_id,
                tag_id,
                search,
                f"%{search}%" if search else None,
            ),
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


def list_ingredients(database_path):
    """Return every reusable ingredient in alphabetical order."""
    with sqlite3.connect(database_path) as connection:
        connection.row_factory = sqlite3.Row

        ingredients = connection.execute(
            """
            SELECT id, name
            FROM ingredient
            ORDER BY name
            """
        ).fetchall()

    return [dict(ingredient) for ingredient in ingredients]


def create_ingredient(database_path, ingredient_data):
    """Create and return a reusable ingredient."""
    with sqlite3.connect(database_path) as connection:
        cursor = connection.execute(
            """
            INSERT INTO ingredient (name)
            VALUES (?)
            """,
            (ingredient_data["name"],),
        )

        ingredient = {
            "id": cursor.lastrowid,
            "name": ingredient_data["name"],
        }

    return ingredient


def list_tags(database_path):
    """Return every reusable tag in alphabetical order."""
    with sqlite3.connect(database_path) as connection:
        connection.row_factory = sqlite3.Row

        tags = connection.execute(
            """
            SELECT id, name, type
            FROM tag
            ORDER BY name
            """
        ).fetchall()

    return [dict(tag) for tag in tags]


def create_tag(database_path, tag_data):
    """Create and return a reusable tag."""
    with sqlite3.connect(database_path) as connection:
        cursor = connection.execute(
            """
            INSERT INTO tag (name, type)
            VALUES (?, ?)
            """,
            (tag_data["name"], tag_data["type"]),
        )

        tag = {
            "id": cursor.lastrowid,
            "name": tag_data["name"],
            "type": tag_data["type"],
        }

    return tag


def list_notes(database_path):
    """Return every reusable note in alphabetical order."""
    with sqlite3.connect(database_path) as connection:
        connection.row_factory = sqlite3.Row

        notes = connection.execute(
            """
            SELECT id, title, note_type, body
            FROM note
            ORDER BY title
            """
        ).fetchall()

    return [dict(note) for note in notes]


def create_note(database_path, note_data):
    """Create and return a reusable note without altering its body text."""
    with sqlite3.connect(database_path) as connection:
        cursor = connection.execute(
            """
            INSERT INTO note (title, note_type, body)
            VALUES (?, ?, ?)
            """,
            (
                note_data["title"],
                note_data["note_type"],
                note_data["body"],
            ),
        )

        note = {
            "id": cursor.lastrowid,
            "title": note_data["title"],
            "note_type": note_data["note_type"],
            "body": note_data["body"],
        }

    return note


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


def delete_recipe(database_path, recipe_id):
    """Delete a recipe and report whether it existed."""
    with sqlite3.connect(database_path) as connection:
        connection.execute("PRAGMA foreign_keys = ON")

        cursor = connection.execute(
            "DELETE FROM recipe WHERE id = ?",
            (recipe_id,),
        )
        recipe_was_deleted = cursor.rowcount > 0

        return recipe_was_deleted


def attach_recipe_ingredient(database_path, recipe_id, ingredient_data):
    """Attach an existing ingredient to a recipe with its amount and unit."""
    with sqlite3.connect(database_path) as connection:
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")

        connection.execute(
            """
            INSERT INTO recipe_ingredient (
                recipe_id,
                ingredient_id,
                amount,
                unit
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                recipe_id,
                ingredient_data["ingredient_id"],
                ingredient_data["amount"],
                ingredient_data["unit"],
            ),
        )

        ingredient = connection.execute(
            """
            SELECT
                ingredient.id,
                ingredient.name,
                recipe_ingredient.amount,
                recipe_ingredient.unit
            FROM recipe_ingredient
            JOIN ingredient
                ON ingredient.id = recipe_ingredient.ingredient_id
            WHERE recipe_ingredient.recipe_id = ?
              AND recipe_ingredient.ingredient_id = ?
            """,
            (
                recipe_id,
                ingredient_data["ingredient_id"],
            ),
        ).fetchone()

    return dict(ingredient)


def update_recipe_ingredient(
    database_path,
    recipe_id,
    ingredient_id,
    ingredient_data,
):
    """Update and return a recipe ingredient relationship."""
    with sqlite3.connect(database_path) as connection:
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")

        cursor = connection.execute(
            """
            UPDATE recipe_ingredient
            SET amount = ?, unit = ?
            WHERE recipe_id = ?
              AND ingredient_id = ?
            """,
            (
                ingredient_data["amount"],
                ingredient_data["unit"],
                recipe_id,
                ingredient_id,
            ),
        )

        if cursor.rowcount == 0:
            return None

        ingredient = connection.execute(
            """
            SELECT
                ingredient.id,
                ingredient.name,
                recipe_ingredient.amount,
                recipe_ingredient.unit
            FROM recipe_ingredient
            JOIN ingredient
                ON ingredient.id = recipe_ingredient.ingredient_id
            WHERE recipe_ingredient.recipe_id = ?
              AND recipe_ingredient.ingredient_id = ?
            """,
            (recipe_id, ingredient_id),
        ).fetchone()

    return dict(ingredient)


def remove_recipe_ingredient(database_path, recipe_id, ingredient_id):
    """Remove an ingredient from a recipe without deleting the ingredient."""
    with sqlite3.connect(database_path) as connection:
        connection.execute("PRAGMA foreign_keys = ON")

        cursor = connection.execute(
            """
            DELETE FROM recipe_ingredient
            WHERE recipe_id = ?
                AND ingredient_id = ?
            """,
            (recipe_id, ingredient_id),
        )

        relationship_was_deleted = cursor.rowcount > 0

    return relationship_was_deleted


def replace_recipe_steps(database_path, recipe_id, instructions):
    """Replace and return all ordered steps for one recipe."""
    with sqlite3.connect(database_path) as connection:
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")

        recipe_exists = connection.execute(
            "SELECT 1 FROM recipe WHERE id = ?",
            (recipe_id,),
        ).fetchone()

        if recipe_exists is None:
            return None

        connection.execute(
            "DELETE FROM recipe_step WHERE recipe_id = ?",
            (recipe_id,),
        )

        connection.executemany(
            """
            INSERT INTO recipe_step (
                recipe_id,
                step_number,
                instruction
            )
            VALUES (?, ?, ?)
            """,
            [
                (recipe_id, step_number, instruction)
                for step_number, instruction in enumerate(
                    instructions,
                    start=1,
                )
            ],
        )

        steps = connection.execute(
            """
            SELECT id, step_number, instruction
            FROM recipe_step
            WHERE recipe_id = ?
            ORDER BY step_number
            """,
            (recipe_id,),
        ).fetchall()

    return [dict(step) for step in steps]


def attach_recipe_tag(database_path, recipe_id, tag_id):
    """Attach an existing reusable tag to a recipe."""
    with sqlite3.connect(database_path) as connection:
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")

        connection.execute(
            """
            INSERT INTO recipe_tag (recipe_id, tag_id)
            VALUES (?, ?)
            """,
            (recipe_id, tag_id),
        )

        tag = connection.execute(
            """
            SELECT tag.id, tag.name, tag.type
            FROM recipe_tag
            JOIN tag ON tag.id = recipe_tag.tag_id
            WHERE recipe_tag.recipe_id = ?
              AND recipe_tag.tag_id = ?
            """,
            (recipe_id, tag_id),
        ).fetchone()

    return dict(tag)


def remove_recipe_tag(database_path, recipe_id, tag_id):
    """Remove a tag from a recipe without deleting the reusable tag."""
    with sqlite3.connect(database_path) as connection:
        connection.execute("PRAGMA foreign_keys = ON")

        cursor = connection.execute(
            """
            DELETE FROM recipe_tag
            WHERE recipe_id = ?
              AND tag_id = ?
            """,
            (recipe_id, tag_id),
        )

        relationship_was_deleted = cursor.rowcount > 0

    return relationship_was_deleted


def attach_recipe_note(database_path, recipe_id, note_id):
    """Attach an existing reusable note to a recipe."""
    with sqlite3.connect(database_path) as connection:
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")

        connection.execute(
            """
            INSERT INTO recipe_note (recipe_id, note_id)
            VALUES (?, ?)
            """,
            (recipe_id, note_id),
        )

        note = connection.execute(
            """
            SELECT note.id, note.title, note.note_type, note.body
            FROM recipe_note
            JOIN note ON note.id = recipe_note.note_id
            WHERE recipe_note.recipe_id = ?
              AND recipe_note.note_id = ?
            """,
            (recipe_id, note_id),
        ).fetchone()

    return dict(note)


def remove_recipe_note(database_path, recipe_id, note_id):
    """Remove a note from a recipe without deleting the reusable note."""
    with sqlite3.connect(database_path) as connection:
        connection.execute("PRAGMA foreign_keys = ON")

        cursor = connection.execute(
            """
            DELETE FROM recipe_note
            WHERE recipe_id = ?
              AND note_id = ?
            """,
            (recipe_id, note_id),
        )

        relationship_was_deleted = cursor.rowcount > 0

    return relationship_was_deleted
