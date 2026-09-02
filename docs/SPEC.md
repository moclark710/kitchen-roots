# Kitchen Roots Project Specification

**Version:** 0.1  
**Status:** Draft  
**Author:** Monah Clark  
**Data model:** Kitchen Roots UML v7.1

## 1. Product Summary

Kitchen Roots is a digital family recipe book for preserving family recipes together with the personal and cultural knowledge connected to them. Users will be able to document ingredients, cooking steps, tags, and family stories, and associate recipes with regional context and heritage notes. Unlike a conventional recipe application, Kitchen Roots treats the origin and lineage of a dish as an important part of the recipe. The initial collection will focus on Liberian dishes, family recipes, and Liberian fusion cuisine developed through Krugeh Cooks.

## 1.1 Core Content Principle

Kitchen Roots is built to preserve authentic family Recipes, cooking knowledge, personal stories, and cultural history. 

Recipes, instructions, family stories, and cultural or heritage Notes must be created and reviewed by users.

Reusable Tags and cultural or heritage Notes may be curated for use across multiple Recipes.

The application may eventually recommend relevant existing Tags and Notes based on Recipe information, but users must review and approve those suggestions before they are attached to a Recipe.

## 2. Problem Statement

Family recipes are often passed down through memory and informal cooking lessons without written measurements, ingredient lists, or helpful tips and techniques. As a result, measurements, techniques, family stories, and cultural context can change, become separated, or be lost over time. Traditional recipe applications focus primarily on ingredients and instructions, leaving little room to preserve where a dish comes from, who passed it down, or how it connects to a family’s history. Kitchen Roots addresses this problem by preserving each recipe together with its personal and cultural context in one structured, searchable application.

## 3. Project Goals

- Preserve family recipes in a consistent, structured format.
- Preserve the family stories and cultural knowledge connected to each recipe.
- Allow users to browse and search a collection of recipes.
- Record recipe-specific ingredient amounts and units.
- Organize recipes using reusable tags.
- Connect recipes to reusable notes about family, region, heritage, and cooking techniques.
- Create a foundation that can support additional recipes and features in future versions.
- Develop practical experience with JavaScript, Flask, Python, SQLite, and full-stack application development.

## 4. MVP Scope

The Kitchen Roots MVP will allow a user to:

- Browse a collection of Recipes.
- Search Recipes by title, Tag, or other relevant information.
- View a complete wiki-style Recipe page.
- Create, edit, and delete Recipes.
- Record a Recipe’s title, description, preparation time, and ordered cooking steps.
- Add Ingredients to a Recipe with Recipe-specific amounts and units.
- Add, remove, and reorder Recipe steps.
- Organize Recipes using reusable Tags.
- Connect Recipes to reusable Notes about family stories, regions, heritage, and cooking techniques.
- View all Ingredients, Tags, Notes, and cooking steps associated with a Recipe.
- Associate each Recipe with an owning User.

The MVP will use an HTML, CSS, and JavaScript frontend, a Flask and Python backend, and a SQLite3 database.

Recipe instructions will be stored as ordered records in the `recipe_steps` table. Ingredient quantities will remain separate and will be stored in `recipe_ingredients` using the `amount` and `unit` fields.

## 5. Future Scope and Non-Goals

Kitchen Roots will begin as a focused MVP. The following features will not be included in the first release:

###Out of scope:

- Premium subscriptions, payments, and an active paywall
- Genealogy or Ancestry.com integration
- Social networking features such as followers, comments, or direct messaging
- Automated nutritional calculations
- Grocery ordering or third-party shopping integrations
- Downloadable ios or Android mobile applications
- A dedicated administrator dashboard for managing users or moderating content

###Possible future enhancements:

- Adding the free and premium content tiers
- Connecting dishes to family migration and genealogy records
- Expanding the Recipe collection beyond the initial Liberian and Krugeh Cooks content
- Suggesting existing tags and curated heritage notes based on a recipe’s title, ingredients, and current classifications
- Allowing users to review and approve suggested tags or notes before they are connected to a recipe
- Supporting additional recipe photos and videos
- Adding advanced Recipe discovery and filtering
- Migrating parts of the frontend to React after the JavaScript MVP is complete

