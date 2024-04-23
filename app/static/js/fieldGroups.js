const significado = document.querySelector("#significado");
const exemplos = document.querySelector("#exemplo");
const representacao = document.querySelector("#representa");
const nFieldGroupsContainers = [representacao, exemplos, significado];

function addFieldGroup(container) {
  const newFieldGroup = container.querySelector(".field-group").cloneNode(true);
  container.querySelector(".field-groups").appendChild(newFieldGroup);
  removeFieldGroupBtn(container);
}

function insertFieldGroupBtn(container) {
  container.addEventListener("click", (event) => {
    if (event.target.classList.contains("btn-add-field-group")) {
      addFieldGroup(container);
    }
  });
}

function removeFieldGroup(button, container) {
  const fieldGroup = button.closest(".field-group");
  if (fieldGroup) {
    fieldGroup.remove();
  }
  removeFieldGroupBtn(container);
}

function removeFieldGroupBtn(container) {
  const removeFieldGroupBtns = container.querySelectorAll(
    ".btn-remove-field-group"
  );

  if (container.id === "representa") {
    if (removeFieldGroupBtns.length > 2) {
      removeFieldGroupBtns.forEach((button) => {
        button.disabled = false;
        button.addEventListener("click", () => {
          removeFieldGroup(button, container);
        });
      });
    } else {
      removeFieldGroupBtns.forEach((button) => {
        button.disabled = true;
      });
    }
  } else {
    if (removeFieldGroupBtns.length > 1) {
      removeFieldGroupBtns.forEach((button) => {
        button.disabled = false;
        button.addEventListener("click", () => {
          removeFieldGroup(button, container);
        });
      });
    } else {
      removeFieldGroupBtns.forEach((button) => {
        button.disabled = true;
      });
    }
  }
}

nFieldGroupsContainers.forEach((container) => {
  insertFieldGroupBtn(container);
  removeFieldGroupBtn(container);
  console.log(container.id);
});
