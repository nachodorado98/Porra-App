document.querySelectorAll('.ver-puntos').forEach(boton => {

    boton.addEventListener('click', () => {

        const card = boton.closest('.ranking-card');

        card.classList.toggle('detalle-activo');

        boton.innerText = card.classList.contains('detalle-activo')
            ? 'Ocultar detalle'
            : 'Ver detalle';

    });

});