const nFieldGroupsContainers = document.querySelectorAll(".has-n-field-groups");

function imageHandle() {
  imageInputs.forEach((input) => {
    input.addEventListener("change", function (e) {
      const imageInputs = document.querySelectorAll(".get-file");
      const file = e.target.files[0];
      const previewId = input.id.replace("get-file-", "");
      const previewImage = document.getElementById(
        "preview-image-" + previewId
      );
      console.log("input:", input);

      if (file && previewImage) {
        const reader = new FileReader();

        reader.onload = function (e) {
          const image = e.target.result;
          const imageMatch = image.match(/^data:image\/.*/);

          if (imageMatch) {
            previewImage.src = e.target.result;
            previewImage.style.padding = 0;
          } else {
            alert("Escolha apenas imagens");
          }
        };

        reader.readAsDataURL(file);
      }
    });
  });
}

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

  fieldGroups.appendChild(newFieldGroup);
  imageInputs = document.querySelectorAll(".get-file");
  updateLabelForAttribute(container);
  imageHandle();
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
    updateLabelForAttribute(container);
  }
}

function updateLabelForAttribute(container) {
  const fieldGroups = container.querySelectorAll(".field-group");
  fieldGroups.forEach((fieldGroup, index) => {
    const imageLabel = fieldGroup.querySelector(".criacao-imagem");
    imageLabel.htmlFor = "get-file-" + (index + 1);
  });
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
