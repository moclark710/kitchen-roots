# Kitchen Roots

Kitchen Roots is a digital family recipe book for preserving family recipes together with the personal and cultural knowledge connected to them. The initial collection will focus on Liberian family recipes and Liberian fusion cuisine developed through Krugeh Cooks.

## Project Status

Kitchen Roots is currently in database development. The SQLite schema, initialization command, Jollof Rice development seed, and database relationship tests are available.

## MVP Features

- Browse and search a collection of Recipes
- View complete wiki-style Recipe pages
- Create, edit, and delete Recipes
- Record Ingredients with Recipe-specific amounts and units
- Record ordered cooking steps
- Organize Recipes with reusable Tags
- Connect Recipes to family, regional, heritage, and technique Notes

## Technology Stack

- **Frontend:** HTML, CSS, and vanilla JavaScript
- **Backend:** Python and Flask
- **Database:** SQLite3
- **Version control:** Git and GitHub

## Architecture

Kitchen Roots will use a three-tier architecture consisting of a browser-based frontend, a Flask API and application layer, and a SQLite3 data layer.

## Project Documentation

- [MVP Specification](docs/SPEC.md)
- [Project One-Pager](docs/KitchenRoots_OnePager.pdf)
- [Pitch-Style One-Pager](docs/KitchenRoots_OnePager_v2_PitchStyle.pdf)
- [Data Model UML v7.1](docs/KitchenRoots_DataModel_v7_1.pdf)
- [UI/UX Mockup](docs/KitchenRoots_UXMockup.pdf)
- [Sample Wiki Recipe: Jollof Rice](docs/KitchenRoots_WikiRecipe_JollofRice.pdf)

## Local Setup

Create an empty development database:

```bash
python3 database/init_db.py
```

Create the database and load the Jollof Rice development data:

```bash
python3 database/init_db.py --seed
```

For a quick Phase 2 demo, inspect the seeded recipe and its related record counts:

```bash
sqlite3 instance/kitchen_roots.db "SELECT title FROM recipe; SELECT COUNT(*) AS ingredients FROM recipe_ingredient; SELECT COUNT(*) AS steps FROM recipe_step;"
```

Run the database test suite:

```bash
python3 -m unittest discover -s tests -v
```

## Author

Monah Clark
