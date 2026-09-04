const recipeRoot = document.querySelector("#recipe");
const recipeTemplate = document.querySelector("#recipe-template");

function createTextElement(tagName, className, text) {
  const element = document.createElement(tagName);
  element.className = className;
  element.textContent = text;
  return element;
}

function renderRecipe(recipe) {
  const page = recipeTemplate.content.cloneNode(true);

  page.querySelector("[data-author]").textContent = recipe.user.name;
  page.querySelector("[data-title]").textContent = recipe.title;
  page.querySelector("[data-description]").textContent = recipe.description;

  const tags = page.querySelector("[data-tags]");
  recipe.tags.forEach((tag) => {
    tags.append(createTextElement("span", "tag", tag.name));
  });

  const ingredients = page.querySelector("[data-ingredients]");
  recipe.ingredients.forEach((ingredient) => {
    const measurement = `${ingredient.amount} ${ingredient.unit}`.trim();
    const item = document.createElement("li");
    item.append(createTextElement("strong", "measurement", measurement));
    item.append(document.createTextNode(ingredient.name));
    ingredients.append(item);
  });

  const steps = page.querySelector("[data-steps]");
  recipe.steps.forEach((step) => {
    steps.append(createTextElement("li", "step", step.instruction));
  });

  const notes = page.querySelector("[data-notes]");
  recipe.notes.forEach((note) => {
    const card = document.createElement("article");
    card.className = "note-card";
    card.append(createTextElement("p", "note-type", note.note_type));
    card.append(createTextElement("h3", "", note.title));
    card.append(createTextElement("p", "", note.body));
    notes.append(card);
  });

  recipeRoot.replaceChildren(page);
}

async function loadRecipe() {
  try {
    const response = await fetch("/api/recipes/1");
    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Unable to load this recipe.");
    }

    renderRecipe(data);
  } catch (error) {
    recipeRoot.replaceChildren(
      createTextElement("p", "error-message", error.message),
    );
  }
}

loadRecipe();
