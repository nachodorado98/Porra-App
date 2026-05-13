document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("formulario");
    const boton = document.getElementById("btn-submit");

    const accionLiga = document.getElementById("accion_liga");
    const codigoFinal = document.getElementById("codigo_final");

    function validarFormularioCompleto() {

        const formularioValido = form.checkValidity();

        let ligaValida = false;

        if (accionLiga.value === "crear") {
            ligaValida = codigoFinal.value.length === 6;

        } else if (accionLiga.value === "unirse") {
            ligaValida = codigoFinal.value.length === 6;

        } else {
            ligaValida = false;
        }

        boton.disabled = !(formularioValido && ligaValida);
    }

    form.addEventListener("input", validarFormularioCompleto);

    validarFormularioCompleto();
});