def test_pagina_porra_sin_login(cliente, conexion):

	respuesta=cliente.get("/porra", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

def test_pagina_porra(cliente, conexion_usuario):

	respuesta=cliente.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert '<main class="main-content">' in contenido
	assert "<h1>Tu porra del Mundial</h1>" in contenido
	assert '<a href="/porra/grupos" class="btn-empezar" data-loading="true">Empezar porra →</a>' in contenido

def test_pagina_porra_grupos_completos(cliente, conexion_usuario):

	conexion_usuario.actualizarEstadoPorraGruposUsuario("nacho98")

	respuesta=cliente.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert '<main class="main-content">' in contenido
	assert "<h1>Tu porra del Mundial</h1>" in contenido
	assert '<a href="/porra/mejores_terceros" class="btn-empezar" data-loading="true">Continuar porra →</a>' in contenido

def test_pagina_porra_mejores_terceros_completos(cliente, conexion_usuario):

	conexion_usuario.actualizarEstadoPorraGruposUsuario("nacho98")

	conexion_usuario.actualizarEstadoPorraMejoresTercerosUsuario("nacho98")

	respuesta=cliente.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert '<main class="main-content">' in contenido
	assert "<h1>Tu porra del Mundial</h1>" in contenido
	assert '<a href="/porra/eliminatorias" class="btn-empezar" data-loading="true">Continuar porra →</a>' in contenido