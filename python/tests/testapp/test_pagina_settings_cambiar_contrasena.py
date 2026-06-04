import pytest
from datetime import datetime, timedelta

def test_pagina_settings_cambiar_contrasena_sin_login(cliente, conexion):

	respuesta=cliente.post("/settings/cambiar_contrasena", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

def test_pagina_settings_cambiar_contrasena_data_no_valida(cliente, conexion_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.post("/settings/cambiar_contrasena", data={"data":"data"})

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/settings"
		assert "<h1>Redirecting...</h1>" in contenido

def test_pagina_settings_cambiar_contrasena_contrasena_nueva_introducida_igual_contrasena_actual_introducida(cliente, conexion_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.post("/settings/cambiar_contrasena", data={"contrasena_actual":"12345678",
																				"nueva_contrasena":"12345678",
																				"repetir_contrasena":"12345679"})

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/settings"
		assert "<h1>Redirecting...</h1>" in contenido

def test_pagina_settings_cambiar_contrasena_contrasena_nueva_introducida_distinta_repetir_contrasena_introducida(cliente, conexion_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.post("/settings/cambiar_contrasena", data={"contrasena_actual":"12345678",
																				"nueva_contrasena":"12345679",
																				"repetir_contrasena":"12345677"})

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/settings"
		assert "<h1>Redirecting...</h1>" in contenido

@pytest.mark.parametrize(["contrasena"],
    [("clave",),("PASSWD",),("1234567",),("Abcdefg",),("",),("A1b2C3d",),("abcd",),("1234",),
     ("Ab CdEfGhI",),("Ab!CdEfGhI ",),(" Ab!CdEfGhI",),("AIJKLMN",),("Ab@cdE2",),
     ("Ab@cdEf1 G",),("Abcd12 34!",),(None,)]
)
def test_pagina_settings_cambiar_contrasena_contrasena_nueva_introducida_no_valida(cliente, conexion_usuario, contrasena):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.post("/settings/cambiar_contrasena", data={"contrasena_actual":"12345678",
																				"nueva_contrasena":contrasena,
																				"repetir_contrasena":contrasena})

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/settings"
		assert "<h1>Redirecting...</h1>" in contenido

def test_pagina_settings_cambiar_contrasena_contrasena_actual_introducida_distinta_contrasena_actual_usuario(cliente, conexion_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.post("/settings/cambiar_contrasena", data={"contrasena_actual":"12345678",
																				"nueva_contrasena":"12345679",
																				"repetir_contrasena":"12345679"})

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/settings"
		assert "<h1>Redirecting...</h1>" in contenido

def test_pagina_settings_cambiar_contrasena_contrasena_nueva_introducida_igual_contrasena_actual_introducida_hashes(cliente, conexion_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.post("/settings/cambiar_contrasena", data={"contrasena_actual":"Ab!CdEfGhIJK3LMN",
																				"nueva_contrasena":"Ab!CdEfGhIJK3LMN",
																				"repetir_contrasena":"Ab!CdEfGhIJK3LMN"})

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/settings"
		assert "<h1>Redirecting...</h1>" in contenido

@pytest.mark.parametrize(["cambios", "ultimo_cambio"],
	[
		(0, datetime.now()-timedelta(hours=23)),
		(2, datetime.now()-timedelta(hours=12)),
		(3, datetime.now()-timedelta(days=20)),
		(4, datetime.now()-timedelta(days=100))
	]
)
def test_pagina_settings_cambiar_contrasena_no_puede_cambio_contrasena(cliente, conexion_usuario, cambios, ultimo_cambio):

	conexion_usuario.c.execute(f"UPDATE usuarios SET Cambios_Contrasena={cambios}, Ultimo_Cambio_Contrasena='{ultimo_cambio}'")

	conexion_usuario.confirmar()

	contrasena_previa=conexion_usuario.obtenerContrasenaUsuario("nacho98")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.post("/settings/cambiar_contrasena", data={"contrasena_actual":"Ab!CdEfGhIJK3LMN",
																				"nueva_contrasena":"12345678",
																				"repetir_contrasena":"12345678"})

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/settings"
		assert "<h1>Redirecting...</h1>" in contenido

		contrasena_nueva=conexion_usuario.obtenerContrasenaUsuario("nacho98")

		assert contrasena_previa==contrasena_nueva

@pytest.mark.parametrize(["cambios", "ultimo_cambio"],
	[
		(0, datetime.now()-timedelta(hours=48)),
		(2, datetime.now()-timedelta(hours=48)),
		(2, datetime.now()-timedelta(hours=24))
	]
)
def test_pagina_settings_cambiar_contrasena_puede_cambio_contrasena(cliente, conexion_usuario, cambios, ultimo_cambio):

	conexion_usuario.c.execute(f"UPDATE usuarios SET Cambios_Contrasena={cambios}, Ultimo_Cambio_Contrasena='{ultimo_cambio}'")

	conexion_usuario.confirmar()

	contrasena_previa=conexion_usuario.obtenerContrasenaUsuario("nacho98")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.post("/settings/cambiar_contrasena", data={"contrasena_actual":"Ab!CdEfGhIJK3LMN",
																				"nueva_contrasena":"12345678",
																				"repetir_contrasena":"12345678"})

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/settings"
		assert "<h1>Redirecting...</h1>" in contenido

		datos_usuario=conexion_usuario.obtenerDatosCambioContrasenaUsuario("nacho98")

		assert datos_usuario[0]==cambios+1
		assert datos_usuario[1].strftime("%Y-%m-%d")==datetime.now().strftime("%Y-%m-%d")

		contrasena_nueva=conexion_usuario.obtenerContrasenaUsuario("nacho98")

		assert contrasena_previa!=contrasena_nueva