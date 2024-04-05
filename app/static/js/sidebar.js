const body = document.querySelector("body");
const sidebar = document.querySelector(".sidebar");
const modeSwitch = document.querySelector(".toggle-switch");
const modeText = document.querySelector(".mode-text");
const moonIcon = document.querySelector(".bi-moon");
const sunIcon = document.querySelector(".bi-sun");
const generalNav = document.querySelector(".div-geral-nav");
const navLinks = document.querySelectorAll(".nav-links");

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

generalNav.addEventListener("mouseover", () => {
  setTimeout(function () {
    sidebar.classList.remove("close");
  }, 350);
});

navLinks.forEach((element) => {
  element.addEventListener("mouseover", () => {
    setTimeout(function () {
      sidebar.classList.remove("close");
    }, 300);
  });
});

generalNav.addEventListener("mouseout", () => {
  setTimeout(function () {
    sidebar.classList.add("close");
  }, 200);
});