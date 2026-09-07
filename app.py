import sqlite3
from pathlib import Path
from flask import Flask, jsonify, render_template, request
from database.recipe_repository import (
    create_recipe,
    delete_recipe,
    get_recipe,
    list_recipes,
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
    def recipe_page():
        return render_template("recipe.html")

    @app.get("/api/recipes")
    def recipe_list():
        recipes = list_recipes(app.config["DATABASE_PATH"])
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
