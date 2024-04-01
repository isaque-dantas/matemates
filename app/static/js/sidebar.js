const body = document.querySelector("body");
const sidebar = document.querySelector(".sidebar");
const toggle = document.querySelector(".toggle");
const modeSwitch = document.querySelector(".toggle-switch");
const modeText = document.querySelector(".mode-text");
const moonIcon = document.querySelector(".bi-moon");
const sunIcon = document.querySelector(".bi-sun");

// close sidebar
toggle.addEventListener("click", () => {
  sidebar.classList.toggle("close");
});

// change theme when the button is clicked
modeSwitch.addEventListener("click", () => {
  body.classList.toggle("light");

  if (body.classList.contains("light")) {
    modeText.innerText = "Dark mode";
    sunIcon.classList.toggle("d-none");
    moonIcon.classList.toggle("d-flex");
  } else {
    modeText.innerText = "Light mode";
    moonIcon.classList.toggle("d-flex");
    sunIcon.classList.toggle("d-none");
  }
});

