import os

def test_pagina_clasificacion_sin_login(cliente, conexion):

	respuesta=cliente.get("/clasificacion/123456", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

def test_pagina_clasificacion_no_existe_codigo(cliente, conexion_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/clasificacion/123456")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/porra"
		assert "<h1>Redirecting...</h1>" in contenido

def test_pagina_clasificacion_no_codigo_usuario(cliente, conexion_usuario):

	conexion_usuario.insertarCodigoLiga("123456")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/clasificacion/123456")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/porra"
		assert "<h1>Redirecting...</h1>" in contenido

def test_pagina_clasificacion(cliente, conexion_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/clasificacion/3YYZKP")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<main class="clasificacion-container">' in contenido
		assert '<div class="clasificacion-header">' in contenido
		assert '<section class="podium">' in contenido
		assert '<section class="ranking-list">' in contenido
		assert '<div class="podium-avatar">' in contenido
		assert "nacho98_perfil.jpeg" not in contenido

def test_pagina_clasificacion_con_imagen(cliente, conexion_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		ruta_imagen_test=os.path.join(os.getcwd(), "testapp", "imagenes_tests", "imagen_tests.jpeg")

		data={}

		with open(ruta_imagen_test, "rb") as imagen_file:
			
			data["imagen"]=(imagen_file, "imagen_tests.jpeg")

			cliente_abierto.post("/settings/actualizar_imagen_perfil", data=data, buffered=True, content_type="multipart/form-data")

		respuesta=cliente_abierto.get("/clasificacion/3YYZKP")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<main class="clasificacion-container">' in contenido
		assert '<div class="clasificacion-header">' in contenido
		assert '<section class="podium">' in contenido
		assert '<section class="ranking-list">' in contenido
		assert '<div class="podium-avatar">' not in contenido
		assert "nacho98_perfil.jpeg" in contenido

def test_pagina_clasificacion_no_admin(cliente, conexion_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/clasificacion/3YYZKP")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert "/porra/nacho98" not in contenido
		assert 'data-podium-card-user="nacho98"' not in contenido
		assert 'style="cursor: pointer;"' not in contenido
		assert 'data-ranking-card-user="nacho98"' not in contenido

def test_pagina_clasificacion_admin(cliente, conexion_usuario):

	conexion_usuario.c.execute("UPDATE usuarios SET Admin=True")

	conexion_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/clasificacion/3YYZKP")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert "/porra/nacho98" in contenido
		assert 'data-podium-card-user="nacho98"' in contenido
		assert 'style="cursor: pointer;"' in contenido
		assert 'data-ranking-card-user="nacho98"' in contenido