from datetime import datetime, timedelta

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

def test_puede_ver_resultados_usuario_no_existe(conexion):

	assert not conexion.puedeVerResultados("nacho98")

def test_puede_ver_resultados_porra_no_completada(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	conexion.insertarEstadoPorraUsuario("nacho98")

	assert not conexion.puedeVerResultados("nacho98")

def test_puede_ver_resultados_porra_abierta(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	conexion.insertarEstadoPorraUsuario("nacho98")

	conexion.actualizarEstadoPorraUsuario("nacho98")

	assert not conexion.puedeVerResultados("nacho98")

def test_puede_ver_resultados_evento_no_iniciado(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	conexion.insertarEstadoPorraUsuario("nacho98")

	conexion.actualizarEstadoPorraUsuario("nacho98")

	fecha_anterior=(datetime.now()-timedelta(days=1)).strftime("%Y-%m-%d")

	conexion.insertarClaveValorMaestro("fecha_cierre_porra", fecha_anterior)

	assert not conexion.puedeVerResultados("nacho98")

def test_puede_ver_resultados(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	conexion.insertarEstadoPorraUsuario("nacho98")

	conexion.actualizarEstadoPorraUsuario("nacho98")

	fecha_anterior=(datetime.now()-timedelta(days=1)).strftime("%Y-%m-%d")

	conexion.insertarClaveValorMaestro("fecha_cierre_porra", fecha_anterior)

	conexion.c.execute("""INSERT INTO grupo_equipos_real
							VALUES ('A', 'seleccion-mexico', 1),
									('A', 'republica-checa', 2),
									('A', 'seleccion-republica-corea', 3),
									('A', 'seleccion-sudafrica', 4)""")

	conexion.confirmar()

	assert conexion.puedeVerResultados("nacho98")