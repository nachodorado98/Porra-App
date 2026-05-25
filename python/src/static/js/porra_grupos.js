const listas = document.querySelectorAll('.grupo-lista')

const btnGuardar = document.getElementById('btnGuardar')

listas.forEach(lista => {

    new Sortable(lista, {

        animation: 150,

        onEnd: () => {

            actualizarPosiciones()

            comprobarFormulario()

        }

    })

})

function actualizarPosiciones(){

    listas.forEach(lista => {

        const equipos = lista.querySelectorAll('.equipo-card')

        equipos.forEach((equipo, index) => {

            equipo.querySelector('.posicion').innerText = index + 1

        })

    })

}

function comprobarFormulario(){

    let completo = true

    listas.forEach(lista => {

        const equipos = lista.querySelectorAll('.equipo-card')

        if(equipos.length !== 4){
            completo = false
        }

    })

    if(completo){

        btnGuardar.disabled = false

        btnGuardar.classList.add('enabled')

    }

}