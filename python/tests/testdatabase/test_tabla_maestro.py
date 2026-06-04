import pytest
from datetime import datetime, timedelta

def test_tabla_maestro_vacia(conexion):

	conexion.c.execute("SELECT * FROM maestro")

	assert not conexion.c.fetchall()

def test_insertar_clave_valor_maestro(conexion):

	conexion.insertarClaveValorMaestro("fecha_cierre_porra", "2026-06-22")

	conexion.c.execute("SELECT * FROM maestro")

	clave_valor=conexion.c.fetchall()

	assert len(clave_valor)==1

def test_insertar_clave_valor_maestro_varios(conexion):

	conexion.insertarClaveValorMaestro("fecha_cierre_porra", "2026-06-22")

	conexion.insertarClaveValorMaestro("clave", "valor")

	conexion.c.execute("SELECT * FROM maestro")

	clave_valor=conexion.c.fetchall()

	assert len(clave_valor)==2

def test_obtener_valor_clave_maestro_no_existe(conexion):

	assert conexion.obtenerValorClaveMaestro("fecha_cierre_porra") is None

def test_obtener_valor_clave_maestro_existe(conexion):

	conexion.insertarClaveValorMaestro("fecha_cierre_porra", "2026-06-22")

	conexion.insertarClaveValorMaestro("clave", "valor")

	assert conexion.obtenerValorClaveMaestro("fecha_cierre_porra")=="2026-06-22"

def test_porra_abierta_sin_fecha(conexion):

	assert conexion.porraAbierta()

@pytest.mark.parametrize(["dias"],
	[(2,),(22,),(5,),(13,),(25,),(1,)]
)
def test_porra_abierta_abierta(conexion, dias):

	fecha_posterior=(datetime.now()+timedelta(days=dias)).strftime("%Y-%m-%d")

	conexion.insertarClaveValorMaestro("fecha_cierre_porra", fecha_posterior)

	assert conexion.porraAbierta()

@pytest.mark.parametrize(["dias"],
	[(2,),(22,),(5,),(13,),(25,),(1,),(0,)]
)
def test_porra_abierta_cerrada(conexion, dias):

	fecha_anterior=(datetime.now()-timedelta(days=dias)).strftime("%Y-%m-%d")

	conexion.insertarClaveValorMaestro("fecha_cierre_porra", fecha_anterior)

	assert not conexion.porraAbierta()