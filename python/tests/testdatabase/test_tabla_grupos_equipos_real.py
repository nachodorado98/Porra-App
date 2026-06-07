def test_tabla_grupos_equipos_real_vacia(conexion):

	conexion.c.execute("SELECT * FROM grupo_equipos_real")

	assert not conexion.c.fetchall()

def test_obtener_grupos_real_grupos_no_existen(conexion):

	assert not conexion.obtenerGruposReal()

def test_obtener_grupos_real_grupos(conexion):

	conexion.c.execute("""INSERT INTO grupo_equipos_real VALUES ('A', 'seleccion-mexico', 1)""")

	conexion.confirmar()

	grupos_real=conexion.obtenerGruposReal()

	assert len(grupos_real)==1

def test_obtener_grupos_real_grupos_varios(conexion):

	conexion.c.execute("""INSERT INTO grupo_equipos_real
							VALUES ('A', 'seleccion-mexico', 1),
									('A', 'republica-checa', 2),
									('A', 'seleccion-republica-corea', 3),
									('A', 'seleccion-sudafrica', 4)""")

	conexion.confirmar()

	grupos_real=conexion.obtenerGruposReal()

	assert len(grupos_real)==4