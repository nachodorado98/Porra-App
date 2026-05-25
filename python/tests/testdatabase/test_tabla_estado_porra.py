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

	