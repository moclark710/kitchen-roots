const editRecipeForm = document.querySelector("#edit-recipe-form");
const formMessage = document.querySelector("#form-message");
const recipeId = editRecipeForm.dataset.recipeId;

const titleInput = document.querySelector("#title");
const descriptionInput = document.querySelector("#description");
const prepTimeInput = document.querySelector("#prep-time");
const cookTimeInput = document.querySelector("#cook-time");

async function loadRecipeForEditing() {
  try {
    const response = await fetch(`/api/recipes/${recipeId}`);
    const recipe = await response.json();

    if (!response.ok) {
      throw new Error(recipe.error || "Unable to load this recipe.");
    }

    titleInput.value = recipe.title;
    descriptionInput.value = recipe.description;
    prepTimeInput.value = recipe.prep_time;
    cookTimeInput.value = recipe.cook_time;
    formMessage.textContent = "";
  } catch (error) {
    formMessage.textContent = error.message;
  }
}

editRecipeForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  formMessage.textContent = "Updating recipe...";

  const recipeData = {
    title: titleInput.value.trim(),
    description: descriptionInput.value.trim(),
    prep_time: Number(prepTimeInput.value),
    cook_time: Number(cookTimeInput.value),
  };

  try {
    const response = await fetch(`/api/recipes/${recipeId}`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(recipeData),
    });

    const recipe = await response.json();

    if (!response.ok) {
      throw new Error(recipe.error || "Unable to update this recipe.");
    }

    window.location.href = `/recipes/${recipe.id}`;
  } catch (error) {
    formMessage.textContent = error.message;
  }
});

loadRecipeForEditing();
