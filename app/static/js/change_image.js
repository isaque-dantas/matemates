// const imageInputs = document.querySelectorAll(".get-file");

// imageInputs.forEach((input) => {
//   input.addEventListener("change", function (e) {
//     const imageInputs = document.querySelectorAll(".get-file");
//     const file = e.target.files[0];
//     const previewId = input.id.replace("get-file-", "");
//     const previewImage = document.getElementById("preview-image-" + previewId);

//     if (file && previewImage) {
//       const reader = new FileReader();

//       reader.onload = function (e) {
//         const image = e.target.result;
//         const imageMatch = image.match(/^data:image\/.*/);

//         if (imageMatch) {
//           previewImage.src = e.target.result;
//           previewImage.style.padding = 0;
//         } else {
//           alert("Escolha apenas imagens");
//         }
//       };

//       reader.readAsDataURL(file);
//     }
//   });
// });
