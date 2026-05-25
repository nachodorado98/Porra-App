import pytest

def test_tabla_grupos_equipos_porra_vacia(conexion):

	conexion.c.execute("SELECT * FROM grupo_equipos_porra")

	assert not conexion.c.fetchall()

@pytest.mark.parametrize(["grupo", "equipo", "posicion"],
	[("A", "seleccion-espanola", 1), ("B", "seleccion-espanola", 2), ("H", "seleccion-uruguay", 4), ("C", "cabo-verde", 3)]
)
def test_insertar_equipo_grupo_porra_usuario(conexion, grupo, equipo, posicion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	conexion.insertarEquipoGrupoPorraUsuario("nacho98", grupo, equipo, posicion)

	conexion.c.execute("SELECT * FROM grupo_equipos_porra")

	equipos_grupos=conexion.c.fetchall()

	assert len(equipos_grupos)==1

def test_insertar_equipo_grupo_porra_usuario_varios(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	for posicion, equipo in enumerate(['seleccion-espanola', 'seleccion-uruguay', 'seleccion-arabia-saudi', 'cabo-verde'], start=1):

		conexion.insertarEquipoGrupoPorraUsuario("nacho98", "H", equipo, posicion)

	conexion.c.execute("SELECT * FROM grupo_equipos_porra")

	equipos_grupos=conexion.c.fetchall()

	assert len(equipos_grupos)==4

def test_insertar_equipos_grupo_porra_usuario(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	conexion.insertarEquipoGruposPorraUsuario("nacho98", "H", ['seleccion-espanola', 'seleccion-uruguay', 'seleccion-arabia-saudi', 'cabo-verde'])

	conexion.c.execute("SELECT Grupo, Equipo_Id, Posicion FROM grupo_equipos_porra ORDER BY Posicion ASC")

	equipos_grupos=conexion.c.fetchall()

	assert len(equipos_grupos)==4