## 6. Primary User

The primary Kitchen Roots user is a home cook, secret family recipe keeper, or cultural enthusiasist who wants to preserve recipes with the knowledge and memories connected to them.

This user may have recipes that were learned through observation, conversation, or informal cooking lessons rather than written instructions. They need a clear way to record ingredients, measurements, ordered cooking steps, family stories, regional context, and heritage information in one place.

The initial users will include Kitchen Roots creator and people contributing Liberian family recipes or recipes developed through Krugeh Cooks. They should be able to create, update, browse, and search recipes without needing advanced technical knowledge.

A secondary user is someone who visits Kitchen Roots to learn how to prepare a dish and understand its family or cultural background. This user primarily needs to browse, search, and read complete recipe pages.


## 7. Functional Requirements

### 7.1 Recipe Management

- The application must allow users to browse all available Recipes.
- The application must display a complete Recipe page containing its title, description, preparation time, Ingredients, ordered cooking steps, Tags, and Notes.
- A Recipe contributor must be able to create a Recipe.
- A Recipe contributor must be able to edit an existing Recipe.
- A Recipe contributor must be able to delete a Recipe.
- Deleting a Recipe must also remove its Recipe Ingredient, Recipe Step, Recipe Tag, and Recipe Note records without deleting reusable Ingredients, Tags, or Notes.

### 7.2 Ingredients and Measurements

- A Recipe contributor must be able to add one or more Ingredients to a Recipe.
- Each Ingredient connected to a Recipe must include a Recipe-specific amount and unit.
- A Recipe contributor must be able to edit an Ingredient’s amount or unit for a Recipe.
- A Recipe contributor must be able to remove an Ingredient from a Recipe.
- The same Ingredient may be reused across multiple Recipes with different amounts and units.

### 7.3 Recipe Steps

- A Recipe contributor must be able to add multiple cooking steps to a Recipe.
- Each Recipe Step must contain a step number and an instruction.
- Recipe Steps must be displayed in step-number order.
- A Recipe contributor must be able to add, edit, delete, and reorder Recipe Steps.
- Ingredient amounts and units must remain separate from Recipe Steps and must be stored through the Recipe Ingredient relationship.

### 7.4 Tags and Notes

- A Recipe contributor must be able to connect one or more reusable Tags to a Recipe.
- A Recipe contributor must be able to add Notes containing family stories, regional context, heritage information, or cooking techniques.
- Each Note must include a title, note type, and body.
- A Tag or Note may be connected to multiple Recipes.
- Removing a Tag or Note from a Recipe must remove only the relationship, not the reusable Tag or Note itself.
- Any future Tag or Note suggestions must require user approval before being connected to a Recipe.

### 7.5 Browsing and Search

- A visitor must be able to browse the Recipe collection.
- A visitor must be able to search for Recipes by title.
- A visitor must be able to find Recipes associated with a selected Tag.
- Search results must provide a way to open the complete Recipe page.
- The application must display a clear message when no matching Recipes are found.

### 7.6 Recipe Ownership

- Every Recipe must be associated with one User.
- One User may own multiple Recipes.
- The application must preserve the User associated with each Recipe.
- User registration, login, and advanced account permissions are not required for the initial MVP.

## 8. User Experience and Primary Flows

The Kitchen Roots interface will be based on the existing UI/UX mockup and adapted for a responsive website. The layout should remain usable on both desktop and mobile browser screens.

### 8.1 Browse and Search for a Recipe

1. The visitor opens the Recipe collection page.
2. The application displays the available Recipes.
3. The visitor may search by Recipe title or select a Tag.
4. The application displays matching Recipes.
5. The visitor selects a Recipe to open its complete Recipe page.
6. If no Recipes match, the application displays a clear no-results message.

### 8.2 View a Recipe

1. The visitor opens a Recipe page.
2. The application displays the Recipe’s title, description, preparation time, and owner.
3. The application displays Ingredients with their Recipe-specific amounts and units.
4. The application displays cooking instructions in step-number order.
5. The application displays the Recipe’s associated Tags and Notes.
6. The visitor may return to the Recipe collection to continue browsing.

