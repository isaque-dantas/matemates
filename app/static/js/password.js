const passwordEye = document.querySelector(".eye-open");
const passwordForm = document.querySelector("#password");
console.log("rodando");

passwordEye.addEventListener("click", function () {
  if (passwordEye.classList.contains("bi-eye-slash")) {
    passwordEye.classList.replace("bi-eye-slash", "bi-eye");
    passwordForm.type = "password";
  } else {
    passwordForm.type = "text";
    passwordEye.classList.replace("bi-eye", "bi-eye-slash");
  }
});
