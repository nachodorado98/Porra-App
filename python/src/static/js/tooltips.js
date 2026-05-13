document.addEventListener("DOMContentLoaded", function () {
    const inputs = [
        {input: "correo", tooltip: "tooltipCorreo"},
        {input: "contrasena", tooltip: "tooltipContrasena"},
        {input: "fecha-nacimiento", tooltip: "tooltipFecha"}
    ];

    inputs.forEach(({input, tooltip}) => {
        const campo = document.getElementById(input);
        const tip = document.getElementById(tooltip);

        campo.addEventListener("focus", () => {
            const rect = campo.getBoundingClientRect();
            tip.style.top = `${rect.top + window.scrollY - tip.offsetHeight - 8}px`;
            tip.style.left = `${rect.left + window.scrollX}px`;
            tip.classList.add("visible");

            setTimeout(() => {
                tip.classList.remove("visible");
            }, 3000);
        });
    });
});