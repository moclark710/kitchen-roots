import sqlite3
from pathlib import Path
from flask import Flask, jsonify, render_template, request
from database.recipe_repository import (
    attach_recipe_ingredient,
    attach_recipe_note,
    attach_recipe_tag,
    create_tag,
    create_recipe,
    delete_recipe,
    get_recipe,
    list_recipes,
    replace_recipe_steps,
    create_ingredient,
    list_ingredients,
    list_tags,
    update_recipe_ingredient,
    remove_recipe_ingredient,
    remove_recipe_note,
    remove_recipe_tag,
    update_recipe,
)

PROJECT_ROOT = Path(__file__).resolve().parent


def find_recipe_validation_error(recipe_data, partial=False):
    """Return a validation message, or None when recipe data is valid."""
    if not isinstance(recipe_data, dict):
        return "Recipe data is required."

    if (not partial or "title" in recipe_data) and not (
        recipe_data.get("title") or ""
    ).strip():
        return "Title is required."

    if (not partial or "description" in recipe_data) and not (
        recipe_data.get("description") or ""
    ).strip():
        return "Description is required."

    prep_time = recipe_data.get("prep_time")
    if not partial or "prep_time" in recipe_data:
        if (
            not isinstance(prep_time, int)
            or isinstance(prep_time, bool)
            or prep_time < 0
        ):
            return "Prep time must be zero or greater."

    cook_time = recipe_data.get("cook_time")
    if not partial or "cook_time" in recipe_data:
        if (
            not isinstance(cook_time, int)
            or isinstance(cook_time, bool)
            or cook_time < 0
        ):
            return "Cook time must be zero or greater."

    user_id = recipe_data.get("user_id")
    if not partial or "user_id" in recipe_data:
        if (
            not isinstance(user_id, int)
            or isinstance(user_id, bool)
            or user_id <= 0
        ):
            return "User is required."

    return None


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        DATABASE_PATH=PROJECT_ROOT / "instance" / "kitchen_roots.db"
    )

    if test_config:
        app.config.update(test_config)

    @app.errorhandler(sqlite3.Error)
    def handle_database_error(error):
        app.logger.error("Database operation failed: %s", error)
        return jsonify(error="A database error occurred."), 500

    @app.get("/recipes")
    def recipe_collection_page():
        return render_template("recipes.html")

    @app.get("/recipes/<int:recipe_id>")
    def recipe_detail_page(recipe_id):
        return render_template("recipe.html", recipe_id=recipe_id)

    @app.get("/")
    def landing_page():
        return render_template("landing.html")

    @app.get("/api/recipes")
    def recipe_list():
        tag_value = request.args.get("tag_id")
        tag_id = None

        if tag_value:
            try:
                tag_id = int(tag_value)
            except ValueError:
                return jsonify(error="Tag filter must be a positive integer."), 400

            if tag_id <= 0:
                return jsonify(error="Tag filter must be a positive integer."), 400

        recipes = list_recipes(
            app.config["DATABASE_PATH"],
            tag_id=tag_id,
        )
        return jsonify(recipes)

    @app.post("/api/recipes")
    def recipe_create():
        recipe_data = request.get_json(silent=True)
        validation_error = find_recipe_validation_error(recipe_data)

        if validation_error:
            return jsonify(error=validation_error), 400

        recipe = create_recipe(
            app.config["DATABASE_PATH"],
            recipe_data,
        )
        return jsonify(recipe), 201

    @app.get("/recipes/new")
    def new_recipe_page():
        return render_template("new_recipe.html")

    @app.get("/api/recipes/<int:recipe_id>")
    def recipe_detail(recipe_id):
        recipe = get_recipe(app.config["DATABASE_PATH"], recipe_id)
        if recipe is None:
            return jsonify(error="Recipe not found."), 404
        return jsonify(recipe)

    @app.get("/api/ingredients")
    def ingredient_list():
        ingredients = list_ingredients(app.config["DATABASE_PATH"])
        return jsonify(ingredients)

    @app.post("/api/ingredients")
    def ingredient_create():
        ingredient_data = request.get_json(silent=True)
        ingredient = create_ingredient(
            app.config["DATABASE_PATH"],
            ingredient_data,
        )
        return jsonify(ingredient), 201

    @app.get("/api/tags")
    def tag_list():
        tags = list_tags(app.config["DATABASE_PATH"])
        return jsonify(tags)

    @app.post("/api/tags")
    def tag_create():
        tag_data = request.get_json(silent=True)

        if not isinstance(tag_data, dict):
            return jsonify(error="Tag data is required."), 400

        name = tag_data.get("name")
        tag_type = tag_data.get("type")

        if not isinstance(name, str) or not name.strip():
            return jsonify(error="Tag name is required."), 400

        if not isinstance(tag_type, str) or not tag_type.strip():
            return jsonify(error="Tag type is required."), 400

        tag = create_tag(
            app.config["DATABASE_PATH"],
            {
                "name": name.strip(),
                "type": tag_type.strip(),
            },
        )
        return jsonify(tag), 201

    @app.post("/api/recipes/<int:recipe_id>/ingredients")
    def recipe_ingredient_create(recipe_id):
        ingredient_data = request.get_json(silent=True)
        ingredient = attach_recipe_ingredient(
            app.config["DATABASE_PATH"],
            recipe_id,
            ingredient_data,
        )
        return jsonify(ingredient), 201

    @app.patch("/api/recipes/<int:recipe_id>/ingredients/<int:ingredient_id>")
    def recipe_ingredient_update(recipe_id, ingredient_id):
        ingredient_data = request.get_json(silent=True)
        ingredient = update_recipe_ingredient(
            app.config["DATABASE_PATH"],
            recipe_id,
            ingredient_id,
            ingredient_data,
        )

        if ingredient is None:
            return jsonify(error="Recipe ingredient not found."), 404

        return jsonify(ingredient)

    @app.delete("/api/recipes/<int:recipe_id>/ingredients/<int:ingredient_id>")
    def recipe_ingredient_delete(recipe_id, ingredient_id):
        relationship_was_deleted = remove_recipe_ingredient(
            app.config["DATABASE_PATH"],
            recipe_id,
            ingredient_id,
        )

        if not relationship_was_deleted:
            return jsonify(error="Recipe ingredient not found."), 404

        return "", 204

    @app.put("/api/recipes/<int:recipe_id>/steps")
    def recipe_steps_replace(recipe_id):
        step_data = request.get_json(silent=True)

        if not isinstance(step_data, dict) or not isinstance(
            step_data.get("steps"),
            list,
        ):
            return jsonify(error="Recipe steps are required."), 400

        instructions = step_data["steps"]

        if any(
            not isinstance(instruction, str) or not instruction.strip()
            for instruction in instructions
        ):
            return jsonify(error="Every recipe step requires instructions."), 400

        steps = replace_recipe_steps(
            app.config["DATABASE_PATH"],
            recipe_id,
            instructions,
        )

        if steps is None:
            return jsonify(error="Recipe not found."), 404

        return jsonify(steps)

    @app.post("/api/recipes/<int:recipe_id>/tags")
    def recipe_tag_create(recipe_id):
        tag_data = request.get_json(silent=True)
        tag = attach_recipe_tag(
            app.config["DATABASE_PATH"],
            recipe_id,
            tag_data["tag_id"],
        )
        return jsonify(tag), 201

    @app.delete("/api/recipes/<int:recipe_id>/tags/<int:tag_id>")
    def recipe_tag_delete(recipe_id, tag_id):
        relationship_was_deleted = remove_recipe_tag(
            app.config["DATABASE_PATH"],
            recipe_id,
            tag_id,
        )

        if not relationship_was_deleted:
            return jsonify(error="Recipe tag not found."), 404

        return "", 204

    @app.post("/api/recipes/<int:recipe_id>/notes")
    def recipe_note_create(recipe_id):
        note_data = request.get_json(silent=True)
        note = attach_recipe_note(
            app.config["DATABASE_PATH"],
            recipe_id,
            note_data["note_id"],
        )
        return jsonify(note), 201

    @app.delete("/api/recipes/<int:recipe_id>/notes/<int:note_id>")
    def recipe_note_delete(recipe_id, note_id):
        relationship_was_deleted = remove_recipe_note(
            app.config["DATABASE_PATH"],
            recipe_id,
            note_id,
        )

        if not relationship_was_deleted:
            return jsonify(error="Recipe note not found."), 404

        return "", 204

    @app.patch("/api/recipes/<int:recipe_id>")
    def recipe_update(recipe_id):
        recipe_data = request.get_json(silent=True)
        validation_error = find_recipe_validation_error(
            recipe_data,
            partial=True,
        )

        if validation_error:
            return jsonify(error=validation_error), 400

        recipe = update_recipe(
            app.config["DATABASE_PATH"],
            recipe_id,
            recipe_data,
        )

        if recipe is None:
            return jsonify(error="Recipe not found."), 404

        return jsonify(recipe)

    @app.delete("/api/recipes/<int:recipe_id>")
    def recipe_delete(recipe_id):
        recipe_was_deleted = delete_recipe(
            app.config["DATABASE_PATH"],
            recipe_id,
        )

        if not recipe_was_deleted:
            return jsonify(error="Recipe not found."), 404

        return "", 204

    @app.get("/recipes/<int:recipe_id>/edit")
    def edit_recipe_page(recipe_id):
        return render_template(
            "edit_recipe.html",
            recipe_id=recipe_id,
        )

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
