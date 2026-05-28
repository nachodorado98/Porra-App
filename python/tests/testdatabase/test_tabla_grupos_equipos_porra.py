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

def test_obtener_terceros_grupos_usuario_usuario_no_existe(conexion):

	assert not conexion.obtenerTercerosGruposUsuario("nacho98")

def test_obtener_terceros_grupos_usuario_porra_grupos_no_existe(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	assert not conexion.obtenerTercerosGruposUsuario("nacho98")

def test_obtener_terceros_grupos_usuario_otro_usuario(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	conexion.insertarEquipoGruposPorraUsuario("nacho98", "H", ['seleccion-espanola', 'seleccion-uruguay', 'seleccion-arabia-saudi', 'cabo-verde'])

	assert not conexion.obtenerTercerosGruposUsuario("nacho")

def test_obtener_terceros_grupos_usuario(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	conexion.insertarEquipoGruposPorraUsuario("nacho98", "H", ['seleccion-espanola', 'seleccion-uruguay', 'seleccion-arabia-saudi', 'cabo-verde'])

	terceros_grupos=conexion.obtenerTercerosGruposUsuario("nacho98")

	assert len(terceros_grupos)==1

def test_obtener_terceros_grupos_usuario_varios(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	conexion.insertarEquipoGruposPorraUsuario("nacho98", "A", ['seleccion-mexico', 'republica-checa', 'seleccion-republica-corea', 'seleccion-sudafrica'])

	conexion.insertarEquipoGruposPorraUsuario("nacho98", "C", ['seleccion-brasil', 'seleccion-marruecos', 'seleccion-escocia', 'haiti'])

	conexion.insertarEquipoGruposPorraUsuario("nacho98", "D", ['seleccion-estados-unidos', 'seleccion-turquia', 'seleccion-paraguay', 'seleccion-australia'])

	conexion.insertarEquipoGruposPorraUsuario("nacho98", "H", ['seleccion-espanola', 'seleccion-uruguay', 'seleccion-arabia-saudi', 'cabo-verde'])

	terceros_grupos=conexion.obtenerTercerosGruposUsuario("nacho98")

	assert len(terceros_grupos)==4

	for tercero_grupo in terceros_grupos:

		assert tercero_grupo[1] in ('seleccion-republica-corea', 'seleccion-escocia', 'seleccion-paraguay', 'seleccion-arabia-saudi')

def test_reiniciar_grupos_porra_usuario_usuario_no_existe(conexion):

	conexion.c.execute("SELECT * FROM grupo_equipos_porra")

	assert not conexion.c.fetchall()

	conexion.reiniciarGruposPorraUsuario("nacho98")

	conexion.c.execute("SELECT * FROM grupo_equipos_porra")

	assert not conexion.c.fetchall()

def test_reiniciar_grupos_porra_usuario_porra_grupos_no_existe(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	conexion.c.execute("SELECT * FROM grupo_equipos_porra")

	assert not conexion.c.fetchall()

	conexion.reiniciarGruposPorraUsuario("nacho98")

	conexion.c.execute("SELECT * FROM grupo_equipos_porra")

	assert not conexion.c.fetchall()

def test_reiniciar_grupos_porra_usuario_otro_usuario(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	conexion.insertarEquipoGruposPorraUsuario("nacho98", "H", ['seleccion-espanola', 'seleccion-uruguay', 'seleccion-arabia-saudi', 'cabo-verde'])

	conexion.c.execute("SELECT * FROM grupo_equipos_porra")

	assert conexion.c.fetchall()

	conexion.reiniciarGruposPorraUsuario("nacho")

	conexion.c.execute("SELECT * FROM grupo_equipos_porra")

	assert conexion.c.fetchall()

def  test_reiniciar_grupos_porra_usuario(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	conexion.insertarEquipoGruposPorraUsuario("nacho98", "H", ['seleccion-espanola', 'seleccion-uruguay', 'seleccion-arabia-saudi', 'cabo-verde'])

	conexion.c.execute("SELECT * FROM grupo_equipos_porra")

	assert conexion.c.fetchall()

	conexion.reiniciarGruposPorraUsuario("nacho98")

	conexion.c.execute("SELECT * FROM grupo_equipos_porra")

	assert not conexion.c.fetchall()