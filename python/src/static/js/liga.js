const btnCrear = document.getElementById("btn-crear-liga");
const btnUnirse = document.getElementById("btn-unirse-liga");

const contenedorCodigo = document.getElementById("contenedor-codigo");
const contenedorCodigoGenerado = document.getElementById("contenedor-codigo-generado");

const codigoMostrado = document.getElementById("codigo_mostrado");

const inputAccion = document.getElementById("accion_liga");
const inputCodigoFinal = document.getElementById("codigo_final");
const inputCodigo = document.getElementById("codigo_liga");

const form = document.getElementById("formulario");

btnCrear.addEventListener("click", async () => {

    const respuesta = await fetch("/registro/generar_codigo");
    const data = await respuesta.json();

    if (data.codigo) {

        inputAccion.value = "crear";
        inputCodigoFinal.value = data.codigo;

        codigoMostrado.textContent = data.codigo;

        contenedorCodigoGenerado.style.display = "block";
        contenedorCodigo.style.display = "none";

        form.dispatchEvent(new Event("input"));
    }
});

btnUnirse.addEventListener("click", () => {

    inputAccion.value = "unirse";

    inputCodigoFinal.value = "";
    inputCodigo.value = "";
    inputCodigo.style.border = "";

    contenedorCodigo.style.display = "block";
    contenedorCodigoGenerado.style.display = "none";

    form.dispatchEvent(new Event("input"));

    inputCodigo.focus();
});

inputCodigo.addEventListener("input", async () => {

    inputCodigoFinal.value = inputCodigo.value.toUpperCase();

    if (inputCodigo.value.length === 6) {

        const respuesta = await fetch(`/registro/verificar_codigo/${inputCodigoFinal.value}`);
        const data = await respuesta.json();

        if (data.valido) {
            inputCodigo.style.border = "2px solid green";
        } else {
            inputCodigo.style.border = "2px solid red";
        }

    } else {
        inputCodigo.style.border = "";
    }

    form.dispatchEvent(new Event("input"));
});