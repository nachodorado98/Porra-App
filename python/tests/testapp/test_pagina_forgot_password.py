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