### 8.3 Create a Recipe

1. The contributor opens the Add Recipe form.
2. The contributor enters the Recipe’s basic information.
3. The contributor adds Ingredient rows containing an Ingredient, amount, and unit.
4. The contributor adds cooking-step rows containing a step number and instruction.
5. The contributor selects or adds relevant Tags and Notes.
6. The contributor submits the form.
7. The application validates the submitted information.
8. If the information is valid, the application saves the Recipe and displays its completed Recipe page.
9. If validation fails, the application explains what must be corrected without removing the contributor’s entered information.

### 8.4 Edit a Recipe

1. The contributor opens an existing Recipe.
2. The contributor selects the edit option.
3. The application displays the Recipe’s current information.
4. The contributor updates the Recipe, Ingredients, steps, Tags, or Notes.
5. The application validates and saves the changes.
6. The updated Recipe page is displayed.

### 8.5 Delete a Recipe

1. The contributor selects the delete option from an existing Recipe.
2. The application asks the contributor to confirm the deletion.
3. After confirmation, the application deletes the Recipe and its related association records.
4. The application returns the contributor to the Recipe collection.

## 9. Technical Architecture

Kitchen Roots will use a three-tier web application architecture. Each tier has separte responsibility but work together to complete user requests.

### 9.1 Three-Tier Architecture and Request Flow

The application will contain three tiers:

1. Presentation tier (frontend): The browser interface used to view and enter information.
2. Application tier (backend): The Flask application that processes requests and applies application rules.
3. Data tier (database): The SQLite3 database that stores and retrieves application data.

The browser will not communicate directly with the database. All database operations will pass through the Flask application.

┌───────────────────────────────────┐
│ User interacts with the website   │
└───────────────────────────────────┘
                  ↓
┌───────────────────────────────────┐
│ Browser                           │
│ HTML, CSS, and JavaScript         │
│ collect input and send a HTTP     |
| request                           |
└───────────────────────────────────┘
                  ↓
┌───────────────────────────────────┐
│ Flask API                         │
│ receives and validates the request│
└───────────────────────────────────┘
                  ↓
┌───────────────────────────────────┐
│ SQLite3 Database                  │
│ stores or retrieves data          │
└───────────────────────────────────┘
                  ↓
┌───────────────────────────────────┐
│ Flask API                         │
│ creates a JSON response           │
└───────────────────────────────────┘
                  ↓
┌───────────────────────────────────┐
│ Browser                           │
│ JavaScript updates the page       │
└───────────────────────────────────┘
                  ↓
┌───────────────────────────────────┐
│ User sees the result              │
└───────────────────────────────────┘

### 9.2 Presentation Tier — HTML, CSS, and JavaScript

The presentation tier will run inside the user’s browser. It will:

- Display the Recipe collection and complete Recipe pages.
- Provide forms for creating and editing Recipes.
- Allow contributors to add Ingredient and Recipe Step rows dynamically.
- Collect search terms and Tag selections.
- Perform basic form validation before submitting information.
- Send HTTP requests to the Flask API using JavaScript.
- Display returned data, validation messages, and errors.
- Provide a responsive layout for desktop and mobile browsers.

Frontend validation will help the user correct input, but the Flask backend will perform the final validation before information is stored.

### 9.3 Application Tier — Flask and Python

The application tier will:

- Provide API endpoints for the JavaScript frontend.
- Receive and parse browser requests.
- Validate submitted Recipe data.
- Apply Recipe, Ingredient, Recipe Step, Tag, Note, and ownership rules.
- Perform create, read, update, and delete operations.
- Communicate with the SQLite3 database.
- Return application data and error messages in JSON format.
- Prevent incomplete or invalid information from being stored.

The backend will separate Flask routes, application logic, and database operations where practical so that the code remains understandable and testable.

### 9.4 Data Tier — SQLite3

The data tier will:

- Use SQLite3 for persistent application storage.
- Follow the tables and relationships defined in Kitchen Roots UML v7.1.
- Store Ingredient amounts and units in `recipe_ingredients`.
- Store ordered cooking instructions in `recipe_steps`.
- Store reusable Recipe relationships through `recipe_tags` and `recipe_notes`.
- Enforce primary-key, foreign-key, uniqueness, and required-field rules.
- Enable SQLite foreign-key enforcement whenever a database connection is opened.

