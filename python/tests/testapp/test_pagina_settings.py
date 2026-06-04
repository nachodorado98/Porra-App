import pytest
import os
from datetime import datetime, timedelta

def test_pagina_settings_sin_login(cliente, conexion):

	respuesta=cliente.get("/settings", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

def test_pagina_settings_sin_imagen_perfil(cliente, conexion_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/settings")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<div class="settings-wrapper">' in contenido
		assert '<div class="settings-card">' in contenido
		assert '<h1 class="titulo-pagina">Configuración' in contenido
		assert '<p class="descripcion-settings">Sube una imagen personalizada para tu perfil.</p>' in contenido
		assert '<div class="contenedor-subir-imagen">' in contenido
		assert '<div class="contenedor-imagen-actual" id="contenedorImagen">' not in contenido
		assert '<div class="seccion-actualizar-imagen-perfil"' not in contenido
		assert '<div id="modalEliminar" class="modal-overlay">' in contenido
		assert '<div class="settings-section danger-zone">' in contenido
		assert '<div class="settings-section password-section">' in contenido
		assert '<h2>Cambiar contraseña</h2>' in contenido
		assert '<form action="/settings/cambiar_contrasena" method="POST" class="form-cambiar-contrasena">' in contenido

def test_pagina_settings_con_imagen_perfil(cliente, conexion_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		ruta_imagen_test=os.path.join(os.getcwd(), "testapp", "imagenes_tests", "imagen_tests.jpeg")

		data={}

		with open(ruta_imagen_test, "rb") as imagen_file:
			
			data["imagen"]=(imagen_file, "imagen_tests.jpeg")

			cliente_abierto.post("/settings/actualizar_imagen_perfil", data=data, buffered=True, content_type="multipart/form-data")

		respuesta=cliente_abierto.get("/settings")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<div class="settings-wrapper">' in contenido
		assert '<div class="settings-card">' in contenido
		assert '<h1 class="titulo-pagina">Configuración' in contenido
		assert '<p class="descripcion-settings">Sube una imagen personalizada para tu perfil.</p>' not in contenido
		assert '<div class="contenedor-subir-imagen">' in contenido
		assert '<div class="contenedor-imagen-actual" id="contenedorImagen">' in contenido
		assert '<img class="imagen-perfil"' in contenido
		assert "/nacho98_perfil.jpeg" in contenido
		assert '<div class="seccion-actualizar-imagen" id="contenedorActualizarImagenPerfil">'  in contenido
		assert '<div id="modalEliminar" class="modal-overlay">' in contenido
		assert '<div class="settings-section danger-zone">' in contenido
		assert '<div class="settings-section password-section">' in contenido
		assert '<h2>Cambiar contraseña</h2>' in contenido
		assert '<form action="/settings/cambiar_contrasena" method="POST" class="form-cambiar-contrasena">' in contenido

@pytest.mark.parametrize(["cambios", "ultimo_cambio"],
	[
		(0, datetime.now()-timedelta(hours=23)),
		(2, datetime.now()-timedelta(hours=12)),
		(3, datetime.now()-timedelta(days=20)),
		(4, datetime.now()-timedelta(days=100))
	]
)
def test_pagina_settings_no_puede_cambio_contrasena(cliente, conexion_usuario, cambios, ultimo_cambio):

	conexion_usuario.c.execute(f"UPDATE usuarios SET Cambios_Contrasena={cambios}, Ultimo_Cambio_Contrasena='{ultimo_cambio}'")

	conexion_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		ruta_imagen_test=os.path.join(os.getcwd(), "testapp", "imagenes_tests", "imagen_tests.jpeg")

		data={}

		with open(ruta_imagen_test, "rb") as imagen_file:
			
			data["imagen"]=(imagen_file, "imagen_tests.jpeg")

			cliente_abierto.post("/settings/actualizar_imagen_perfil", data=data, buffered=True, content_type="multipart/form-data")

		respuesta=cliente_abierto.get("/settings")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<div class="settings-section password-section">' in contenido
		assert '<h2>Cambiar contraseña</h2>' in contenido
		assert '<form action="/settings/cambiar_contrasena" method="POST" class="form-cambiar-contrasena">' not in contenido

@pytest.mark.parametrize(["cambios", "ultimo_cambio"],
	[
		(0, datetime.now()-timedelta(hours=48)),
		(2, datetime.now()-timedelta(hours=48)),
		(2, datetime.now()-timedelta(hours=24))
	]
)
def test_pagina_settings_puede_cambio_contrasena(cliente, conexion_usuario, cambios, ultimo_cambio):

	conexion_usuario.c.execute(f"UPDATE usuarios SET Cambios_Contrasena={cambios}, Ultimo_Cambio_Contrasena='{ultimo_cambio}'")

	conexion_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		ruta_imagen_test=os.path.join(os.getcwd(), "testapp", "imagenes_tests", "imagen_tests.jpeg")

		data={}

		with open(ruta_imagen_test, "rb") as imagen_file:
			
			data["imagen"]=(imagen_file, "imagen_tests.jpeg")

			cliente_abierto.post("/settings/actualizar_imagen_perfil", data=data, buffered=True, content_type="multipart/form-data")

		respuesta=cliente_abierto.get("/settings")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<div class="settings-section password-section">' in contenido
		assert '<h2>Cambiar contraseña</h2>' in contenido
		assert '<form action="/settings/cambiar_contrasena" method="POST" class="form-cambiar-contrasena">' in contenido