-- Development seed data based on docs/KitchenRoots_WikiRecipe_JollofRice.pdf.
-- Run only after database/schema.sql has created the tables.

BEGIN TRANSACTION;

INSERT INTO user (id, name, email, tier)
VALUES (1, 'KrugehCooks', 'demo@kitchenroots.local', 'free');

INSERT INTO recipe (id, title, description, user_id, prep_time, tier)
VALUES (
    1,
    'Liberian Jollof Rice',
    'A bold Liberian-style jollof rice made with a tomato-pepper base, long-grain rice, assorted meats, and vegetables in one large pot.',
    1,
    0,
    'free'
);

INSERT INTO ingredient (id, name) VALUES
    (1, 'Long-grain rice, rinsed'),
    (2, 'Large tomatoes, blended'),
    (3, 'Red bell pepper, blended'),
    (4, 'Scotch bonnet or habanero pepper, blended'),
    (5, 'Large onion, divided'),
    (6, 'Cooking oil'),
    (7, 'Tomato paste'),
    (8, 'Chicken or beef stock'),
    (9, 'Assorted chicken, beef, and sausage'),
    (10, 'Mixed vegetables'),
    (11, 'Garlic, minced'),
    (12, 'Bay leaves'),
    (13, 'Thyme, bouillon, or seasoning cubes'),
    (14, 'Salt and pepper');

INSERT INTO recipe_ingredient (recipe_id, ingredient_id, amount, unit) VALUES
    (1, 1, '2', 'cups'),
    (1, 2, '3', 'whole'),
    (1, 3, '1', 'whole'),
    (1, 4, '1', 'whole'),
    (1, 5, '1', 'whole'),
    (1, 6, '1/4', 'cup'),
    (1, 7, '2', 'tbsp'),
    (1, 8, '2', 'cups'),
    (1, 9, 'as desired', 'mixed pieces'),
    (1, 10, 'as desired', 'mixed vegetables'),
    (1, 11, '2', 'cloves'),
    (1, 12, '2', 'leaves'),
    (1, 13, '1', 'tsp'),
    (1, 14, 'to taste', 'seasoning');

INSERT INTO recipe_step (id, recipe_id, step_number, instruction) VALUES
    (1, 1, 1, 'Blend tomatoes, bell pepper, hot pepper, and half the onion into a smooth base.'),
    (2, 1, 2, 'Heat oil in a heavy, oven-safe pot; saute the sliced onion and garlic until fragrant.'),
    (3, 1, 3, 'Stir in tomato paste and cook for 2-3 minutes to deepen the color.'),
    (4, 1, 4, 'Add the blended base and bay leaves; simmer uncovered until thickened and reduced.'),
    (5, 1, 5, 'Stir in stock, thyme, and seasoning; bring to a boil.'),
    (6, 1, 6, 'Add rinsed rice, stir to coat, cover the pot, and move it into the oven to finish cooking.'),
    (7, 1, 7, 'Check once partway through to fluff and prevent sticking; continue until the rice is tender.'),
    (8, 1, 8, 'Fold in the browned proteins, sausage, and mixed vegetables near the end to warm through.'),
    (9, 1, 9, 'Rest covered for a few minutes, then fluff and serve family-style from the pot.');

INSERT INTO tag (id, name, type) VALUES
    (1, 'West African', 'region'),
    (2, 'One-Pot', 'style'),
    (3, 'Rice', 'dish'),
    (4, 'Family Recipe', 'collection');

INSERT INTO recipe_tag (recipe_id, tag_id) VALUES
    (1, 1), (1, 2), (1, 3), (1, 4);

INSERT INTO note (id, title, note_type, body) VALUES
    (1, 'Family Story', 'family', 'This dish was a specialty learned from the contributor''s mother and was made several times a year, including for the contributor''s father''s birthday.'),
    (2, 'About This Dish', 'region', 'Jollof rice originated with the Wolof people of Senegal and spread across West Africa, with each country and family developing its own version.'),
    (3, 'Stove-to-Oven Finish', 'technical', 'Starting the rice on the stove and finishing it covered in the oven builds the deep color and flavor distinct to this family version.'),
    (4, 'Heritage Note', 'heritage', 'West African rice cultivation and one-pot cookery influenced Gullah Geechee cuisine in the American South; jollof rice and Gullah red rice share related foundations.');

INSERT INTO recipe_note (recipe_id, note_id) VALUES
    (1, 1), (1, 2), (1, 3), (1, 4);

COMMIT;
