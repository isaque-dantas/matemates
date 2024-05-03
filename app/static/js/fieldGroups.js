const nFieldGroupsContainers = document.querySelectorAll(".has-n-field-groups");

function addFieldGroup(container) {
  const fieldGroups = container.querySelector(".field-groups");
  const newFieldGroup = fieldGroups
    .querySelector(".field-group")
    .cloneNode(true);

  newFieldGroup.querySelectorAll("input, textarea").forEach((input) => {
    input.value = "";
  });

  const imageSelect = newFieldGroup.querySelector(".preview-image");
  imageSelect.src = "../static/img/selecionar-imagem.png";
  imageSelect.style.padding = "20px";

  const previewId = imageSelect.id.replace("preview-image-", "");
  const inputLabel = newFieldGroup.querySelector(".criacao-imagem");
  console.log(previewId)
  inputLabel.htmlFor = "get-file-" + previewId;


  fieldGroups.appendChild(newFieldGroup);
  removeFieldGroupBtn(container);
  sortFieldGroupsIndexes();
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
    removeFieldGroupBtn(container);
    sortFieldGroupsIndexes();
  }
}

function removeFieldGroupBtn(container) {
  const removeFieldGroupBtns = container.querySelectorAll(
    ".btn-remove-field-group"
  );
  const minRemoveButtons = container.id === "representa" ? 3 : 1;

  removeFieldGroupBtns.forEach((button) => {
    button.disabled = removeFieldGroupBtns.length <= minRemoveButtons;
    button.addEventListener("click", () => {
      removeFieldGroup(button, container);
    });
  });
}

function sortFieldGroupsIndexes() {
  nFieldGroupsContainers.forEach((container) => {
    const fieldsGroups = container.querySelectorAll(".field-group");
    let index = 1;
    fieldsGroups.forEach((fieldGroup) => {
      updateFieldGroupIndex(fieldGroup, index++);
    });
  });
}

function updateFieldGroupIndex(fieldGroup, newIndex) {
  updateIDIndex(fieldGroup, newIndex);

  const inputs = fieldGroup.querySelectorAll("input, select, textaream, img");
  inputs.forEach((input) => {
    updateIDIndex(input, newIndex);
    updateNameIndex(input, newIndex);
  });
}

function updateIDIndex(element, newIndex) {
  element.id = getDescriptionFromProperty(element.id) + newIndex.toString();
}

function updateNameIndex(element, newIndex) {
  element.name = getDescriptionFromProperty(element.name) + newIndex.toString();
}

function getDescriptionFromProperty(property) {
  const propertyMatch = property.match(/^[a-zA-z\-_]+/);
  return propertyMatch ? propertyMatch[0] : "";
}

nFieldGroupsContainers.forEach((container) => {
  insertFieldGroupBtn(container);
  removeFieldGroupBtn(container);
});
