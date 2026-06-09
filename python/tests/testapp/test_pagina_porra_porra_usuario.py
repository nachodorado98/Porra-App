import json
import pytest
import os
from datetime import datetime, timedelta

def test_pagina_porra_porra_usuario_sin_login(cliente, conexion):

	respuesta=cliente.get("/porra/nacho98", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

def test_pagina_porra_porra_usuario_usuario_no_existe(cliente, conexion_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/porra/no_existo")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/porra"
		assert "<h1>Redirecting...</h1>" in contenido

def test_pagina_porra_porra_usuario_usuario_no_admin(cliente, conexion_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/porra/nacho98")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/porra"
		assert "<h1>Redirecting...</h1>" in contenido

@pytest.mark.parametrize(["dias"],
	[(2,),(22,),(5,),(13,),(25,),(1,)]
)
def test_pagina_porra_porra_usuario_porra_abierta(cliente, conexion_usuario, dias):

	fecha_posterior=(datetime.now()+timedelta(days=dias)).strftime("%Y-%m-%d")

	conexion_usuario.insertarClaveValorMaestro("fecha_cierre_porra", fecha_posterior)

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
		assert '<h1 class="titulo-pagina">' in contenido
		assert "nacho98_perfil.jpeg" not in contenido
		assert "Porra de nacho98" in contenido
		assert '<section class="mi-porra-seccion">' in contenido
		assert '<h2 class="titulo-seccion">Fase de grupos</h2>' in contenido
		assert '<h2 class="titulo-seccion">Mejores terceros' in contenido
		assert '<h2 class="titulo-seccion">Fase eliminatoria' in contenido

@pytest.mark.parametrize(["dias"],
	[(2,),(22,),(5,),(13,),(25,),(1,),(0,)]
)
def test_pagina_porra_porra_usuario_porra_cerrada(cliente, conexion_usuario, porra_grupos, porra_mejores_terceros, partidos_bracket, password_hash, dias):

	conexion_usuario.insertarUsuario("usuario", "correo@correo.es", password_hash, "nacho", "dorado", "3YYZKP")

	conexion_usuario.insertarEstadoPorraUsuario("usuario")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra_grupos})

		cliente_abierto.post("/porra/mejores_terceros/guardar", json={"equipos":porra_mejores_terceros})
		
		cliente_abierto.post("/porra/eliminatorias/guardar", data={"elecciones_eliminatorias":json.dumps(partidos_bracket)})

	fecha_anterior=(datetime.now()-timedelta(days=dias)).strftime("%Y-%m-%d")

	conexion_usuario.insertarClaveValorMaestro("fecha_cierre_porra", fecha_anterior)

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "usuario", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/porra/nacho98")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<div class="mi-porra-wrapper">' in contenido
		assert '<div class="info-clasificacion">' in contenido
		assert '<h1 class="titulo-pagina">' in contenido
		assert "Porra de nacho98" in contenido
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
		assert '<h1 class="titulo-pagina">' in contenido
		assert "Mi Porra" in contenido
		assert '<section class="mi-porra-seccion">' in contenido
		assert '<h2 class="titulo-seccion">Fase de grupos</h2>' in contenido
		assert '<h2 class="titulo-seccion">Mejores terceros' in contenido
		assert '<h2 class="titulo-seccion">Fase eliminatoria' in contenido

def test_pagina_porra_porra_usuario_con_imagen(cliente, conexion_usuario, porra_grupos, porra_mejores_terceros, partidos_bracket, password_hash):

	conexion_usuario.insertarUsuario("usuario", "correo@correo.es", password_hash, "nacho", "dorado", "3YYZKP")

	conexion_usuario.insertarEstadoPorraUsuario("usuario")

	conexion_usuario.c.execute("UPDATE usuarios SET Admin=True")

	conexion_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra_grupos})

		cliente_abierto.post("/porra/mejores_terceros/guardar", json={"equipos":porra_mejores_terceros})
		
		cliente_abierto.post("/porra/eliminatorias/guardar", data={"elecciones_eliminatorias":json.dumps(partidos_bracket)})

		ruta_imagen_test=os.path.join(os.getcwd(), "testapp", "imagenes_tests", "imagen_tests.jpeg")

		data={}

		with open(ruta_imagen_test, "rb") as imagen_file:
			
			data["imagen"]=(imagen_file, "imagen_tests.jpeg")

			cliente_abierto.post("/settings/actualizar_imagen_perfil", data=data, buffered=True, content_type="multipart/form-data")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "usuario", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/porra/nacho98")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<div class="mi-porra-wrapper">' in contenido
		assert '<div class="info-clasificacion">' in contenido
		assert '<h1 class="titulo-pagina">' in contenido
		assert "nacho98_perfil.jpeg" in contenido
		assert "Porra de nacho98" in contenido
		assert '<section class="mi-porra-seccion">' in contenido
		assert '<h2 class="titulo-seccion">Fase de grupos</h2>' in contenido
		assert '<h2 class="titulo-seccion">Mejores terceros' in contenido
		assert '<h2 class="titulo-seccion">Fase eliminatoria' in contenido