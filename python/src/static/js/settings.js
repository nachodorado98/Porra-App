const modal =
    document.getElementById('modalEliminar')

const abrirModal =
    document.getElementById('abrirModalEliminar')

const cerrarModal =
    document.getElementById('cerrarModal')

const cancelarEliminar =
    document.getElementById('cancelarEliminar')

abrirModal.addEventListener('click', () => {

    modal.classList.add('active')

})

function cerrarVentanaModal(){

    modal.classList.remove('active')

}

cerrarModal.addEventListener('click', () => {

    cerrarVentanaModal()

})

cancelarEliminar.addEventListener('click', () => {

    cerrarVentanaModal()

})

window.addEventListener('click', (e) => {

    if(e.target === modal){

        cerrarVentanaModal()

    }

})

const confirmarEliminar =
    document.getElementById('confirmarEliminar')

confirmarEliminar.addEventListener('click', () => {

    mostrarLoading()

    confirmarEliminar.disabled = true

    confirmarEliminar.innerText = 'Eliminando cuenta...'

    window.location.href = '/settings/eliminar_cuenta'

})