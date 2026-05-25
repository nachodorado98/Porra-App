def test_tabla_estado_porra_vacia(conexion):

	conexion.c.execute("SELECT * FROM estado_porra")

	assert not conexion.c.fetchall()

def test_insertar_estado_porra(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	conexion.insertarEstadoPorraUsuario("nacho98")

	conexion.c.execute("SELECT * FROM estado_porra")

	estado_porras=conexion.c.fetchall()

	assert len(estado_porras)==1

def test_actualizar_estado_porra_grupos_no_existe_usuario(conexion):

	conexion.c.execute("SELECT * FROM estado_porra")

	assert not conexion.c.fetchall()

	conexion.actualizarEstadoPorraGruposUsuario("nacho98")

	conexion.c.execute("SELECT * FROM estado_porra WHERE usuario='nacho98'")

	assert not conexion.c.fetchall()

def test_actualizar_estado_porra_grupos_otro_usuario(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	conexion.insertarEstadoPorraUsuario("nacho98")

	conexion.c.execute("SELECT Grupos_Completados FROM estado_porra WHERE usuario='nacho98'")

	assert not conexion.c.fetchone()["grupos_completados"]

	conexion.actualizarEstadoPorraGruposUsuario("nacho")

	conexion.c.execute("SELECT Grupos_Completados FROM estado_porra WHERE usuario='nacho98'")

	assert not conexion.c.fetchone()["grupos_completados"]

def test_actualizar_estado_porra_grupos(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	conexion.insertarEstadoPorraUsuario("nacho98")

	conexion.c.execute("SELECT Grupos_Completados FROM estado_porra WHERE usuario='nacho98'")

	assert not conexion.c.fetchone()["grupos_completados"]

	conexion.actualizarEstadoPorraGruposUsuario("nacho98")

	conexion.c.execute("SELECT Grupos_Completados FROM estado_porra WHERE usuario='nacho98'")

	assert conexion.c.fetchone()["grupos_completados"]