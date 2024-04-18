const significado = document.querySelector("#significado");
const exemplos = document.querySelector("#exemplo");
const representacao = document.querySelector("#representa");
const nFieldGroupsContainers = [representacao, exemplos, significado];

function addFieldGroup(container) {
  const newFieldGroup = container.querySelector(".field-group").cloneNode(true);
  container.appendChild(newFieldGroup);

  const addFieldGroupBtns = container.querySelectorAll(".btn-add-field-group");
  addFieldGroupBtns.forEach((button) => {
    button.removeEventListener("click", addFieldGroup);
  });

  addFieldGroupBtns.forEach((button) => {
    button.addEventListener("click", () => {
      addFieldGroup(container);
    });
  });

  removeFieldGroupBtn(container); // Update remove button listeners
}

function insertFieldGroupBtn(container) {
  const addFieldGroupBtns = container.querySelectorAll(".btn-add-field-group");

  addFieldGroupBtns.forEach((button) => {
    button.addEventListener("click", () => {
      addFieldGroup(container);
    });
  });
}

function removeFieldGroup(button) {
  button.parentNode.parentNode.parentNode.remove();
}

function removeFieldGroupBtn(container) {
  const removeFieldGroupBtns = container.querySelectorAll(
    ".btn-remove-field-group"
  );

  if (removeFieldGroupBtns.length > 1) {
    removeFieldGroupBtns.forEach((button) => {
      button.disabled = false;
      button.addEventListener("click", () => {
        removeFieldGroup(button);
      });
    });
  } else if (removeFieldGroupBtns.length === 1) {
    removeFieldGroupBtns[0].disabled = true;
  }
}

nFieldGroupsContainers.forEach((container) => {
  insertFieldGroupBtn(container);
});
