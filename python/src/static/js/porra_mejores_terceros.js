const cards = document.querySelectorAll('.tercero-card')

const contador = document.getElementById(
    'contadorSeleccionados'
)

const btnContinuar = document.getElementById(
    'btnContinuar'
)

const modal = document.getElementById('modalResumen')

const resumenContenido = document.getElementById(
    'resumenContenido'
)

const cancelarModal = document.getElementById(
    'cancelarModal'
)

const confirmarModal = document.getElementById(
    'confirmarModal'
)

let seleccionados = []

cards.forEach(card => {

    card.addEventListener('click', () => {

        const equipo = card.dataset.equipo

        const grupo = card.dataset.grupo

        if(card.classList.contains('selected')){

            card.classList.remove('selected')

            seleccionados = seleccionados.filter(
                item => item.equipo_id !== equipo
            )

        }
        else{

            if(seleccionados.length >= 8){
                return
            }

            card.classList.add('selected')

            seleccionados.push({
                equipo_id: equipo,
                grupo: grupo
            })

        }

        actualizarEstado()

    })

})

function actualizarEstado(){

    contador.innerText = seleccionados.length

    if(seleccionados.length === 8){

        btnContinuar.disabled = false

        btnContinuar.classList.add('enabled')

        cards.forEach(card => {

            if(!card.classList.contains('selected')){
                card.classList.add('disabled')
            }

        })

    }
    else{

        btnContinuar.disabled = true

        btnContinuar.classList.remove('enabled')

        cards.forEach(card => {
            card.classList.remove('disabled')
        })

    }

}

btnContinuar.addEventListener('click', () => {

    generarResumen()

    modal.classList.add('active')

})

cancelarModal.addEventListener('click', () => {

    modal.classList.remove('active')

})

function generarResumen(){

    resumenContenido.innerHTML = ''

    seleccionados.forEach((equipo, index) => {

        const card = document.querySelector(
            `[data-equipo="${equipo.equipo_id}"]`
        )

        const nombre = card.querySelector(
            '.nombre-equipo'
        ).innerText

        const escudo = card.querySelector(
            '.escudo-img'
        ).src

        const bandera = card.querySelector(
            '.bandera-img'
        ).src

        resumenContenido.innerHTML += `
            <div class="resumen-equipo-card">

                <div class="resumen-posicion">
                    ${index + 1}
                </div>

                <div class="resumen-equipo-info">

                    <img class="resumen-escudo"
                         src="${escudo}">

                    <img class="resumen-bandera"
                         src="${bandera}">

                    <span>
                        ${nombre}
                    </span>

                </div>

            </div>
        `

    })

}

confirmarModal.addEventListener('click', async () => {

    try{

        const response = await fetch(
            '/porra/mejores_terceros/guardar',
            {
                method:'POST',

                headers:{
                    'Content-Type':'application/json'
                },

                body:JSON.stringify({
                    equipos: seleccionados
                })
            }
        )

        window.location.href = response.url

    }
    catch(error){

        console.error(error)

        window.location.href = '/porra'

    }

})