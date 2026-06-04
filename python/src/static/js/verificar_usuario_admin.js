const inputUsuarioObjetivo = document.getElementById("usuario_objetivo");
const mensajeUsuarioObjetivo = document.getElementById("mensaje_usuario_objetivo");
const botonAdminContrasena = document.getElementById("botonAdminContrasena");

let usuarioValido = false;

inputUsuarioObjetivo.addEventListener("input", async () => {

    const usuario = inputUsuarioObjetivo.value.trim();

    usuarioValido = false;
    botonAdminContrasena.disabled = true;

    if (usuario.length === 0) {
        inputUsuarioObjetivo.style.border = "";
        mensajeUsuarioObjetivo.textContent = "";
        return;
    }

    try {

        const respuesta = await fetch(`/settings/verificar_usuario/${usuario}`);
        const data = await respuesta.json();

        if (data.valido) {

            usuarioValido = true;

            inputUsuarioObjetivo.style.border = "2px solid green";
            mensajeUsuarioObjetivo.textContent = "Usuario encontrado";
            mensajeUsuarioObjetivo.style.color = "green";

            botonAdminContrasena.disabled = false;

        } else {

            inputUsuarioObjetivo.style.border = "2px solid red";
            mensajeUsuarioObjetivo.textContent = "Usuario no existe";
            mensajeUsuarioObjetivo.style.color = "red";

        }

    } catch (error) {

        inputUsuarioObjetivo.style.border = "2px solid red";
        mensajeUsuarioObjetivo.textContent = "Error al verificar usuario";
        mensajeUsuarioObjetivo.style.color = "red";

    }

});