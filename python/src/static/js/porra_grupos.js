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

            equipo.classList.remove(
                'clasificado',
                'tercero',
                'eliminado'
            )

            if(index === 0 || index === 1){

                equipo.classList.add('clasificado')

            }
            else if(index === 2){

                equipo.classList.add('tercero')

            }
            else{

                equipo.classList.add('eliminado')

            }

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

actualizarPosiciones()

const modal = document.getElementById('modalResumen')

const resumenContenido =
    document.getElementById('resumenContenido')

const cancelarModal =
    document.getElementById('cancelarModal')

const confirmarModal =
    document.getElementById('confirmarModal')

btnGuardar.addEventListener('click', () => {

    generarResumen()

    modal.classList.add('active')

})

cancelarModal.addEventListener('click', () => {

    modal.classList.remove('active')

})

function generarResumen(){

    resumenContenido.innerHTML = ''

    listas.forEach(lista => {

        const grupo = lista.dataset.grupo

        const equipos =
            lista.querySelectorAll('.equipo-card')

        let html = `
            <div class="resumen-grupo">

                <div class="resumen-grupo-header">
                    Grupo ${grupo}
                </div>

                <div class="resumen-lista">
        `

        equipos.forEach((equipo, index) => {

            const nombre =
                equipo.querySelector('.nombre-equipo')
                    .innerText

            const bandera =
                equipo.querySelector('.bandera-img')
                    .src

            const escudo =
                equipo.querySelector('.escudo-img')
                    .src

            let clase = ''

            if(index === 0 || index === 1){
                clase = 'clasificado'
            }
            else if(index === 2){
                clase = 'tercero'
            }
            else{
                clase = 'eliminado'
            }

            html += `
                <div class="resumen-equipo-card ${clase}">

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

        html += `
                </div>
            </div>
        `

        resumenContenido.innerHTML += html

    })

}