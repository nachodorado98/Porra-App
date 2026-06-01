import pytest

def test_tabla_mejores_terceros_porra_vacia(conexion):

	conexion.c.execute("SELECT * FROM mejores_terceros_porra")

	assert not conexion.c.fetchall()

@pytest.mark.parametrize(["grupo", "equipo", "orden"],
	[("A", "seleccion-espanola", 1), ("B", "seleccion-espanola", 8), ("H", "seleccion-uruguay", 5), ("C", "cabo-verde", 3)]
)
def test_insertar_equipo_mejor_tercero_porra_usuario(conexion, grupo, equipo, orden):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	conexion.insertarEquipoMejorTerceroPorraUsuario("nacho98", grupo, equipo, orden)

	conexion.c.execute("SELECT * FROM mejores_terceros_porra")

	equipos_mejores_terceros=conexion.c.fetchall()

	assert len(equipos_mejores_terceros)==1

def test_insertar_equipo_mejor_tercero_porra_usuario_varios(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	for posicion, grupo_equipo in enumerate([("A", "seleccion-espanola"), ("B", "seleccion-espanola"), ("H", "seleccion-uruguay"), ("C", "cabo-verde")], start=1):

		conexion.insertarEquipoMejorTerceroPorraUsuario("nacho98", grupo_equipo[0], grupo_equipo[1], posicion)

	conexion.c.execute("SELECT * FROM mejores_terceros_porra")

	equipos_mejores_terceros=conexion.c.fetchall()

	assert len(equipos_mejores_terceros)==4

def test_insertar_equipos_mejor_tercero_porra_usuario(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	conexion.insertarEquipoMejoresTercerosPorraUsuario("nacho98", [("A", "seleccion-espanola"), ("B", "seleccion-espanola"), ("H", "seleccion-uruguay"), ("C", "cabo-verde")])

	conexion.c.execute("SELECT Grupo, Equipo_Id, Orden FROM mejores_terceros_porra ORDER BY Orden ASC")

	equipos_mejores_terceros=conexion.c.fetchall()

	assert len(equipos_mejores_terceros)==4

def test_obtener_mejores_terceros_usuario_usuario_no_existe(conexion):

	assert not conexion.obtenerMejoresTercerosUsuario("nacho98")

def test_obtener_mejores_terceros_usuario_porra_grupos_no_existe(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	assert not conexion.obtenerMejoresTercerosUsuario("nacho98")

def test_obtener_mejores_terceros_usuario_otro_usuario(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	conexion.insertarEquipoMejoresTercerosPorraUsuario("nacho98", [("A", "seleccion-espanola"), ("B", "seleccion-espanola"), ("H", "seleccion-uruguay"), ("C", "cabo-verde")])

	assert not conexion.obtenerMejoresTercerosUsuario("nacho")

def  test_obtener_mejores_terceros_usuario(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	conexion.insertarEquipoMejoresTercerosPorraUsuario("nacho98", [("A", "seleccion-espanola"), ("B", "seleccion-espanola"), ("H", "seleccion-uruguay"), ("C", "cabo-verde")])

	mejores_terceros=conexion.obtenerMejoresTercerosUsuario("nacho98")

	assert len(mejores_terceros)==4

	for mejor_tercero in mejores_terceros:

		assert mejor_tercero[-1]==3

def test_reiniciar_mejores_terceros_porra_usuario_usuario_no_existe(conexion):

	conexion.c.execute("SELECT * FROM mejores_terceros_porra")

	assert not conexion.c.fetchall()

	conexion.reiniciarMejoresTercerosPorraUsuario("nacho98")

	conexion.c.execute("SELECT * FROM mejores_terceros_porra")

	assert not conexion.c.fetchall()

def test_reiniciar_mejores_terceros_porra_usuario_porra_grupos_no_existe(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	conexion.c.execute("SELECT * FROM mejores_terceros_porra")

	assert not conexion.c.fetchall()

	conexion.reiniciarMejoresTercerosPorraUsuario("nacho98")

	conexion.c.execute("SELECT * FROM mejores_terceros_porra")

	assert not conexion.c.fetchall()

def test_reiniciar_mejores_terceros_porra_usuario_otro_usuario(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	conexion.insertarEquipoMejoresTercerosPorraUsuario("nacho98", [("A", "seleccion-espanola"), ("B", "seleccion-espanola"), ("H", "seleccion-uruguay"), ("C", "cabo-verde")])

	conexion.c.execute("SELECT * FROM mejores_terceros_porra")

	assert conexion.c.fetchall()

	conexion.reiniciarMejoresTercerosPorraUsuario("nacho")

	conexion.c.execute("SELECT * FROM mejores_terceros_porra")

	assert conexion.c.fetchall()

def  test_reiniciar_mejores_terceros_porra_usuario(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	conexion.insertarEquipoMejoresTercerosPorraUsuario("nacho98", [("A", "seleccion-espanola"), ("B", "seleccion-espanola"), ("H", "seleccion-uruguay"), ("C", "cabo-verde")])

	conexion.c.execute("SELECT * FROM mejores_terceros_porra")

	assert conexion.c.fetchall()

	conexion.reiniciarMejoresTercerosPorraUsuario("nacho98")

	conexion.c.execute("SELECT * FROM mejores_terceros_porra")

	assert not conexion.c.fetchall()