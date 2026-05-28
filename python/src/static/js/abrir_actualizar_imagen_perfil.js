const botonActualizar =
    document.getElementById(
        'botonActualizarImagenPerfil'
    )

if(botonActualizar){

    botonActualizar.addEventListener('click', () => {

        const contenedor =
            document.getElementById(
                'contenedorActualizarImagenPerfil'
            )

        const visible =
            contenedor.style.display === 'block'

        contenedor.style.display =
            visible ? 'none' : 'block'

        if(!visible){

            contenedor.scrollIntoView({
                behavior:'smooth',
                block:'start'
            })

        }

    })

}