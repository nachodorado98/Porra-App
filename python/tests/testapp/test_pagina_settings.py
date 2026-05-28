def test_pagina_settings_sin_login(cliente, conexion):

	respuesta=cliente.get("/settings", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

def test_pagina_settings(cliente, conexion_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/settings")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<div class="settings-wrapper">' in contenido
		assert '<div class="settings-card">' in contenido
		assert '<h1 class="titulo-pagina">Configuración' in contenido
		assert '<div class="settings-section danger-zone">' in contenido