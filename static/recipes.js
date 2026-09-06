const recipeList = document.querySelector("#recipe-list");

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

async function loadRecipes() {
  try {
    const response = await fetch("/api/recipes");
    const recipes = await response.json();

    if (!response.ok) {
      throw new Error("Unable to load recipes.");
    }

    if (recipes.length === 0) {
      recipeList.textContent = "No recipes are available yet.";
      return;
    }

    const cards = recipes.map(createRecipeCard);
    recipeList.replaceChildren(...cards);
  } catch (error) {
    recipeList.textContent = error.message;
    recipeList.className = "error-message";
  }
}

loadRecipes();