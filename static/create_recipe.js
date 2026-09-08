const recipeForm = document.querySelector("#recipe-form");
const formMessage = document.querySelector("#form-message");

recipeForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  formMessage.textContent = "Saving recipe...";

  const formData = new FormData(recipeForm);

  const recipeData = {
    title: formData.get("title").trim(),
    description: formData.get("description").trim(),
    prep_time: Number(formData.get("prep_time")),
    cook_time: Number(formData.get("cook_time")),
    user_id: Number(formData.get("user_id")),
  };

  try {
    const response = await fetch("/api/recipes", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(recipeData),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Unable to save this recipe.");
    }

    window.location.href = `/recipes/${data.id}/edit`;
  } catch (error) {
    formMessage.textContent = error.message;
  }
});
