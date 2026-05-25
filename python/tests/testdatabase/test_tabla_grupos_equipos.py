def test_tabla_grupos_equipos_llena(conexion):

	conexion.c.execute("SELECT * FROM grupo_equipos")

	assert conexion.c.fetchall()

def test_tabla_obtener_grupos_equipos(conexion):

	grupos_equipos=conexion.obtenerGruposEquipos()

	assert len(grupos_equipos)==48