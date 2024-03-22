const btnExemplos = document.querySelectorAll(".btn-exemplo-definicao");
const definition = document.querySelector("#significado");
const question = document.querySelector("#exemplo");

function showQuestion() {
  //  hide definition
  definition.classList.replace("d-flex", "d-none");

  // show exemple
  question.classList.replace("d-none", "d-flex");

  // hide see exemple button
  btnExemplos[0].classList.replace("d-block", "d-none");
  btnExemplos[1].classList.replace("d-none", "d-block");
}

function showDefinition() {
  // show definition
  definition.classList.replace("d-none", "d-flex");

  // show exemple
  question.classList.replace("d-flex", "d-none");

  // hide go back to definition button
  btnExemplos[0].classList.replace("d-none", "d-block");
  btnExemplos[1].classList.replace("d-block", "d-none");
}

btnExemplos[0].addEventListener('click', showQuestion)

btnExemplos[1].addEventListener("click", showDefinition)
