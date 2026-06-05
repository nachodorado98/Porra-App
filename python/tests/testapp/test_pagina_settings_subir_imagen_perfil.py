import os
import time

from src.utilidades.utils import existe_imagen_datalake

def test_pagina_settings_actualizar_imagen_perfil_sin_login(cliente):

	respuesta=cliente.post("/settings/actualizar_imagen_perfil", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

def test_pagina_settings_actualizar_imagen_perfil_usuario_con_imagen_no_valida(cliente, conexion_usuario, datalake, contenedor_dl):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		conexion_usuario.c.execute("SELECT imagen_perfil FROM usuarios")

		imagen_usuario=conexion_usuario.c.fetchone()

		assert not imagen_usuario["imagen_perfil"]

		ruta_imagen_test=os.path.join(os.getcwd(), "testapp", "imagenes_tests", "imagen_tests_no_valida.txt")

		data={}

		with open(ruta_imagen_test, "rb") as imagen_file:
			
			data["imagen"]=(imagen_file, "imagen_tests_no_valida.txt")

			respuesta=cliente_abierto.post("/settings/actualizar_imagen_perfil", data=data, buffered=True, content_type="multipart/form-data")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/settings"
		assert "Redirecting..." in contenido

		ruta_carpeta_imagenes=os.path.join(os.path.abspath(".."), "src", "static", "imagenes", "perfil", "nacho98")

		ruta_imagen=os.path.join(ruta_carpeta_imagenes, "nacho98_perfil.txt")

		assert not os.path.exists(ruta_imagen)

		conexion_usuario.c.execute("SELECT imagen_perfil FROM usuarios")

		imagen_usuario=conexion_usuario.c.fetchone()

		assert not imagen_usuario["imagen_perfil"]

		datalake.existe_carpeta(contenedor_dl, "perfil/nacho98")

		assert not existe_imagen_datalake("nacho98", "imagen_tests_no_valida.txt", contenedor_dl)

		datalake.cerrarConexion()

def test_pagina_settings_actualizar_imagen_perfil_usuario_con_imagen_valida(cliente, conexion_usuario, datalake, contenedor_dl):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		conexion_usuario.c.execute("SELECT imagen_perfil FROM usuarios")

		imagen_usuario=conexion_usuario.c.fetchone()

		assert not imagen_usuario["imagen_perfil"]

		ruta_imagen_test=os.path.join(os.getcwd(), "testapp", "imagenes_tests", "imagen_tests.jpeg")

		data={}

		with open(ruta_imagen_test, "rb") as imagen_file:
			
			data["imagen"]=(imagen_file, "imagen_tests.jpeg")

			respuesta=cliente_abierto.post("/settings/actualizar_imagen_perfil", data=data, buffered=True, content_type="multipart/form-data")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/settings"
		assert "Redirecting..." in contenido
		
		ruta_carpeta_imagenes=os.path.join(os.path.abspath(".."), "src", "static", "imagenes", "perfil", "nacho98")

		ruta_imagen=os.path.join(ruta_carpeta_imagenes, "nacho98_perfil.jpeg")

		assert os.path.exists(ruta_imagen)

		conexion_usuario.c.execute("SELECT imagen_perfil FROM usuarios")

		imagen_usuario=conexion_usuario.c.fetchone()

		assert imagen_usuario["imagen_perfil"]=="nacho98_perfil.jpeg"

		datalake.existe_carpeta(contenedor_dl, "perfil/nacho98")

		time.sleep(5)

		assert existe_imagen_datalake("nacho98", "nacho98_perfil.jpeg", contenedor_dl)

		datalake.cerrarConexion()

def test_pagina_settings_actualizar_imagen_perfil_usuario_con_imagen_existente(cliente, conexion_usuario, datalake, contenedor_dl):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		ruta_imagen_test=os.path.join(os.getcwd(), "testapp", "imagenes_tests", "imagen_tests.jpeg")

		data={}

		with open(ruta_imagen_test, "rb") as imagen_file:
			
			data["imagen"]=(imagen_file, "imagen_tests.jpeg")

			cliente_abierto.post("/settings/actualizar_imagen_perfil", data=data, buffered=True, content_type="multipart/form-data")
		
		ruta_carpeta_imagenes=os.path.join(os.path.abspath(".."), "src", "static", "imagenes", "perfil", "nacho98")

		ruta_imagen=os.path.join(ruta_carpeta_imagenes, "nacho98_perfil.jpeg")

		assert os.path.exists(ruta_imagen)

		conexion_usuario.c.execute("SELECT imagen_perfil FROM usuarios")

		imagen_usuario=conexion_usuario.c.fetchone()

		assert imagen_usuario["imagen_perfil"]=="nacho98_perfil.jpeg"

		ruta_imagen_test_nueva=os.path.join(os.getcwd(), "testapp", "imagenes_tests", "imagen_tests_nueva.png")

		data={}

		with open(ruta_imagen_test_nueva, "rb") as imagen_file:
			
			data["imagen"]=(imagen_file, "imagen_tests_nueva.png")

			respuesta=cliente_abierto.post("/settings/actualizar_imagen_perfil", data=data, buffered=True, content_type="multipart/form-data")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/settings"
		assert "Redirecting..." in contenido
		
		ruta_carpeta_imagenes=os.path.join(os.path.abspath(".."), "src", "static", "imagenes", "perfil", "nacho98")

		ruta_imagen=os.path.join(ruta_carpeta_imagenes, "nacho98_perfil.png")

		assert os.path.exists(ruta_imagen)

		conexion_usuario.c.execute("SELECT imagen_perfil FROM usuarios")

		imagen_usuario=conexion_usuario.c.fetchone()

		assert imagen_usuario["imagen_perfil"]=="nacho98_perfil.png"

		datalake.existe_carpeta(contenedor_dl, "perfil/nacho98")

		time.sleep(5)

		assert existe_imagen_datalake("nacho98", "nacho98_perfil.png", contenedor_dl)

		datalake.cerrarConexion()