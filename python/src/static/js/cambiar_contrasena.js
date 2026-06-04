document.addEventListener("DOMContentLoaded", function(){

    const contrasenaActual = document.getElementById("contrasena_actual");
    const nuevaContrasena = document.getElementById("nueva_contrasena");
    const repetirContrasena = document.getElementById("repetir_contrasena");
    const boton = document.getElementById("botonCambiarContrasena");

    if(!contrasenaActual || !nuevaContrasena || !repetirContrasena || !boton){
        return;
    }

    function contrasenaCorrecta(contrasena){

        const patron = /^[^\s]{8,}$/;

        return patron.test(contrasena);

    }

    function validarFormulario(){

        const actual = contrasenaActual.value;
        const nueva = nuevaContrasena.value;
        const repetir = repetirContrasena.value;

        const camposRellenos =
            actual !== "" &&
            nueva !== "" &&
            repetir !== "";

        const nuevaValida = contrasenaCorrecta(nueva);

        const distintaActual = nueva !== actual;

        const coinciden = nueva === repetir;

        boton.disabled = !(
            camposRellenos &&
            nuevaValida &&
            distintaActual &&
            coinciden
        );

    }

    contrasenaActual.addEventListener("input", validarFormulario);
    nuevaContrasena.addEventListener("input", validarFormulario);
    repetirContrasena.addEventListener("input", validarFormulario);

    validarFormulario();

});