import pytest
from datetime import datetime, timedelta

def test_pagina_settings_admin_cambiar_contrasena_usuario_sin_login(cliente, conexion):

	respuesta=cliente.post("/settings/admin/cambiar_contrasena_usuario", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

def test_pagina_settings_admin_cambiar_contrasena_usuario_no_admin(cliente, conexion_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.post("/settings/admin/cambiar_contrasena_usuario", data={"data":"data"})

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/settings"
		assert "<h1>Redirecting...</h1>" in contenido

def test_pagina_settings_admin_cambiar_contrasena_usuario_usuario_no_existe(cliente, conexion_usuario):

	conexion_usuario.c.execute("UPDATE usuarios SET Admin=True")

	conexion_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.post("/settings/admin/cambiar_contrasena_usuario", data={"usuario":"golden", "nueva_contrasena":"12345679"})

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/settings"
		assert "<h1>Redirecting...</h1>" in contenido

def test_pagina_settings_admin_cambiar_contrasena_usuario_contrasena_nueva_introducida_igual_contrasena_actual_introducida(cliente, conexion_usuario, password_hash):

	conexion_usuario.insertarUsuario("golden", "correo@correo.es", password_hash, "nacho", "dorado", "3YYZKP")

	conexion_usuario.c.execute("UPDATE usuarios SET Admin=True")

	conexion_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.post("/settings/admin/cambiar_contrasena_usuario", data={"usuario":"golden", "nueva_contrasena":"Ab!CdEfGhIJK3LMN"})

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/settings"
		assert "<h1>Redirecting...</h1>" in contenido

@pytest.mark.parametrize(["contrasena"],
    [("clave",),("PASSWD",),("1234567",),("Abcdefg",),("",),("A1b2C3d",),("abcd",),("1234",),
     ("Ab CdEfGhI",),("Ab!CdEfGhI ",),(" Ab!CdEfGhI",),("AIJKLMN",),("Ab@cdE2",),
     ("Ab@cdEf1 G",),("Abcd12 34!",),(None,)]
)
def test_pagina_settings_admin_cambiar_contrasena_usuario_contrasena_nueva_introducida_no_valida(cliente, conexion_usuario, password_hash, contrasena):

	conexion_usuario.insertarUsuario("golden", "correo@correo.es", password_hash, "nacho", "dorado", "3YYZKP")

	conexion_usuario.c.execute("UPDATE usuarios SET Admin=True")

	conexion_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.post("/settings/admin/cambiar_contrasena_usuario", data={"usuario":"golden", "nueva_contrasena":contrasena})

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/settings"
		assert "<h1>Redirecting...</h1>" in contenido

def test_pagina_settings_admin_cambiar_contrasena_usuario(cliente, conexion_usuario, password_hash):

	conexion_usuario.insertarUsuario("golden", "correo@correo.es", password_hash, "nacho", "dorado", "3YYZKP")

	conexion_usuario.c.execute("UPDATE usuarios SET Admin=True")

	conexion_usuario.confirmar()

	datos_usuario_previo=conexion_usuario.obtenerDatosCambioContrasenaUsuario("golden")

	contrasena_previa=conexion_usuario.obtenerContrasenaUsuario("golden")

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.post("/settings/admin/cambiar_contrasena_usuario", data={"usuario":"golden", "nueva_contrasena":"12345679"})

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/settings"
		assert "<h1>Redirecting...</h1>" in contenido

		datos_usuario=conexion_usuario.obtenerDatosCambioContrasenaUsuario("golden")

		assert datos_usuario_previo[0]==datos_usuario[0]
		assert datos_usuario_previo[1]==datos_usuario[1]

		contrasena_nueva=conexion_usuario.obtenerContrasenaUsuario("golden")

		assert contrasena_previa!=contrasena_nueva