const animationsToggle = document.querySelector(".bi-columns-gap");
const animationsToggleDiv = document.querySelector(".animations-div");
const closeButton = document.querySelector(".options-close");
const animationContainer = document.querySelector(".options-container");
const AnimationsSwitchToggler = document.querySelectorAll(".switch-animations");
const borderAnimations = Object.values(document.querySelectorAll(".animated"));
const blueAnimation = Object.values(
  document.querySelectorAll(".animacao-azul")
);
const grandBlueAnimation = document.querySelector(".animacao-azul-superior");
const animationsTogglers = [animationsToggle, animationsToggleDiv];

AnimationsSwitchToggler.forEach((button) => {
  if (localStorage.getItem(button.id) === "true") {
    button.classList.add("animation-off");
  }
});

if (localStorage.getItem("grandBlueIsOff") === "true") {
  grandBlueAnimation.classList.add("animation-off");
}

if (localStorage.getItem("sidebarAnimationOff") === "true") {
  OpenCloseSidebar();
}

if (localStorage.getItem("blueIsOff") === "true") {
  blueAnimation.forEach((element) => {
    element.classList.add("animation-off");
  });
}

if (localStorage.getItem("opennedMenu") === "true") {
  animationContainer.style.right = "0%";
}

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

// shows the animations optiosn when the button is clicked
animationsTogglers.forEach((element) => {
  element.addEventListener("click", () => {
    animationContainer.style.right = "0%";
    localStorage.setItem("opennedMenu", "true");
  });
});

closeButton.addEventListener("click", () => {
  animationContainer.style.right = "-100%";
  localStorage.removeItem("opennedMenu");
});

// toggle animations when button is clicked
AnimationsSwitchToggler.forEach((button, index) => {
  // changes the button based on the index
  switch (index) {
    // active and deactive the buble animations in the background
    case 0:
      button.addEventListener("click", () => {
        if (fundoBolhas.style.display !== "none") {
          fundoBolhas.style.display = "none";
          localStorage.setItem("disableBubles", "true");
        } else {
          fundoBolhas.style.display = "flex";
          localStorage.removeItem("disableBubles");
        }
        toggleButton(button);
      });
      break;

    // activate and deactivate the looping border animations
    case 1:
      // since some pages does not have this animation, it's necessary to verify if the borderAnimations array is all null
      if (borderAnimations.some((element) => element !== null)) {
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
            toggleButton(button);
          });
        });
      } else {
        // removes the li from the menu if there is no animation of this type in the page
        button.parentNode.parentNode.remove();
      }
      break;

    // toggles the blue border animation
    case 2:
      if (
        blueAnimation.some((element) => element !== null) &&
        grandBlueAnimation === null
      ) {
        button.addEventListener("click", () => {
          blueAnimation.forEach((element) => {
            if (element.classList.contains("animation-off")) {
              localStorage.removeItem("blueIsOff");
            } else {
              localStorage.setItem("blueIsOff", "true");
            }
            element.classList.toggle("animation-off");
          });
          toggleButton(button);
        });
      } else {
        // removes the li from the menu if there is no animation of this type in the page
        button.parentNode.parentNode.remove();
      }
      break;
    case 3:
      if (grandBlueAnimation !== null) {
        button.addEventListener("click", () => {
          if (grandBlueAnimation.classList.contains("animation-off")) {
          } else {
            localStorage.setItem("grandBlueIsOff", "true");
          }
          grandBlueAnimation.classList.toggle("animation-off");
          toggleButton(button);
        });
      } else {
        // removes the li from the menu if there is no animation of this type in the page
        button.parentNode.parentNode.remove();
      }
      break;
    case 4:
      button.addEventListener("click", () => {
        ToggleSideBar();
        sidebar.classList.toggle("animation-off");
        toggleButton(button);
      });
  }
});

function toggleButton(button) {
  button.classList.toggle("animation-off");
  var buttonId = button.id;
  var isOff = button.classList.contains("animation-off");
  localStorage.setItem(buttonId, isOff);
}

function ToggleSideBar() {
  if (sidebar.classList.contains("animation-off")) {
    OpenCloseSidebar();
    console.log("evento adicionado");
    localStorage.setItem("sidebarAnimationOff", "true");
  } else {
    localStorage.removeItem("sidebarAnimationOff");
    generalNav.removeEventListener("mouseover", removeClose);
    generalNav.removeEventListener("mouseout", addClose);
    console.log("evento removido");
  }
}

console.log(localStorage.getItem("sidebarAnimationOff"));
