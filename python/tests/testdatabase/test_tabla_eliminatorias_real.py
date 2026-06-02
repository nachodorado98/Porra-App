def test_tabla_eliminatorias_real_vacia(conexion):

	conexion.c.execute("SELECT * FROM eliminatorias_real")

	assert not conexion.c.fetchall()