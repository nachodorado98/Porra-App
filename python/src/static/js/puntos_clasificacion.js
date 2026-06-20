document.querySelectorAll('.ver-puntos').forEach(boton => {

    boton.addEventListener('click', () => {

        const card = boton.closest('.ranking-card');

        card.classList.toggle('detalle-activo');

        boton.innerText = card.classList.contains('detalle-activo')
            ? 'Ocultar detalle'
            : 'Ver detalle';

    });

});

document.addEventListener("DOMContentLoaded", function () {
    const botonCargarMas = document.getElementById("cargar-mas-ranking");

    if (!botonCargarMas) return;

    botonCargarMas.addEventListener("click", function () {
        const ocultos = document.querySelectorAll(".ranking-card.ranking-oculto");

        for (let i = 0; i < 40 && i < ocultos.length; i++) {
            ocultos[i].classList.remove("ranking-oculto");
        }

        const quedanOcultos = document.querySelectorAll(".ranking-card.ranking-oculto");

        if (quedanOcultos.length === 0) {
            botonCargarMas.style.display = "none";
        }
    });
});