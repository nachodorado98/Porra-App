def test_tabla_puntuaciones_vacia(conexion):

	conexion.c.execute("SELECT * FROM puntuaciones")

	assert not conexion.c.fetchall()

def test_insertar_puntuaciones(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	conexion.insertarPuntuacionUsuario("nacho98")

	conexion.c.execute("SELECT * FROM puntuaciones")

	puntuacion=conexion.c.fetchall()

	assert len(puntuacion)==1