const botonCalcularPuntuacion = document.getElementById("botonCalcularPuntuacion");

if(botonCalcularPuntuacion){

    botonCalcularPuntuacion.addEventListener("click", async () => {

        botonCalcularPuntuacion.disabled = true;
        botonCalcularPuntuacion.innerText = "Recalculando...";

        try{

            const response = await fetch("/puntuacion/calcular_puntuacion", {
                method: "PUT"
            });

            window.location.href = response.url;

        }catch(error){

            console.error(error);

            botonCalcularPuntuacion.disabled = false;
            botonCalcularPuntuacion.innerText = "Recalcular puntuación";

            window.location.href = "/settings";
        }

    });

}