The MVP will use Python’s built-in `sqlite3` module unless the technical stack changes later.

## 10. API Requirements

The Flask API will provide the connection between the browser interface and the SQLite3 database. JavaScript will send HTTP requests to the API, and the API will return JSON responses.

### 10.1 Recipe Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/api/recipes` | Return a list of Recipes |
| `GET` | `/api/recipes/<recipe_id>` | Return one complete Recipe |
| `POST` | `/api/recipes` | Create a Recipe and its related records |
| `PUT` | `/api/recipes/<recipe_id>` | Update a Recipe and its related records |
| `DELETE` | `/api/recipes/<recipe_id>` | Delete a Recipe and its association records |

The Recipe list endpoint will support optional search parameters:

```text
GET /api/recipes?search=jollof
GET /api/recipes?tag_id=2
```

The complete Recipe response must include:

- Basic Recipe information
- The owning User
- Ingredients with amounts and units
- Recipe Steps in step-number order
- Associated Tags
- Associated Notes

### 10.2 Supporting Resource Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/api/ingredients` | Return available reusable Ingredients |
| `POST` | `/api/ingredients` | Create an Ingredient |
| `GET` | `/api/tags` | Return available reusable Tags |
| `POST` | `/api/tags` | Create a Tag |
| `GET` | `/api/notes` | Return available reusable Notes |
| `POST` | `/api/notes` | Create a Note |

Additional update or delete endpoints for reusable Ingredients, Tags, and Notes are not required for the initial MVP.

### 10.3 Recipe Request Data

When creating or updating a Recipe, the frontend will send the Recipe information and its relationships to Flask in one JSON request.

Example:

```json
{
  "title": "Jollof Rice",
  "description": "A family-style Liberian rice dish.",
  "user_id": 1,
  "prep_time": 20,
  "tier": "free",
  "ingredients": [
    {
      "ingredient_id": 1,
      "amount": "2",
      "unit": "cups"
    }
  ],
  "steps": [
    {
      "step_number": 1,
      "instruction": "Rinse the rice."
    }
  ],
  "tag_ids": [1, 3],
  "note_ids": [2]
}
```

Preparation time will be stored as a number of minutes. Ingredient amounts will be stored as text so values such as `1/2`, `1 1/2`, or `to taste` can be recorded.

Flask will create or update the Recipe and its related records as one database operation. If any required part fails validation, the complete operation should fail so that a partially completed Recipe is not stored.

### 10.4 JSON Responses

Successful requests will return JSON data when appropriate.

A successful Recipe creation will return:

- HTTP status `201 Created`
- The ID of the new Recipe
- The saved Recipe information

A successful read or update will return:

- HTTP status `200 OK`
- The requested or updated information

A successful deletion will return:

- HTTP status `204 No Content`

### 10.5 Validation and Error Responses

The API must:

- Reject missing required fields.
- Reject IDs that do not reference existing records.
- Reject invalid Recipe Step numbers.
- Return `400 Bad Request` when submitted data is invalid.
- Return `404 Not Found` when a requested record does not exist.
- Return `500 Internal Server Error` for an unexpected server failure.
- Return a clear JSON error message that the frontend can display.

Example:

```json
{
  "error": "Recipe title is required."
}
```

The API must use parameterized SQL queries and must not build SQL statements by directly combining user-submitted text.

## 11. Data Model

The Kitchen Roots database will follow the structure defined in Kitchen Roots UML v7.1. SQLite3 will use `INTEGER` and `TEXT` data types for the MVP.

### 11.1 Tables

