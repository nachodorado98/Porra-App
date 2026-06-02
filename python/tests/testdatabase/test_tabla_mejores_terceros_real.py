def test_tabla_mejores_terceros_real_vacia(conexion):

	conexion.c.execute("SELECT * FROM mejores_terceros_real")

	assert not conexion.c.fetchall()