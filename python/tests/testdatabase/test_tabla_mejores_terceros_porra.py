def test_tabla_mejores_terceros_porra_vacia(conexion):

	conexion.c.execute("SELECT * FROM mejores_terceros_porra")

	assert not conexion.c.fetchall()