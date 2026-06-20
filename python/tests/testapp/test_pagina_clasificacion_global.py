import os
import pytest
from datetime import datetime, timedelta

def test_pagina_clasificacion_global_sin_login(cliente, conexion):

	respuesta=cliente.get("/clasificacion/global", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

def test_pagina_clasificacion_global(cliente, conexion_usuario):

	conexion_usuario.actualizarEstadoPorraUsuario("nacho98")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/clasificacion/global")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<main class="clasificacion-container">' in contenido
		assert '<div class="clasificacion-header">' in contenido
		assert '<section class="podium">' in contenido
		assert '<section class="ranking-list">' in contenido
		assert '<div class="podium-avatar">' in contenido
		assert "nacho98_perfil.jpeg" not in contenido
		assert '<button type="button" class="ranking-btn secondary ver-puntos">Ver puntos</button>' in contenido
		assert '<div class="detalle-puntos">' in contenido

def test_pagina_clasificacion_global_con_imagen(cliente, conexion_usuario):

	conexion_usuario.actualizarEstadoPorraUsuario("nacho98")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		ruta_imagen_test=os.path.join(os.getcwd(), "testapp", "imagenes_tests", "imagen_tests.jpeg")

		data={}

		with open(ruta_imagen_test, "rb") as imagen_file:
			
			data["imagen"]=(imagen_file, "imagen_tests.jpeg")

			cliente_abierto.post("/settings/actualizar_imagen_perfil", data=data, buffered=True, content_type="multipart/form-data")

		respuesta=cliente_abierto.get("/clasificacion/global")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<main class="clasificacion-container">' in contenido
		assert '<div class="clasificacion-header">' in contenido
		assert '<section class="podium">' in contenido
		assert '<section class="ranking-list">' in contenido
		assert '<div class="podium-avatar">' not in contenido
		assert "nacho98_perfil.jpeg" in contenido
		assert '<button type="button" class="ranking-btn secondary ver-puntos">Ver puntos</button>' in contenido
		assert '<div class="detalle-puntos">' in contenido

def test_pagina_clasificacion_global_puede_pinchar_no_admin(cliente, conexion_usuario):

	conexion_usuario.actualizarEstadoPorraUsuario("nacho98")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/clasificacion/global")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert "/porra/nacho98" not in contenido
		assert 'data-podium-card-user="nacho98"' not in contenido
		assert 'style="cursor: pointer;"' not in contenido
		assert 'class="ranking-btn primary">Ver porra</a>' not in contenido

@pytest.mark.parametrize(["dias"],
	[(2,),(22,),(5,),(13,),(25,),(1,)]
)
def test_pagina_clasificacion_global_puede_pinchar_porra_abierta(cliente, conexion_usuario, dias):

	conexion_usuario.actualizarEstadoPorraUsuario("nacho98")

	fecha_posterior=(datetime.now()+timedelta(days=dias)).strftime("%Y-%m-%d")

	conexion_usuario.insertarClaveValorMaestro("fecha_cierre_porra", fecha_posterior)

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/clasificacion/global")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert "/porra/nacho98" not in contenido
		assert 'data-podium-card-user="nacho98"' not in contenido
		assert 'style="cursor: pointer;"' not in contenido
		assert 'class="ranking-btn primary">Ver porra</a>' not in contenido

def test_pagina_clasificacion_global_puede_pinchar_admin(cliente, conexion_usuario):

	conexion_usuario.actualizarEstadoPorraUsuario("nacho98")

	conexion_usuario.c.execute("UPDATE usuarios SET Admin=True")

	conexion_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/clasificacion/global")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert "/porra/nacho98" in contenido
		assert 'data-podium-card-user="nacho98"' in contenido
		assert 'style="cursor: pointer;"' in contenido
		assert 'class="ranking-btn primary">Ver porra</a>' in contenido

@pytest.mark.parametrize(["dias"],
	[(2,),(22,),(5,),(13,),(25,),(1,),(0,)]
)
def test_pagina_clasificacion_global_puede_pinchar_porra_cerrada(cliente, conexion_usuario, dias):

	conexion_usuario.actualizarEstadoPorraUsuario("nacho98")

	fecha_anterior=(datetime.now()-timedelta(days=dias)).strftime("%Y-%m-%d")

	conexion_usuario.insertarClaveValorMaestro("fecha_cierre_porra", fecha_anterior)

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/clasificacion/global")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert "/porra/nacho98" in contenido
		assert 'data-podium-card-user="nacho98"' in contenido
		assert 'style="cursor: pointer;"' in contenido
		assert 'class="ranking-btn primary">Ver porra</a>' in contenido

def test_pagina_clasificacion_global_puede_pinchar_admin_porra_no_completada(cliente, conexion_usuario):

	conexion_usuario.c.execute("UPDATE usuarios SET Admin=True")

	conexion_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/clasificacion/global")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert 'class="ranking-btn primary">Ver porra</a>' not in contenido

@pytest.mark.parametrize(["dias"],
	[(2,),(22,),(5,),(13,),(25,),(1,),(0,)]
)
def test_pagina_clasificacion_global_puede_pinchar_porra_cerrada_porra_no_completada(cliente, conexion_usuario, dias):

	fecha_anterior=(datetime.now()-timedelta(days=dias)).strftime("%Y-%m-%d")

	conexion_usuario.insertarClaveValorMaestro("fecha_cierre_porra", fecha_anterior)

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/clasificacion/global")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert 'class="ranking-btn primary">Ver porra</a>' not in contenido