def test_tabla_grupos_equipos_porra_vacia(conexion):

	conexion.c.execute("SELECT * FROM grupo_equipos_porra")

	assert not conexion.c.fetchall()