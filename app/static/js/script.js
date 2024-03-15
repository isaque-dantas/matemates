function mostrarDefinicao(button) {
    removerSelecaoDeBotoes();
    button.classList.add('selecionado');
    var significado = document.getElementById('significado');
    var exemplo = document.getElementById('exemplo');
    var representa = document.getElementById('representa');
    var btnExemplo = document.getElementById('btn-ex');
    var btnSignificado = document.getElementById('btn-sig');
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
    var significado = document.getElementById('significado');
    var exemplo = document.getElementById('exemplo');
    var representa = document.getElementById('representa');
    var btnExemplo = document.getElementById('btn-ex');
    var btnSignificado = document.getElementById('btn-sig');
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
    var significado = document.getElementById('significado');
    var exemplo = document.getElementById('exemplo');
    var representa = document.getElementById('representa');
    if (representa.classList.contains('d-none')) {
        significado.classList.replace('d-flex', 'd-none');
        exemplo.classList.replace('d-flex', 'd-none');
        representa.classList.replace('d-none', 'd-flex');
    }
}

function removerSelecaoDeBotoes() {
    var botoes = document.querySelectorAll('.btn-exemplo-definicao');
    botoes.forEach(function (botao) {
        botao.classList.remove('selecionado');
    });
}

function toggleGeneroVisibility() {
    var selectClasse = document.getElementById('select-classe');
    var genero = document.getElementById('genero');

    selectClasse.addEventListener('change', function() {
        var selectedOption = this.value;
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



