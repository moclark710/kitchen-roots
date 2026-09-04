from pathlib import Path

from flask import Flask, jsonify, render_template

from database.recipe_repository import get_recipe


PROJECT_ROOT = Path(__file__).resolve().parent


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        DATABASE_PATH=PROJECT_ROOT / "instance" / "kitchen_roots.db"
    )

    if test_config:
        app.config.update(test_config)

    @app.get("/")
    def recipe_page():
        return render_template("recipe.html")

    @app.get("/api/recipes/<int:recipe_id>")
    def recipe_detail(recipe_id):
        recipe = get_recipe(app.config["DATABASE_PATH"], recipe_id)
        if recipe is None:
            return jsonify(error="Recipe not found."), 404
        return jsonify(recipe)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
