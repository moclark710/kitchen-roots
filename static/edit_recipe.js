const editRecipeForm = document.querySelector("#edit-recipe-form");
const formMessage = document.querySelector("#form-message");
const recipeId = editRecipeForm.dataset.recipeId;

const titleInput = document.querySelector("#title");
const descriptionInput = document.querySelector("#description");
const prepTimeInput = document.querySelector("#prep-time");
const cookTimeInput = document.querySelector("#cook-time");
const ingredientList = document.querySelector("[data-ingredient-list]");
const ingredientForm = document.querySelector("#ingredient-form");
const ingredientSelect = document.querySelector("#ingredient-id");
const ingredientNameInput = document.querySelector("#ingredient-name");
const ingredientAmountInput = document.querySelector("#ingredient-amount");
const ingredientUnitInput = document.querySelector("#ingredient-unit");
const ingredientMessage = document.querySelector("#ingredient-message");
let currentIngredients = [];

async function removeIngredient(ingredientId) {
  const confirmed = window.confirm(
    "Remove this ingredient from the recipe?"
  );

  if (!confirmed) {
    return;
  }

  ingredientMessage.textContent = "Removing ingredient...";

  try {
    const response = await fetch(
      `/api/recipes/${recipeId}/ingredients/${ingredientId}`,
      {
        method: "DELETE",
      }
    );

    if (!response.ok) {
      const data = await response.json();
      throw new Error(data.error || "Unable to remove the ingredient.");
    }

    await loadRecipeForEditing();
    ingredientMessage.textContent = "Ingredient removed.";
  } catch (error) {
    ingredientMessage.textContent = error.message;
  }
}

function renderIngredients(ingredients) {
  currentIngredients = ingredients;
  ingredientList.replaceChildren();

  if (ingredients.length === 0) {
    const emptyMessage = document.createElement("li");
    emptyMessage.className = "ingredient-empty-message";
    emptyMessage.textContent = "No ingredients added yet...";
    ingredientList.append(emptyMessage);
    return;
  }

  ingredients.forEach((ingredient) => {
    const item = document.createElement("li");
    const measurement = `${ingredient.amount} ${ingredient.unit}`.trim();

    const measurementElement = document.createElement("span");
    measurementElement.className = "measurement";
    measurementElement.textContent = measurement;

    const removeButton = document.createElement("button");
    removeButton.type = "button";
    removeButton.className = "ingredient-remove-button";
    removeButton.textContent = "Remove";

    removeButton.addEventListener("click", () => {
      removeIngredient(ingredient.id);
    });

    item.append(
      measurementElement,
      document.createTextNode(ingredient.name),
      removeButton
    );

    ingredientList.append(item);
  });
}

async function loadIngredientOptions() {
  try {
    const response = await fetch("/api/ingredients");
    const ingredients = await response.json();

    if (!response.ok) {
      throw new Error(
        ingredients.error || "Unable to load ingredient choices."
      );
    }

    ingredientSelect.length = 1;

    ingredients.forEach((ingredient) => {
      const option = document.createElement("option");
      option.value = ingredient.id;
      option.textContent = ingredient.name;
      ingredientSelect.append(option);
    });
  } catch (error) {
    ingredientMessage.textContent = error.message;
  }
}

ingredientSelect.addEventListener("change", () => {
  const selectedIngredient = currentIngredients.find(
    (ingredient) => ingredient.id === Number(ingredientSelect.value)
  );

  if (!selectedIngredient) {
    return;
  }

  ingredientNameInput.value = "";
  ingredientAmountInput.value = selectedIngredient.amount;
  ingredientUnitInput.value = selectedIngredient.unit;
});

ingredientNameInput.addEventListener("input", () => {
  if (ingredientNameInput.value.trim()) {
    ingredientSelect.value = "";
  }
});

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
    renderIngredients(recipe.ingredients);
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

ingredientForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  ingredientMessage.textContent = "Saving ingredient...";

  let ingredientId = Number(ingredientSelect.value);
  const newIngredientName = ingredientNameInput.value.trim();

  try {
    if (!ingredientId && !newIngredientName) {
      throw new Error(
        "Choose an existing ingredient or enter a new ingredient."
      );
    }

    if (newIngredientName) {
      const createResponse = await fetch("/api/ingredients", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name: newIngredientName,
        }),
      });

      const createdIngredient = await createResponse.json();

      if (!createResponse.ok) {
        throw new Error(
          createdIngredient.error || "Unable to create the ingredient."
        );
      }

      ingredientId = createdIngredient.id;
    }

    const ingredientIsAttached = currentIngredients.some(
      (ingredient) => ingredient.id === ingredientId
    );

    const relationshipUrl = ingredientIsAttached
      ? `/api/recipes/${recipeId}/ingredients/${ingredientId}`
      : `/api/recipes/${recipeId}/ingredients`;

    const relationshipData = {
      amount: ingredientAmountInput.value.trim(),
      unit: ingredientUnitInput.value.trim(),
    };

    if (!ingredientIsAttached) {
      relationshipData.ingredient_id = ingredientId;
    }

    const saveResponse = await fetch(relationshipUrl, {
      method: ingredientIsAttached ? "PATCH" : "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(relationshipData),
    });

    const savedIngredient = await saveResponse.json();

    if (!saveResponse.ok) {
      throw new Error(
        savedIngredient.error || "Unable to save the ingredient."
      );
    }

    ingredientForm.reset();
    await loadRecipeForEditing();
    await loadIngredientOptions();

    ingredientMessage.textContent = ingredientIsAttached
      ? "Ingredient updated."
      : "Ingredient added.";
  } catch (error) {
    ingredientMessage.textContent = error.message;
  }
});

loadRecipeForEditing();
loadIngredientOptions();
