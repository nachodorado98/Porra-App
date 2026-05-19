import os
import sys
sys.path.append("..")

import pytest
from src import crear_app
from confmain import config
from src.database.conexion import Conexion

@pytest.fixture()
def app():

	configuracion=config["DEV"]

	app=crear_app(configuracion)

	yield app

@pytest.fixture()
def cliente(app):

	return app.test_client()

@pytest.fixture()
def conexion():

	con=Conexion()

	con.vaciarBBDD()

	return con

def pytest_sessionfinish(session, exitstatus):

	con=Conexion()

	con.vaciarBBDD()

	con.cerrarConexion()

	print("\nLimpieza de la BBDD correcta")