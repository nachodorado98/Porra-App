def test_tabla_mejores_terceros_real_vacia(conexion):

	conexion.c.execute("SELECT * FROM mejores_terceros_real")

	assert not conexion.c.fetchall()

def test_obtener_mejores_terceros_real_no_existen(conexion):

	assert not conexion.obtenerMejoresTercerosReal()

def test_obtener_mejores_terceros_real(conexion):

	conexion.c.execute("""INSERT INTO mejores_terceros_real VALUES ('A', 'seleccion-mexico', 1)""")

	conexion.confirmar()

	mejores_terceros_real=conexion.obtenerMejoresTercerosReal()

	assert len(mejores_terceros_real)==1

def test_obtener_mejores_terceros_real_varios(conexion):

	conexion.c.execute("""INSERT INTO mejores_terceros_real
							VALUES ('A', 'seleccion-mexico', 1),
									('B', 'seleccion-bosnia-herzegovina', 2),
									('C', 'seleccion-escocia', 3),
									('D', 'seleccion-paraguay', 4)""")

	conexion.confirmar()

	mejores_terceros_real=conexion.obtenerMejoresTercerosReal()

	assert len(mejores_terceros_real)==4