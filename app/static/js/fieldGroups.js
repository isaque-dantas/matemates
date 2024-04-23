const nFieldGroupsContainers = document.querySelectorAll(".has-n-field-groups");

function addFieldGroup(container) {
  const fieldGroups = container.querySelector(".field-groups");
  const newFieldGroup = fieldGroups
    .querySelector(".field-group")
    .cloneNode(true);
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
  const fieldsQueries = ["input", "select"];
  fieldsQueries.forEach((fieldQuery) => {
    const field = fieldGroup.querySelector(fieldQuery);
    if (field) {
      updateIDIndex(field, newIndex);
      updateNameIndex(field, newIndex);
    }
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
