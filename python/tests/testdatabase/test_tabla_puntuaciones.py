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

def test_actualizar_puntuacion_usuario_no_existe_usuario(conexion):

	assert not conexion.existe_usuario("nacho98")

	conexion.actualizarPuntuacionUsuario("nacho98", 1, 1, 1)

	assert not conexion.existe_usuario("nacho98")

def test_actualizar_puntuacion_usuario_otro_usuario(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	conexion.insertarPuntuacionUsuario("nacho98")

	conexion.actualizarPuntuacionUsuario("nacho", 1, 1, 1)

	conexion.c.execute("SELECT Puntos_Grupos, Puntos_Mejores_Terceros, Puntos_Eliminatorias, Puntos_Total FROM puntuaciones")

	puntuacion=conexion.c.fetchone()

	assert puntuacion["puntos_grupos"]==0
	assert puntuacion["puntos_mejores_terceros"]==0
	assert puntuacion["puntos_eliminatorias"]==0
	assert puntuacion["puntos_total"]==0

def test_actualizar_puntuacion_usuario(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	conexion.insertarPuntuacionUsuario("nacho98")

	conexion.actualizarPuntuacionUsuario("nacho98", 1, 1, 1)

	conexion.c.execute("SELECT Puntos_Grupos, Puntos_Mejores_Terceros, Puntos_Eliminatorias, Puntos_Total FROM puntuaciones")

	puntuacion=conexion.c.fetchone()

	assert puntuacion["puntos_grupos"]==1
	assert puntuacion["puntos_mejores_terceros"]==1
	assert puntuacion["puntos_eliminatorias"]==1
	assert puntuacion["puntos_total"]==3