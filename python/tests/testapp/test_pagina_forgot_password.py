import pytest
from datetime import datetime, timedelta
from src.utilidades.utils import generarHashToken

def test_pagina_forgot_password(cliente):

	respuesta=cliente.get("/forgot_password")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Recuperar contraseña</h1>" in contenido

def test_pagina_forgot_password_solicitar_usuario_no_correo(cliente, conexion):

	respuesta=cliente.post("/forgot_password/solicitar", data={"correo":"micorreo@correo.es"}, follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert respuesta.request.path=="/forgot_password"
	assert '<div class="mensaje error">El correo introducido no existe</div>' in contenido

def test_pagina_forgot_password_solicitar_token_reciente_enviado(cliente, conexion_usuario):

	expires_at=datetime.now()+timedelta(minutes=30)

	conexion_usuario.insertarToken("nacho98", "token", expires_at)

	respuesta=cliente.post("/forgot_password/solicitar", data={"correo":"micorreo@correo.es"}, follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert respuesta.request.path=="/forgot_password"
	assert '<div class="mensaje error">Ya se ha enviado un enlace recientemente. Espera unos minutos antes de solicitar otro</div>' in contenido

def test_pagina_forgot_password_solicitar(cliente, conexion_usuario):

	respuesta=cliente.post("/forgot_password/solicitar", data={"correo":"micorreo@correo.es"}, follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert respuesta.request.path=="/"
	assert '<div class="mensaje correcto">El correo de recuperacion ha sido enviado</div>' in contenido

	conexion_usuario.c.execute("SELECT * FROM password_reset_tokens")

	tokens=conexion_usuario.c.fetchall()

	assert len(tokens)==1

	conexion_usuario.c.execute("SELECT * FROM password_reset_tokens WHERE Usado=False")

	tokens_no_usados=conexion_usuario.c.fetchall()

	assert len(tokens_no_usados)==1

def test_pagina_forgot_password_solicitar_token_no_reciente_enviado(cliente, conexion_usuario):

	expires_at=datetime.now()+timedelta(minutes=30)

	conexion_usuario.insertarToken("nacho98", "token", expires_at)

	conexion_usuario.c.execute("""UPDATE password_reset_tokens
									SET Created_At=CURRENT_TIMESTAMP-INTERVAL '10 minutes'""")

	conexion_usuario.confirmar()

	respuesta=cliente.post("/forgot_password/solicitar", data={"correo":"micorreo@correo.es"}, follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert respuesta.request.path=="/"
	assert '<div class="mensaje correcto">El correo de recuperacion ha sido enviado</div>' in contenido

	conexion_usuario.c.execute("SELECT * FROM password_reset_tokens")

	tokens=conexion_usuario.c.fetchall()

	assert len(tokens)==2

	conexion_usuario.c.execute("SELECT * FROM password_reset_tokens WHERE Usado=False")

	tokens_no_usados=conexion_usuario.c.fetchall()

	assert len(tokens_no_usados)==1

def test_pagina_forgot_password_reset_password_token_no_existe(cliente, conexion):

	respuesta=cliente.get("/forgot_password/reset_password/token", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert respuesta.request.path=="/forgot_password"
	assert '<div class="mensaje error">El enlace de recuperación no es válido</div>' in contenido

def test_pagina_forgot_password_reset_password_token_usado(cliente, conexion_usuario):

	expires_at=datetime.now()+timedelta(minutes=30)

	hash_token=generarHashToken("token123456")

	conexion_usuario.insertarToken("nacho98", hash_token, expires_at)

	conexion_usuario.c.execute("""UPDATE password_reset_tokens
									SET Usado=True""")

	conexion_usuario.confirmar()

	respuesta=cliente.get("/forgot_password/reset_password/token123456", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert respuesta.request.path=="/forgot_password"
	assert '<div class="mensaje error">Este enlace ya ha sido utilizado</div>' in contenido

def test_pagina_forgot_password_reset_password_token_expirado(cliente, conexion_usuario):

	expires_at=datetime.now()+timedelta(minutes=30)

	hash_token=generarHashToken("token123456")

	conexion_usuario.insertarToken("nacho98", hash_token, expires_at)

	conexion_usuario.c.execute("""UPDATE password_reset_tokens
									SET Expires_At=CURRENT_TIMESTAMP-INTERVAL '10 minutes'""")

	conexion_usuario.confirmar()

	respuesta=cliente.get("/forgot_password/reset_password/token123456", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert respuesta.request.path=="/forgot_password"
	assert '<div class="mensaje error">Este enlace ha caducado</div>' in contenido

def test_pagina_forgot_password_reset_password(cliente, conexion_usuario):

	expires_at=datetime.now()+timedelta(minutes=30)

	hash_token=generarHashToken("token123456")

	conexion_usuario.insertarToken("nacho98", hash_token, expires_at)

	respuesta=cliente.get("/forgot_password/reset_password/token123456", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert '<h1>Cambiar contraseña</h1>' in contenido

def test_pagina_forgot_password_change_password_data_no_valida(cliente, conexion_usuario):

	expires_at=datetime.now()+timedelta(minutes=30)

	hash_token=generarHashToken("token123456")

	conexion_usuario.insertarToken("nacho98", hash_token, expires_at)

	respuesta=cliente.post("/forgot_password/change_password/token123456", data={"data":"data"}, follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert respuesta.request.path=="/forgot_password/reset_password/token123456"
	assert '<div class="mensaje error">Debes rellenar todos los campos</div>' in contenido

def test_pagina_forgot_password_change_password_contrasena_nueva_introducida_distinta_repetir_contrasena_introducida(cliente, conexion_usuario):

	expires_at=datetime.now()+timedelta(minutes=30)

	hash_token=generarHashToken("token123456")

	conexion_usuario.insertarToken("nacho98", hash_token, expires_at)

	respuesta=cliente.post("/forgot_password/change_password/token123456", data={"nueva_contrasena":"12345678", "repetir_contrasena":"12345679"}, follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert respuesta.request.path=="/forgot_password/reset_password/token123456"
	assert '<div class="mensaje error">Las contraseñas no coinciden</div>' in contenido

@pytest.mark.parametrize(["contrasena"],
    [("clave",),("PASSWD",),("1234567",),("Abcdefg",),("A1b2C3d",),("abcd",),("1234",),
     ("Ab CdEfGhI",),("Ab!CdEfGhI ",),(" Ab!CdEfGhI",),("AIJKLMN",),("Ab@cdE2",),
     ("Ab@cdEf1 G",),("Abcd12 34!",)]
)
def test_pagina_forgot_password_change_password_contrasena_no_valida(cliente, conexion_usuario, contrasena):

	expires_at=datetime.now()+timedelta(minutes=30)

	hash_token=generarHashToken("token123456")

	conexion_usuario.insertarToken("nacho98", hash_token, expires_at)

	respuesta=cliente.post("/forgot_password/change_password/token123456", data={"nueva_contrasena":contrasena, "repetir_contrasena":contrasena}, follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert respuesta.request.path=="/forgot_password/reset_password/token123456"
	assert '<div class="mensaje error">La contraseña debe tener al menos 8 caracteres y no contener espacios</div>' in contenido

def test_pagina_forgot_password_change_password_token_no_existe(cliente, conexion):

	respuesta=cliente.post("/forgot_password/change_password/token123456", data={"nueva_contrasena":"12345678", "repetir_contrasena":"12345678"}, follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert respuesta.request.path=="/forgot_password"
	assert '<div class="mensaje error">El enlace de recuperación no es válido</div>' in contenido

def test_pagina_forgot_password_change_password_token_usado(cliente, conexion_usuario):

	expires_at=datetime.now()+timedelta(minutes=30)

	hash_token=generarHashToken("token123456")

	conexion_usuario.insertarToken("nacho98", hash_token, expires_at)

	conexion_usuario.c.execute("""UPDATE password_reset_tokens
									SET Usado=True""")

	conexion_usuario.confirmar()

	respuesta=cliente.post("/forgot_password/change_password/token123456", data={"nueva_contrasena":"12345678", "repetir_contrasena":"12345678"}, follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert respuesta.request.path=="/forgot_password"
	assert '<div class="mensaje error">Este enlace ya ha sido utilizado</div>' in contenido

def test_pagina_forgot_password_change_password_token_expirado(cliente, conexion_usuario):

	expires_at=datetime.now()+timedelta(minutes=30)

	hash_token=generarHashToken("token123456")

	conexion_usuario.insertarToken("nacho98", hash_token, expires_at)

	conexion_usuario.c.execute("""UPDATE password_reset_tokens
									SET Expires_At=CURRENT_TIMESTAMP-INTERVAL '10 minutes'""")

	conexion_usuario.confirmar()

	respuesta=cliente.post("/forgot_password/change_password/token123456", data={"nueva_contrasena":"12345678", "repetir_contrasena":"12345678"}, follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert respuesta.request.path=="/forgot_password"
	assert '<div class="mensaje error">Este enlace ha caducado</div>' in contenido

def test_pagina_forgot_password_change_password_contrasena_igual_anterior(cliente, conexion_usuario):

	expires_at=datetime.now()+timedelta(minutes=30)

	hash_token=generarHashToken("token123456")

	conexion_usuario.insertarToken("nacho98", hash_token, expires_at)

	respuesta=cliente.post("/forgot_password/change_password/token123456", data={"nueva_contrasena":"Ab!CdEfGhIJK3LMN", "repetir_contrasena":"Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert respuesta.request.path=="/forgot_password/reset_password/token123456"
	assert '<div class="mensaje error">La nueva contraseña no puede ser igual a la anterior</div>' in contenido

@pytest.mark.parametrize(["cambios", "ultimo_cambio"],
	[
		(0, datetime.now()-timedelta(hours=48)),
		(2, datetime.now()-timedelta(hours=48)),
		(2, datetime.now()-timedelta(hours=24))
	]
)
def test_pagina_forgot_password_change_password(cliente, conexion_usuario, cambios, ultimo_cambio):

	conexion_usuario.c.execute(f"UPDATE usuarios SET Cambios_Contrasena={cambios}, Ultimo_Cambio_Contrasena='{ultimo_cambio}'")

	conexion_usuario.confirmar()

	expires_at=datetime.now()+timedelta(minutes=30)

	hash_token=generarHashToken("token123456")

	conexion_usuario.insertarToken("nacho98", hash_token, expires_at)

	contrasena_previa=conexion_usuario.obtenerContrasenaUsuario("nacho98")

	respuesta=cliente.post("/forgot_password/change_password/token123456", data={"nueva_contrasena":"12345678", "repetir_contrasena":"12345678"}, follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert respuesta.request.path=="/"
	assert '<div class="mensaje correcto">La contraseña se ha cambiado correctamente</div>' in contenido

	conexion_usuario.c.execute("SELECT * FROM password_reset_tokens WHERE Usado=True")

	tokens_usados=conexion_usuario.c.fetchall()

	assert len(tokens_usados)==1

	datos_usuario=conexion_usuario.obtenerDatosCambioContrasenaUsuario("nacho98")

	assert datos_usuario[0]==cambios+1
	assert datos_usuario[1].strftime("%Y-%m-%d")==datetime.now().strftime("%Y-%m-%d")

	contrasena_nueva=conexion_usuario.obtenerContrasenaUsuario("nacho98")

	assert contrasena_previa!=contrasena_nueva