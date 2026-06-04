import json

def test_pagina_porra_porra_usuario_sin_login(cliente, conexion):

	respuesta=cliente.get("/porra/nacho98", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

def test_pagina_porra_porra_usuario_usuario_no_admin(cliente, conexion_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/porra/nacho98")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/porra"
		assert "<h1>Redirecting...</h1>" in contenido

def test_pagina_porra_porra_usuario_porra_no_completada(cliente, conexion_usuario):

	conexion_usuario.c.execute("UPDATE usuarios SET Admin=True")

	conexion_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/porra/nacho98")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/porra"
		assert "<h1>Redirecting...</h1>" in contenido

def test_pagina_porra_porra_usuario(cliente, conexion_usuario, porra_grupos, porra_mejores_terceros, partidos_bracket, password_hash):

	conexion_usuario.insertarUsuario("usuario", "correo@correo.es", password_hash, "nacho", "dorado", "3YYZKP")

	conexion_usuario.insertarEstadoPorraUsuario("usuario")

	conexion_usuario.c.execute("UPDATE usuarios SET Admin=True")

	conexion_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra_grupos})

		cliente_abierto.post("/porra/mejores_terceros/guardar", json={"equipos":porra_mejores_terceros})
		
		cliente_abierto.post("/porra/eliminatorias/guardar", data={"elecciones_eliminatorias":json.dumps(partidos_bracket)})

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "usuario", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/porra/nacho98")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<div class="mi-porra-wrapper">' in contenido
		assert '<div class="info-clasificacion">' in contenido
		assert '<h1 class="titulo-pagina">Porra de nacho98' in contenido
		assert '<section class="mi-porra-seccion">' in contenido
		assert '<h2 class="titulo-seccion">Fase de grupos</h2>' in contenido
		assert '<h2 class="titulo-seccion">Mejores terceros' in contenido
		assert '<h2 class="titulo-seccion">Fase eliminatoria' in contenido

def test_pagina_porra_porra_usuario_mismo_usuario(cliente, conexion_usuario, porra_grupos, porra_mejores_terceros, partidos_bracket):

	conexion_usuario.c.execute("UPDATE usuarios SET Admin=True")

	conexion_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra_grupos})

		cliente_abierto.post("/porra/mejores_terceros/guardar", json={"equipos":porra_mejores_terceros})
		
		cliente_abierto.post("/porra/eliminatorias/guardar", data={"elecciones_eliminatorias":json.dumps(partidos_bracket)})

		respuesta=cliente_abierto.get("/porra/nacho98", follow_redirects=True)

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<div class="mi-porra-wrapper">' in contenido
		assert '<div class="info-clasificacion">' in contenido
		assert '<h1 class="titulo-pagina">Mi Porra' in contenido
		assert '<section class="mi-porra-seccion">' in contenido
		assert '<h2 class="titulo-seccion">Fase de grupos</h2>' in contenido
		assert '<h2 class="titulo-seccion">Mejores terceros' in contenido
		assert '<h2 class="titulo-seccion">Fase eliminatoria' in contenido