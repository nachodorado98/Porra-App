document.addEventListener("DOMContentLoaded", () => {

    // TODOS los formularios
    const forms = document.querySelectorAll("form");

    forms.forEach(form => {

        form.addEventListener("submit", () => {

            mostrarLoading();

            const botones = form.querySelectorAll(
                "button[type='submit'], input[type='submit']"
            );

            botones.forEach(boton => {

                boton.disabled = true;

                if (boton.tagName === "BUTTON") {
                    boton.innerText = "Cargando...";
                }

            });

        });

    });

});

function mostrarLoading() {

    const overlay =
        document.getElementById("loading-overlay");

    if (overlay) {
        overlay.classList.remove("hidden");
    }

}

function ocultarLoading() {

    const overlay =
        document.getElementById("loading-overlay");

    if (overlay) {
        overlay.classList.add("hidden");
    }

}

document.addEventListener("click", (e) => {

    const link = e.target.closest("[data-loading='true']");

    if (!link) return;

    mostrarLoading();

});