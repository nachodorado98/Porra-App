import pytest

def test_tabla_eliminatorias_porra_vacia(conexion):

	conexion.c.execute("SELECT * FROM eliminatorias_porra")

	assert not conexion.c.fetchall()

@pytest.mark.parametrize(["ronda", "partido", "equipo_1_id", "equipo_2_id", "ganador_id"],
	[
		("dieciseisavos", "M74", "seleccion-espanola", "seleccion-uruguay", "seleccion-espanola"),
		("dieciseisavos", "M73", "seleccion-mexico", "seleccion-alemania", "seleccion-alemania"),
		("cuartos", "M90", "seleccion-brasil", "seleccion-holanda", "seleccion-brasil"),
		("semis", "M100", "seleccion-espanola", "seleccion-argentina", "seleccion-espanola")
	]
)
def test_insertar_partido_eliminatoria_porra_usuario(conexion, ronda, partido, equipo_1_id, equipo_2_id, ganador_id):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	conexion.insertarPartidoEliminatoriaPorraUsuario("nacho98", ronda, partido, equipo_1_id, equipo_2_id, ganador_id)

	conexion.c.execute("SELECT * FROM eliminatorias_porra")

	partidos_eliminatorias=conexion.c.fetchall()

	assert len(partidos_eliminatorias)==1

def test_insertar_partido_eliminatoria_porra_usuario_varios(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	partidos=[("dieciseisavos", "M74", "seleccion-espanola", "seleccion-uruguay", "seleccion-espanola"),
				("dieciseisavos", "M73", "seleccion-mexico", "seleccion-alemania", "seleccion-alemania"),
				("cuartos", "M90", "seleccion-brasil", "seleccion-holanda", "seleccion-brasil"),
				("semis", "M100", "seleccion-espanola", "seleccion-argentina", "seleccion-espanola")]

	for partido in partidos:

		conexion.insertarPartidoEliminatoriaPorraUsuario("nacho98", partido[0], partido[1], partido[2], partido[3], partido[4])

	conexion.c.execute("SELECT * FROM eliminatorias_porra")

	partidos_eliminatorias=conexion.c.fetchall()

	assert len(partidos_eliminatorias)==4

def test_insertar_partidos_eliminatorias_porra_usuario(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	partidos=[("dieciseisavos", "M74", "seleccion-espanola", "seleccion-uruguay", "seleccion-espanola"),
				("dieciseisavos", "M73", "seleccion-mexico", "seleccion-alemania", "seleccion-alemania"),
				("cuartos", "M90", "seleccion-brasil", "seleccion-holanda", "seleccion-brasil"),
				("semis", "M100", "seleccion-espanola", "seleccion-argentina", "seleccion-espanola")]

	conexion.insertarPartidosEliminatoriasPorraUsuario("nacho98", partidos)

	conexion.c.execute("SELECT * FROM eliminatorias_porra")

	partidos_eliminatorias=conexion.c.fetchall()

	assert len(partidos_eliminatorias)==4

def test_reiniciar_eliminatorias_porra_usuario_usuario_no_existe(conexion):

	conexion.c.execute("SELECT * FROM eliminatorias_porra")

	assert not conexion.c.fetchall()

	conexion.reiniciarEliminatoriasPorraUsuario("nacho98")

	conexion.c.execute("SELECT * FROM eliminatorias_porra")

	assert not conexion.c.fetchall()

def test_reiniciar_eliminatorias_porra_usuario_porra_eliminatorias_no_existe(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	conexion.c.execute("SELECT * FROM eliminatorias_porra")

	assert not conexion.c.fetchall()

	conexion.reiniciarEliminatoriasPorraUsuario("nacho98")

	conexion.c.execute("SELECT * FROM eliminatorias_porra")

	assert not conexion.c.fetchall()

def test_reiniciar_eliminatorias_porra_usuario_otro_usuario(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	partidos=[("dieciseisavos", "M74", "seleccion-espanola", "seleccion-uruguay", "seleccion-espanola"),
				("dieciseisavos", "M73", "seleccion-mexico", "seleccion-alemania", "seleccion-alemania"),
				("cuartos", "M90", "seleccion-brasil", "seleccion-holanda", "seleccion-brasil"),
				("semis", "M100", "seleccion-espanola", "seleccion-argentina", "seleccion-espanola")]

	conexion.insertarPartidosEliminatoriasPorraUsuario("nacho98", partidos)

	conexion.c.execute("SELECT * FROM eliminatorias_porra")

	assert conexion.c.fetchall()

	conexion.reiniciarEliminatoriasPorraUsuario("nacho")

	conexion.c.execute("SELECT * FROM eliminatorias_porra")

	assert conexion.c.fetchall()

def  test_reiniciar_eliminatorias_porra_usuario(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	partidos=[("dieciseisavos", "M74", "seleccion-espanola", "seleccion-uruguay", "seleccion-espanola"),
				("dieciseisavos", "M73", "seleccion-mexico", "seleccion-alemania", "seleccion-alemania"),
				("cuartos", "M90", "seleccion-brasil", "seleccion-holanda", "seleccion-brasil"),
				("semis", "M100", "seleccion-espanola", "seleccion-argentina", "seleccion-espanola")]

	conexion.insertarPartidosEliminatoriasPorraUsuario("nacho98", partidos)

	conexion.c.execute("SELECT * FROM eliminatorias_porra")

	assert conexion.c.fetchall()

	conexion.reiniciarEliminatoriasPorraUsuario("nacho98")

	conexion.c.execute("SELECT * FROM eliminatorias_porra")

	assert not conexion.c.fetchall()