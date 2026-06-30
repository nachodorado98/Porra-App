document.addEventListener("DOMContentLoaded", function(){

    const nuevaContrasena = document.getElementById("nueva_contrasena");
    const repetirContrasena = document.getElementById("repetir_contrasena");
    const boton = document.getElementById("botonCambiarContrasena");

    if(!nuevaContrasena || !repetirContrasena || !boton){
        return;
    }

    function contrasenaCorrecta(contrasena){

        const patron = /^[^\s]{8,}$/;

        return patron.test(contrasena);

    }

    function validarFormulario(){

        const nueva = nuevaContrasena.value;
        const repetir = repetirContrasena.value;

        const camposRellenos =
            nueva !== "" &&
            repetir !== "";

        const nuevaValida = contrasenaCorrecta(nueva);

        const coinciden = nueva === repetir;

        boton.disabled = !(
            camposRellenos &&
            nuevaValida &&
            coinciden
        );

    }

    nuevaContrasena.addEventListener("input", validarFormulario);
    repetirContrasena.addEventListener("input", validarFormulario);

    validarFormulario();

});