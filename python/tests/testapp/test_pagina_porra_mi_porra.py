import json

def test_pagina_porra_mi_porra_sin_login(cliente, conexion):

	respuesta=cliente.get("/porra/mi_porra", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

def test_pagina_porra_mi_porra_porra_no_completada(cliente, conexion_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/porra/mi_porra")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/porra"
		assert "<h1>Redirecting...</h1>" in contenido

def test_pagina_porra_mi_porra(cliente, conexion_usuario, porra_grupos, porra_mejores_terceros, partidos_bracket):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra_grupos})

		cliente_abierto.post("/porra/mejores_terceros/guardar", json={"equipos":porra_mejores_terceros})
		
		cliente_abierto.post("/porra/eliminatorias/guardar", data={"elecciones_eliminatorias":json.dumps(partidos_bracket)})

		respuesta=cliente_abierto.get("/porra/mi_porra")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<div class="mi-porra-wrapper">' in contenido
		assert '<div class="info-clasificacion">' in contenido
		assert '<h1 class="titulo-pagina">Mi Porra' in contenido
		assert '<section class="mi-porra-seccion">' in contenido
		assert '<h2 class="titulo-seccion">Fase de grupos</h2>' in contenido
		assert '<div class="grupos-grid">' in contenido
		assert '<div class="grupo-container">' in contenido
		assert '<div class="grupo-lista">' in contenido
		assert '<div class="equipo-card' in contenido