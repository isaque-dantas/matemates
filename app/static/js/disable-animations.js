const animationsToggle = document.querySelector(".bi-columns-gap");
const closeButton = document.querySelector(".options-close");
const animationContainer = document.querySelector(".options-container");
const AnimationsSwitchToggler = document.querySelectorAll(".switch-animations");
const significado = document.querySelector(".significado");
const informacoes = document.querySelector(".informacoes");
const borderAnimations = [significado, informacoes];


// shows the animations optiosn when the button is clicked
animationsToggle.addEventListener("click", () => {
  animationContainer.style.right = "0%";
});

closeButton.addEventListener("click", () => {
  animationContainer.style.right = "-100%";
});

if (localStorage.getItem("disableBubles") === "true") {
  fundoBolhas.style.display = "none";
}

if (localStorage.getItem("noBorderAnimation") === "true") {
  borderAnimations.forEach((element) => {
    if (element !== null) {
      element.classList.add("animation-off");
    }
  });
}

// toggle animations when button is clicked
AnimationsSwitchToggler.forEach((button, index) => {
  // changes the button based on the index
  switch (index) {
    case 0:
      button.addEventListener("click", () => {
        if (fundoBolhas.style.display !== "none") {
          fundoBolhas.style.display = "none";
          localStorage.setItem("disableBubles", "true");
        } else {
          fundoBolhas.style.display = "flex";

          localStorage.removeItem("disableBubles");
        }
      });
      break;
    case 1:
      button.addEventListener("click", () => {
        borderAnimations.forEach((element) => {
          if (element !== null) {
            if (element.classList.contains("animation-off")) {
              localStorage.removeItem("noBorderAnimation");
            } else {
              localStorage.setItem("noBorderAnimation", "true");
            }
            element.classList.toggle("animation-off");
          }
        });
      });
      break;
  }
});
