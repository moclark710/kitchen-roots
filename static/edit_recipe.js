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
const stepEditorList = document.querySelector("[data-step-editor-list]");
const addStepButton = document.querySelector("[data-add-step]");
const saveStepsButton = document.querySelector("[data-save-steps]");
const stepMessage = document.querySelector("#step-message");
const tagEditorList = document.querySelector("[data-tag-editor-list]");
const tagForm = document.querySelector("#tag-form");
const tagSelect = document.querySelector("#tag-id");
const tagNameInput = document.querySelector("#tag-name");
const tagTypeInput = document.querySelector("#tag-type");
const tagMessage = document.querySelector("#tag-message");

let currentIngredients = [];
let currentSteps = [];
let currentTags = [];

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

function renderStepEditor(steps) {
  currentSteps = steps.map((step) => ({ ...step }));
  stepEditorList.replaceChildren();

  if (currentSteps.length === 0) {
    const emptyMessage = document.createElement("li");
    emptyMessage.textContent = "No recipe steps added yet.";
    stepEditorList.append(emptyMessage);
    return;
  }

  currentSteps.forEach((step, index) => {
    const item = document.createElement("li");

    const stepNumber = document.createElement("span");
    stepNumber.className = "step-editor-number";
    stepNumber.textContent = `Step ${index + 1}`;

    const instructionInput = document.createElement("textarea");
    instructionInput.value = step.instruction;
    instructionInput.setAttribute(
      "aria-label",
      `Instruction for step ${index + 1}`
    );

    instructionInput.addEventListener("input", () => {
      currentSteps[index].instruction = instructionInput.value;
      stepMessage.textContent = "Unsaved step changes.";
    });

    const actions = document.createElement("div");
    actions.className = "step-row-actions";

    const moveUpButton = document.createElement("button");
    moveUpButton.type = "button";
    moveUpButton.textContent = "Move up";
    moveUpButton.disabled = index === 0;

    moveUpButton.addEventListener("click", () => {
      [currentSteps[index - 1], currentSteps[index]] = [
        currentSteps[index],
        currentSteps[index - 1],
      ];

      renderStepEditor(currentSteps);
      stepMessage.textContent = "Unsaved step order.";
    });

    const moveDownButton = document.createElement("button");
    moveDownButton.type = "button";
    moveDownButton.textContent = "Move down";
    moveDownButton.disabled = index === currentSteps.length - 1;

    moveDownButton.addEventListener("click", () => {
      [currentSteps[index], currentSteps[index + 1]] = [
        currentSteps[index + 1],
        currentSteps[index],
      ];

      renderStepEditor(currentSteps);
      stepMessage.textContent = "Unsaved step order.";
    });

    const removeButton = document.createElement("button");
    removeButton.type = "button";
    removeButton.textContent = "Remove";

    removeButton.addEventListener("click", () => {
      currentSteps.splice(index, 1);
      renderStepEditor(currentSteps);
      stepMessage.textContent = "Unsaved step removed.";
    });

    actions.append(
      moveUpButton,
      moveDownButton,
      removeButton
    );

    item.append(
      stepNumber,
      instructionInput,
      actions
    );

    stepEditorList.append(item);
  });
}

async function removeTag(tagId) {
  tagMessage.textContent = "Removing tag...";

  try {
    const response = await fetch(
      `/api/recipes/${recipeId}/tags/${tagId}`,
      { method: "DELETE" }
    );

    if (!response.ok) {
      const data = await response.json();
      throw new Error(data.error || "Unable to remove the tag.");
    }

    await loadRecipeForEditing();
    tagMessage.textContent = "Tag removed.";
  } catch (error) {
    tagMessage.textContent = error.message;
  }
}

