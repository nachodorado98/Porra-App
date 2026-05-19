import pytest

def test_tabla_codigos_vacia(conexion):

	conexion.c.execute("SELECT * FROM codigos")

	assert not conexion.c.fetchall()

@pytest.mark.parametrize(["codigo"],
	[("C4N5VT",),("5BN52O",),("1985M9",),("F779H9",)]
)
def test_insertar_codigo_liga(conexion, codigo):

	conexion.insertarCodigoLiga(codigo)

	conexion.c.execute("SELECT * FROM codigos")

	codigos=conexion.c.fetchall()

	assert len(codigos)==1

def test_insertar_codigos_ligas(conexion):

	for codigo in ["C4N5VT", "5BN52O", "1985M9", "F779H9"]:

		conexion.insertarCodigoLiga(codigo)

	conexion.c.execute("SELECT * FROM codigos")

	codigos=conexion.c.fetchall()

	assert len(codigos)==4

def test_obtener_codigos_ligas_no_existen(conexion):

	assert not conexion.obtenerCodigosLigas()

def test_obtener_codigos_ligas_existen(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	assert conexion.obtenerCodigosLigas()

def test_existe_codigo_liga_no_existen(conexion):

	assert not conexion.existe_codigo_liga("C4N5VT")

def test_existe_codigo_liga_no_existe(conexion):

	conexion.insertarCodigoLiga("otro")

	assert not conexion.existe_codigo_liga("C4N5VT")

def test_existe_codigo_liga_existe(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	assert conexion.existe_codigo_liga("C4N5VT")