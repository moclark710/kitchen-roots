const recipeList = document.querySelector("#recipe-list");
const tagFilterForm = document.querySelector("#tag-filter-form");
const tagFilterSelect = document.querySelector("#tag-filter");
const clearFilterButton = document.querySelector("[data-clear-filter]");
const filterMessage = document.querySelector("#filter-message");

function createRecipeCard(recipe) {
  const card = document.createElement("article");
  card.className = "recipe-card";

  const title = document.createElement("h2");
  const link = document.createElement("a");
  link.href = `/recipes/${recipe.id}`;
  link.textContent = recipe.title;
  title.append(link);

  const author = document.createElement("p");
  author.className = "recipe-author";
  author.textContent = `From ${recipe.user.name}'s kitchen`;

  const description = document.createElement("p");
  description.textContent = recipe.description;

  card.append(author, title, description);
  return card;
}

async function loadTagFilters() {
  try {
    const response = await fetch("/api/tags");
    const tags = await response.json();

    if (!response.ok) {
      throw new Error(tags.error || "Unable to load tag filters.");
    }

    tags.forEach((tag) => {
      const option = document.createElement("option");
      option.value = tag.id;
      option.textContent = tag.name;
      tagFilterSelect.append(option);
    });
  } catch (error) {
    filterMessage.textContent = error.message;
  }
}

async function loadRecipes(tagId = "") {
  recipeList.innerHTML = '<p class="loading">Loading recipes...</p>';

  try {
    const query = tagId ? `?tag_id=${encodeURIComponent(tagId)}` : "";
    const response = await fetch(`/api/recipes${query}`);
    const recipes = await response.json();

    if (!response.ok) {
      throw new Error("Unable to load recipes.");
    }

    if (recipes.length === 0) {
      recipeList.textContent = tagId
        ? "No recipes match this tag."
        : "No recipes are available yet.";
      return;
    }

    const cards = recipes.map(createRecipeCard);
    recipeList.replaceChildren(...cards);
  } catch (error) {
    recipeList.textContent = error.message;
    recipeList.className = "error-message";
  }
}

tagFilterForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const selectedOption = tagFilterSelect.selectedOptions[0];

  filterMessage.textContent = tagFilterSelect.value
    ? `Showing recipes tagged ${selectedOption.textContent}.`
    : "Showing all recipes.";

  loadRecipes(tagFilterSelect.value);
});

clearFilterButton.addEventListener("click", () => {
  tagFilterSelect.value = "";
  filterMessage.textContent = "Showing all recipes.";
  loadRecipes();
});

loadTagFilters();
loadRecipes();
