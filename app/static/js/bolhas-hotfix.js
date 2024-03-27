const fundoBolhas = document.querySelector(".fundo-bolhas");

window.onload = function () {
  for (i = 0; i < 140; i++) {
    let newSpan = document.createElement("span");
    newSpan.style = `--i: ${Math.random() * (30-5) + 5}`;
    fundoBolhas.appendChild(newSpan);
  }
};
