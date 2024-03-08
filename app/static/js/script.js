function mostrarExemplos() {
    var significado = document.getElementById('significado');
    var exemplo = document.getElementById('exemplo');
    var btnExemplo = document.getElementById('btn-ex');
    var btnSignificado = document.getElementById('btn-sig');
    if (significado.classList.contains('d-flex')) {
        significado.classList.replace('d-flex', 'd-none');
        exemplo.classList.replace('d-none', 'd-flex');
        btnExemplo.classList.replace('d-block', 'd-none');
        btnSignificado.classList.replace('d-none', 'd-block');
    }
}

function mostrarSignificado() {
    var significado = document.getElementById('significado');
    var exemplo = document.getElementById('exemplo');
    var btnExemplo = document.getElementById('btn-ex');
    var btnSignificado = document.getElementById('btn-sig');
    if (significado.classList.contains('d-none')) {
        significado.classList.replace('d-none', 'd-flex');
        exemplo.classList.replace('d-flex', 'd-none');
        btnExemplo.classList.replace('d-none', 'd-block');
        btnSignificado.classList.replace('d-block', 'd-none');
    }
}