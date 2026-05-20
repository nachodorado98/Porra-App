def test_tabla_equipos_llena(conexion):

	conexion.c.execute("SELECT * FROM equipos")

	assert conexion.c.fetchall()