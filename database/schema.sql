-- Kitchen Roots database schema
-- Based on Kitchen Roots UML v7.1

PRAGMA foreign_keys = ON; 
-- tells sqlite to enforce relationships defined by foreign keys

CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    --gives user free tier since no tier implementation exists
    tier TEXT NOT NULL DEFAULT 'free' 
);

CREATE TABLE IF NOT EXISTS ingredient (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS tag (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS note (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    note_type TEXT NOT NULL,
    body TEXT NOT NULL
);


CREATE TABLE IF NOT EXISTS recipe (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    prep_time INTEGER NOT NULL CHECK (prep_time >= 0),
    cook_time INTEGER NOT NULL DEFAULT 0 CHECK (cook_time >= 0),
    tier TEXT NOT NULL DEFAULT 'free',
    FOREIGN KEY (user_id) REFERENCES user(id)
);

CREATE TABLE IF NOT EXISTS recipe_step (
    id INTEGER PRIMARY KEY,
    recipe_id INTEGER NOT NULL,
    step_number INTEGER NOT NULL CHECK (step_number > 0 ),
    instruction TEXT NOT NULL,
    UNIQUE (recipe_id, step_number),
    FOREIGN KEY (recipe_id) REFERENCES recipe(id) ON DELETE CASCADE
);

CREATE TABLE  IF NOT EXISTS recipe_ingredient (
    recipe_id INTEGER NOT NULL,
    ingredient_id INTEGER NOT NULL,
    amount TEXT NOT NULL,
    unit TEXT NOT NULL,
    PRIMARY KEY (recipe_id, ingredient_id),
    FOREIGN KEY (recipe_id) REFERENCES recipe(id) ON DELETE CASCADE,
    FOREIGN KEY (ingredient_id) REFERENCES ingredient(id) ON DELETE CASCADE
);


CREATE TABLE  IF NOT EXISTS recipe_tag (
    recipe_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    PRIMARY KEY (recipe_id, tag_id),
    FOREIGN KEY (recipe_id) REFERENCES recipe(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tag(id) ON DELETE CASCADE
);

CREATE TABLE  IF NOT EXISTS recipe_note (
    recipe_id INTEGER NOT NULL,
    note_id INTEGER NOT NULL,
    PRIMARY KEY (recipe_id, note_id),
    FOREIGN KEY (recipe_id) REFERENCES recipe(id) ON DELETE CASCADE,
    FOREIGN KEY (note_id) REFERENCES note(id) ON DELETE CASCADE
);

-- run sqlite3 :memory: ".read database/schema.sql" ".tables"
-- to check for syntax errors without creating a database file
-- then displays tables that were successfully created