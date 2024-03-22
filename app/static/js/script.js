function mostrarDefinicao(button) {
    removerSelecaoDeBotoes();
    button.classList.add('selecionado');
    const significado = document.getElementById('significado');
    const exemplo = document.getElementById('exemplo');
    const representa = document.getElementById('representa');
    const btnExemplo = document.getElementById('btn-ex');
    const btnSignificado = document.getElementById('btn-sig');
    if (significado.classList.contains('d-none')) {
        significado.classList.replace('d-none', 'd-flex');
        exemplo.classList.replace('d-flex', 'd-none');
        representa.classList.replace('d-flex', 'd-none');
        btnExemplo.classList.replace('d-none', 'd-block');
        btnSignificado.classList.replace('d-block', 'd-none');
    }
}

function mostrarExemplos(button) {
    removerSelecaoDeBotoes();
    button.classList.add('selecionado');
    const significado = document.getElementById('significado');
    const exemplo = document.getElementById('exemplo');
    const representa = document.getElementById('representa');
    const btnExemplo = document.getElementById('btn-ex');
    const btnSignificado = document.getElementById('btn-sig');
    if (exemplo.classList.contains('d-none')) {
        significado.classList.replace('d-flex', 'd-none');
        exemplo.classList.replace('d-none', 'd-flex');
        representa.classList.replace('d-flex', 'd-none');
        btnExemplo.classList.replace('d-block', 'd-none');
        btnSignificado.classList.replace('d-none', 'd-block');
    }
}

function mostrarRepresentacao(button) {
    removerSelecaoDeBotoes();
    button.classList.add('selecionado');
    const significado = document.getElementById('significado');
    const exemplo = document.getElementById('exemplo');
    const representa = document.getElementById('representa');
    if (representa.classList.contains('d-none')) {
        significado.classList.replace('d-flex', 'd-none');
        exemplo.classList.replace('d-flex', 'd-none');
        representa.classList.replace('d-none', 'd-flex');
    }
}

function removerSelecaoDeBotoes() {
    const botoes = document.querySelectorAll('.btn-exemplo-definicao');
    botoes.forEach(function (botao) {
        botao.classList.remove('selecionado');
    });
}

function toggleGeneroVisibility() {
    const selectClasse = document.getElementById('select-classe');
    const genero = document.getElementById('genero');

    selectClasse.addEventListener('change', function() {
        const selectedOption = this.value;
        if (selectedOption === 'Numeral' || selectedOption === 'Verbo') {
            genero.classList.replace('d-block', 'd-none');
        } 
        else {
            genero.classList.replace('d-none', 'd-block');
        }
    });
}

// Chamada da função ao carregar a página
document.addEventListener("DOMContentLoaded", function() {
    toggleGeneroVisibility();
});



