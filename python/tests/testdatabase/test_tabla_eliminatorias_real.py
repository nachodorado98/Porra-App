def test_tabla_eliminatorias_real_vacia(conexion):

	conexion.c.execute("SELECT * FROM eliminatorias_real")

	assert not conexion.c.fetchall()

def test_obtener_eliminatorias_real_no_existen(conexion):

	assert not conexion.obtenerEliminatoriasReal()

def test_obtener_eliminatorias_real(conexion):

	conexion.c.execute("""INSERT INTO eliminatorias_real VALUES ('dieciseisavos', 'M73', 'seleccion-mexico', 'seleccion-espanola', 'seleccion-espanola')""")

	conexion.confirmar()

	eliminatorias_real=conexion.obtenerEliminatoriasReal()

	assert len(eliminatorias_real)==1

def test_obtener_eliminatorias_real_varios(conexion):

	conexion.c.execute("""INSERT INTO eliminatorias_real
							VALUES ('dieciseisavos', 'M73', 'seleccion-mexico', 'seleccion-espanola', 'seleccion-espanola'),
									('octavos', 'M80', 'seleccion-mexico', 'seleccion-espanola', 'seleccion-espanola'),
									('cuartos', 'M90', 'seleccion-mexico', 'seleccion-espanola', 'seleccion-espanola'),
									('semis', 'M100', 'seleccion-mexico', 'seleccion-espanola', 'seleccion-espanola'),
									('final', 'M104', 'seleccion-mexico', 'seleccion-espanola', 'seleccion-espanola')""")

	conexion.confirmar()

	eliminatorias_real=conexion.obtenerEliminatoriasReal()

	assert len(eliminatorias_real)==5