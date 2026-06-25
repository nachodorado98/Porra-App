from datetime import datetime, timedelta

def test_tabla_password_reset_tokens_vacia(conexion):

	conexion.c.execute("SELECT * FROM password_reset_tokens")

	assert not conexion.c.fetchall()

def test_insertar_token_password_reset_tokens(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	expires_at=datetime.now()+timedelta(minutes=30)

	conexion.insertarToken("nacho98", "token", expires_at)

	conexion.c.execute("SELECT * FROM password_reset_tokens")

	tokens=conexion.c.fetchall()

	assert len(tokens)==1

def test_obtener_token_no_existe(conexion):

	assert conexion.obtenerToken("token") is None

def test_obtener_correo_usuario_existen(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	expires_at=datetime.now()+timedelta(minutes=30)

	conexion.insertarToken("nacho98", "token", expires_at)

	assert conexion.obtenerToken("token")

def test_actualizar_token_no_existe(conexion):

	assert conexion.obtenerToken("token") is None

	conexion.actualizarToken("token")

	assert conexion.obtenerToken("token") is None

def test_actualizar_token(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	expires_at=datetime.now()+timedelta(minutes=30)

	conexion.insertarToken("nacho98", "token", expires_at)

	id_token, usuario, token, expires_at, usado=conexion.obtenerToken("token")

	assert not usado

	conexion.actualizarToken("token")

	id_token, usuario, token, expires_at, usado=conexion.obtenerToken("token")

	assert usado