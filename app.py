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


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        DATABASE_PATH=PROJECT_ROOT / "instance" / "kitchen_roots.db"
    )

    if test_config:
        app.config.update(test_config)

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
        recipe_data = request.get_json()
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
        recipe_data = request.get_json()
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
