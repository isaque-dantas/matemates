const imageInput = document.querySelector("#get-file");
const previewImage = document.querySelector(".preview-image");

// Listen for changes in the file input
imageInput.addEventListener("change", function (e) {
  const file = e.target.files[0];

  if (file) {
    // Create the FileReader object
    const reader = new FileReader();

    // Set up the onload event handler
    reader.onload = function (e) {
      // Set the source of the image element to the data URL
      previewImage.src = e.target.result;
    };

    // Read the contents of the file as a data URL
    reader.readAsDataURL(file);
  }
});
