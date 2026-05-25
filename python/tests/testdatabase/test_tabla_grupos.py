def test_tabla_grupos_llena(conexion):

	conexion.c.execute("SELECT * FROM grupos")

	assert conexion.c.fetchall()