| Table | Fields | Purpose |
|---|---|---|
| `User` | `id INTEGER PK`, `name TEXT`, `email TEXT`, `tier TEXT` | Stores Recipe owners |
| `Recipe` | `id INTEGER PK`, `title TEXT`, `description TEXT`, `user_id INTEGER FK`, `prep_time INTEGER`, `tier TEXT` | Stores the main information for each Recipe |
| `Ingredient` | `id INTEGER PK`, `name TEXT` | Stores reusable Ingredients |
| `Recipe_Ingredient` | `recipe_id INTEGER PK/FK`, `ingredient_id INTEGER PK/FK`, `amount TEXT`, `unit TEXT` | Connects Recipes and Ingredients and records Recipe-specific measurements |
| `Recipe_Step` | `id INTEGER PK`, `recipe_id INTEGER FK`, `step_number INTEGER`, `instruction TEXT` | Stores ordered cooking instructions |
| `Tag` | `id INTEGER PK`, `name TEXT`, `type TEXT` | Stores reusable Recipe classifications |
| `Recipe_Tag` | `recipe_id INTEGER PK/FK`, `tag_id INTEGER PK/FK` | Connects Recipes and Tags |
| `Note` | `id INTEGER PK`, `title TEXT`, `note_type TEXT`, `body TEXT` | Stores reusable family, regional, heritage, and technique information |
| `Recipe_Note` | `recipe_id INTEGER PK/FK`, `note_id INTEGER PK/FK` | Connects Recipes and Notes |

`Recipe_Ingredient`, `Recipe_Tag`, and `Recipe_Note` are join tables. `Recipe_Step` is a child table, not a join table.

### 11.2 Relationships

- One `User` may own many `Recipe` records.
- Each `Recipe` belongs to one `User`.

- One `Recipe` may have many `Recipe_Ingredient` records.
- One `Ingredient` may have many `Recipe_Ingredient` records.
- `Recipe_Ingredient` resolves the many-to-many relationship between Recipes and Ingredients.

- One `Recipe` may have many `Recipe_Step` records.
- Each `Recipe_Step` belongs to one `Recipe`.

- One `Recipe` may have many `Recipe_Tag` records.
- One `Tag` may have many `Recipe_Tag` records.
- `Recipe_Tag` resolves the many-to-many relationship between Recipes and Tags.

- One `Recipe` may have many `Recipe_Note` records.
- One `Note` may have many `Recipe_Note` records.
- `Recipe_Note` resolves the many-to-many relationship between Recipes and Notes.

### 11.3 Data-Integrity Rules

- Every table must have a primary key.
- Every foreign key must reference an existing parent record.
- SQLite foreign-key enforcement must be enabled whenever a database connection is opened.
- Each Recipe must reference an existing User through `Recipe.user_id`.
- The combination of `recipe_id` and `ingredient_id` must be unique in `Recipe_Ingredient`.
- The combination of `recipe_id` and `tag_id` must be unique in `Recipe_Tag`.
- The combination of `recipe_id` and `note_id` must be unique in `Recipe_Note`.
- Each Recipe Step must have a positive step number.
- A Recipe must not contain two Recipe Steps with the same step number.
- Recipe Steps must be retrieved and displayed in step-number order.
- Ingredient `amount` and `unit` values must be stored in `Recipe_Ingredient`, not in `Ingredient` or `Recipe_Step`.
- Ingredient amounts will use `TEXT` so values such as `1/2`, `1 1/2`, `2-3`, and `to taste` can be stored.
- Recipe preparation time will use `INTEGER` and represent minutes.
- Deleting a Recipe must remove its related Recipe Ingredient, Recipe Step, Recipe Tag, and Recipe Note records.
- Deleting a Recipe must not delete reusable Ingredient, Tag, or Note records.
- Recipe creation and updates involving multiple related tables must be completed within a database transaction.
- The `tier` fields will be stored for possible future use but will not restrict content during the MVP.
- `Note.note_type` may identify categories such as `family story`, `region`, `heritage`, `technique`, or `other`.

## 12. Testing Strategy

Kitchen Roots will be tested at the database, Flask API, and frontend levels. Testing will be completed throughout development instead of when the application is finished.

### 12.1 Database Testing

Database tests will verify that:

- The database can be initialized from an empty state.
- All tables are created with the expected fields and data types.
- Primary-key and foreign-key rules are enforced.
- Join tables prevent duplicate relationships.
- Recipe Ingredients store the correct amounts and units.
- Recipe Steps are connected to the correct Recipe.
- Recipe Steps are returned in step-number order.
- Invalid foreign-key values are rejected.
- Deleting a Recipe removes its child and association records without deleting reusable Ingredients, Tags, or Notes.

