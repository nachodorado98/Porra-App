function configurarPreviewImagen(
    inputId,
    previewId,
    mensajeId
){

    const input =
        document.getElementById(inputId)

    if(!input) return

    const preview =
        document.getElementById(previewId)

    const mensaje =
        document.getElementById(mensajeId)

    input.addEventListener('change', () => {

        const file = input.files[0]

        if(file){

            const fileType =
                file.type.toLowerCase()

            if(
                fileType === 'image/jpeg' ||
                fileType === 'image/jpg' ||
                fileType === 'image/png'
            ){

                const reader = new FileReader()

                reader.onload = (e) => {

                    preview.src = e.target.result

                    preview.style.display = 'block'

                    mensaje.textContent = file.name

                }

                reader.readAsDataURL(file)

            }
            else{

                preview.style.display = 'none'

                mensaje.textContent =
                    'El archivo no es válido'

            }

        }
        else{

            preview.style.display = 'none'

            mensaje.textContent =
                'No se ha seleccionado archivo'

        }

    })

}

configurarPreviewImagen(
    'imagen',
    'preview',
    'mensaje'
)

configurarPreviewImagen(
    'imagenActualizar',
    'previewActualizar',
    'mensajeActualizar'
)