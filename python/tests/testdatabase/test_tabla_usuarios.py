import pytest

def test_tabla_usuarios_vacia(conexion):

	conexion.c.execute("SELECT * FROM usuarios")

	assert not conexion.c.fetchall()

@pytest.mark.parametrize(["usuario", "correo", "contrasena", "nombre", "apellido", "codigo_liga"],
	[
		("nacho98", "nacho@correo", "1234", "nacho", "dorado", "C4N5VT"),
		("nacho948", "correo", "12vvnvvb34", "naegcho", "dordado", "5BN52O"),
		("nacho", "micorreo@correo.es", "12vvn&fvvb34", "nachitoo", "dordado", "1985M9")
	]
)
def test_insertar_usuario(conexion, usuario, correo, contrasena, nombre, apellido, codigo_liga):

	conexion.insertarCodigoLiga(codigo_liga)

	conexion.insertarUsuario(usuario, correo, contrasena, nombre, apellido, codigo_liga)

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	assert len(usuarios)==1

@pytest.mark.parametrize(["numero_usuarios"],
	[(2,),(22,),(5,),(13,),(25,)]
)
def test_insertar_usuarios(conexion, numero_usuarios):

	conexion.insertarCodigoLiga("C4N5VT")

	for numero in range(numero_usuarios):

		conexion.insertarUsuario(f"nacho{numero}", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	assert len(usuarios)==numero_usuarios

def test_existe_usuario_no_existen(conexion):

	assert not conexion.existe_usuario("nacho98")

def test_existe_usuario_existen_no_existente(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	assert not conexion.existe_usuario("nacho99")

def test_existe_usuario_existe(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	assert conexion.existe_usuario("nacho98")