### 12.2 Flask API Testing

Automated API tests will use Python and the Flask test client to verify that:

- Recipe list and detail endpoints return the expected information.
- Valid Recipe data can be created and updated.
- Recipes can be deleted successfully.
- Ingredient, Recipe Step, Tag, and Note relationships are saved correctly.
- Search and Tag filtering return appropriate Recipes.
- Invalid requests return clear error messages.
- Requests for records that do not exist return a `404 Not Found` response.
- Failed multi-table operations do not save partial Recipe data.

### 12.3 Frontend Testing

The browser interface will be tested manually to verify that:

- Recipe collection and detail pages display correctly.
- Search and Tag filtering work as expected.
- Recipe forms collect the required information.
- Ingredient and Recipe Step rows can be added and removed.
- Recipe Steps can be placed in the correct order.
- Validation and API error messages are displayed clearly.
- Create, edit, and delete flows work from beginning to end.
- The interface remains usable on desktop and mobile browser sizes.

### 12.4 End-to-End Testing

At least one complete sample Recipe will be used to test the application across all three tiers. The Jollof Rice Recipe from the existing Recipe wiki document may be used for this purpose.

The end-to-end test will confirm that a Recipe can be:

1. Entered through the browser.
2. Validated and processed by Flask.
3. Stored correctly in SQLite3.
4. Retrieved through the API.
5. Displayed as a complete Recipe page.
6. Edited and saved again.
7. Deleted without damaging reusable related records.


## 13. MVP Acceptance Criteria

The Kitchen Roots MVP will be considered complete when all of the following criteria are satisfied:

### Application Setup

- [ ] A developer can follow the `README.md` instructions to install dependencies and run the application.
- [ ] The SQLite3 database can be created from an empty state using the database initialization process.
- [ ] The database structure matches Kitchen Roots UML v7.1.
- [ ] The frontend, Flask application, and SQLite3 database operate together as a three-tier application.

### Recipe Collection

- [ ] A visitor can browse the available Recipes.
- [ ] A visitor can search for a Recipe by title.
- [ ] A visitor can find Recipes associated with a selected Tag.
- [ ] A visitor can open a complete wiki-style Recipe page.
- [ ] A clear message appears when no Recipes match a search.

### Recipe Management

- [ ] A contributor can create a Recipe.
- [ ] A contributor can edit an existing Recipe.
- [ ] A contributor can delete a Recipe after confirming the action.
- [ ] Every Recipe is associated with an existing User.
- [ ] The MVP works with its initial User record without requiring registration or login.

### Recipe Content

- [ ] A Recipe can contain multiple Ingredients.
- [ ] Each Recipe Ingredient can store its own amount and unit.
- [ ] The same Ingredient can be reused in multiple Recipes with different measurements.
- [ ] A Recipe can contain multiple cooking steps.
- [ ] Cooking steps appear in step-number order.
- [ ] A contributor can add, edit, remove, and reorder cooking steps.
- [ ] A Recipe can be connected to reusable Tags.
- [ ] A Recipe can be connected to reusable family, regional, heritage, or technique Notes.
- [ ] Removing a Tag or Note from a Recipe does not delete it from other Recipes.

### API and Data Integrity

- [ ] The frontend can retrieve and submit Recipe information through the Flask API.
- [ ] Successful API requests return the expected data and HTTP status codes.
- [ ] Invalid requests return clear error responses.
- [ ] Foreign-key and join-table rules are enforced.
- [ ] A failed multi-table operation does not create a partial Recipe.
- [ ] Deleting a Recipe removes its child and association records.
- [ ] Deleting a Recipe does not delete reusable Ingredients, Tags, or Notes.

### Testing and Documentation

- [ ] Database and Flask API tests pass.
- [ ] The Jollof Rice sample Recipe completes the end-to-end test flow.
- [ ] The primary frontend flows have been tested in a browser.
- [ ] The final project documentation reflects the implemented application.
- [ ] Features listed as future scope are not required for MVP completion.
