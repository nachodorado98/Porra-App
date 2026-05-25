def test_tabla_grupos_equipos_real_vacia(conexion):

	conexion.c.execute("SELECT * FROM grupo_equipos_real")

	assert not conexion.c.fetchall()