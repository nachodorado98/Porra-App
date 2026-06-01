import pytest

def test_tabla_lookup_bracket_mejores_terceros_llena(conexion):

	conexion.c.execute("SELECT * FROM lookup_bracket_mejores_terceros")

	assert conexion.c.fetchall()

@pytest.mark.parametrize(["combinacion"],
	[("combinacion",),("hola",),("A",),("ABCDEFKN",),("BACDEFKL",)]
)
def test_obtener_combinacion_partidos_mejores_terceros_combinacion_no_existe(conexion, combinacion):

	assert not conexion.obtenerCombinacionPartidosMejoresTerceros(combinacion)

@pytest.mark.parametrize(["combinacion"],
	[("ABCDEFKL",)]
)
def test_obtener_combinacion_partidos_mejores_terceros_combinacion_existe(conexion, combinacion):

	combinacion_partidos_mejores_terceros=conexion.obtenerCombinacionPartidosMejoresTerceros(combinacion)

	assert len(combinacion_partidos_mejores_terceros.keys())==8