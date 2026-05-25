def test_pagina_porra_grupos_sin_login(cliente, conexion):

	respuesta=cliente.get("/porra/grupos", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

def test_pagina_porra_grupos(cliente, conexion_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/porra/grupos")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<div class="porra-grupos-wrapper">' in contenido
		assert '<div class="info-clasificacion">' in contenido
		assert '<h1 class="titulo-pagina">Fase de Grupos</h1>' in contenido
		assert '<div class="grupo-container">' in contenido

		for grupo in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']:

			assert f"<h2>Grupo {grupo}</h2>" in contenido
			assert f'<div class="grupo-lista" data-grupo="{grupo}">' in contenido

		assert '<div id="modalResumen" class="modal-overlay">' in contenido
		assert "<h2> Confirmar Clasificación Grupos </h2>" in contenido