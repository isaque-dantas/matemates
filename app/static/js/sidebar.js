const body = document.querySelector("body");
const sidebar = document.querySelector(".sidebar");
const modeSwitch = document.querySelector(".toggle-switch");
const modeText = document.querySelector(".mode-text");
const moonIcon = document.querySelector(".bi-moon");
const sunIcon = document.querySelector(".bi-sun");
const generalNav = document.querySelector(".div-geral-nav");
const navLinks = document.querySelectorAll(".nav-links");
const hamburguerMenu = document.querySelector(".bi-list");

if (localStorage.getItem("responsiveOpened" === "true")) {
  sidebar.style.left = "0";
}

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

function removeClose() {
  sidebar.classList.remove("close");
}

function addClose() {
  sidebar.classList.add("close");
}

function OpenCloseSidebar() {
  generalNav.addEventListener("mouseover", removeClose);

  generalNav.addEventListener("mouseout", addClose);
}

hamburguerMenu.addEventListener("click", () => {
  if ((sidebar.style.left === "-100%")) {
    sidebar.style.left = "0";
    localStorage.setItem("responsiveOpened", "true");
  } else {
    sidebar.style.left = "-100%";
    localStorage.removeItem("responsiveOpened");
  }
});