function renderTags(tags) {
  currentTags = tags;
  tagEditorList.replaceChildren();

  if (tags.length === 0) {
    const emptyMessage = document.createElement("li");
    emptyMessage.textContent = "No tags added yet.";
    tagEditorList.append(emptyMessage);
    return;
  }

  tags.forEach((tag) => {
    const item = document.createElement("li");
    const label = document.createElement("span");
    label.className = "tag";
    label.textContent = tag.name;

    const type = document.createElement("span");
    type.className = "tag-editor-type";
    type.textContent = tag.type;

    const removeButton = document.createElement("button");
    removeButton.type = "button";
    removeButton.textContent = "Remove";
    removeButton.addEventListener("click", () => removeTag(tag.id));

    item.append(label, type, removeButton);
    tagEditorList.append(item);
  });
}

async function loadTagOptions() {
  try {
    const response = await fetch("/api/tags");
    const tags = await response.json();

    if (!response.ok) {
      throw new Error(tags.error || "Unable to load tag choices.");
    }

    tagSelect.length = 1;

    tags.forEach((tag) => {
      const option = document.createElement("option");
      option.value = tag.id;
      option.textContent = `${tag.name} (${tag.type})`;
      tagSelect.append(option);
    });
  } catch (error) {
    tagMessage.textContent = error.message;
  }
}

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
    renderStepEditor(recipe.steps);
    renderTags(recipe.tags);
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

addStepButton.addEventListener("click", () => {
  currentSteps.push({
    instruction: "",
  });

  renderStepEditor(currentSteps);

  const instructionInputs = stepEditorList.querySelectorAll("textarea");
  const lastInput = instructionInputs[instructionInputs.length - 1];

  lastInput.focus();
  stepMessage.textContent = "Unsaved step added.";
});

saveStepsButton.addEventListener("click", async () => {
  const instructions = currentSteps.map((step) =>
    step.instruction.trim()
  );

  if (instructions.some((instruction) => !instruction)) {
    stepMessage.textContent = "Every step needs an instruction.";
    return;
  }

  stepMessage.textContent = "Saving recipe steps...";

  try {
    const response = await fetch(`/api/recipes/${recipeId}/steps`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        steps: instructions,
      }),
    });

    const savedSteps = await response.json();

    if (!response.ok) {
      throw new Error(savedSteps.error || "Unable to save recipe steps.");
    }

    renderStepEditor(savedSteps);
    stepMessage.textContent = "Recipe steps saved.";
  } catch (error) {
    stepMessage.textContent = error.message;
  }
});

tagSelect.addEventListener("change", () => {
  if (tagSelect.value) {
    tagNameInput.value = "";
    tagTypeInput.value = "";
  }
});

tagNameInput.addEventListener("input", () => {
  if (tagNameInput.value.trim()) {
    tagSelect.value = "";
  }
});

tagForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  let tagId = Number(tagSelect.value);
  const newTagName = tagNameInput.value.trim();
  const newTagType = tagTypeInput.value.trim();

  if (!tagId && !newTagName) {
    tagMessage.textContent = "Choose a tag or enter a new tag.";
    return;
  }

  if (newTagName && !newTagType) {
    tagMessage.textContent = "Enter a type for the new tag.";
    return;
  }

  if (currentTags.some((tag) => tag.id === tagId)) {
    tagMessage.textContent = "That tag is already on this recipe.";
    return;
  }

  tagMessage.textContent = "Saving tag...";

  try {
    if (newTagName) {
      const createResponse = await fetch("/api/tags", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: newTagName,
          type: newTagType,
        }),
      });

      const createdTag = await createResponse.json();

      if (!createResponse.ok) {
        throw new Error(createdTag.error || "Unable to create the tag.");
      }

      tagId = createdTag.id;
    }

    const attachResponse = await fetch(`/api/recipes/${recipeId}/tags`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ tag_id: tagId }),
    });

    const attachedTag = await attachResponse.json();

    if (!attachResponse.ok) {
      throw new Error(attachedTag.error || "Unable to attach the tag.");
    }

    tagForm.reset();
    await loadRecipeForEditing();
    await loadTagOptions();
    tagMessage.textContent = "Tag saved.";
  } catch (error) {
    tagMessage.textContent = error.message;
  }
});

loadRecipeForEditing();
loadIngredientOptions();
loadTagOptions();
