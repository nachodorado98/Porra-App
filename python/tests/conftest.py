import os
import sys
sys.path.append("..")

import pytest
from src import crear_app
from confmain import config
from src.database.conexion import Conexion

from src.utilidades.utils import vaciarCarpeta

@pytest.fixture()
def app():

	configuracion=config["DEV"]

	app=crear_app(configuracion)

	yield app

@pytest.fixture()
def password_hash():

	return "$2b$12$NZ.GhycT.kofGXpTgwyYuenY/BPbF1dpO7udruM.sKb09/46Gn7aK"

@pytest.fixture()
def cliente(app):

	return app.test_client()

@pytest.fixture()
def conexion():

	con=Conexion()

	con.vaciarBBDD()

	return con

@pytest.fixture()
def conexion_usuario(conexion, password_hash):

	conexion.insertarCodigoLiga("3YYZKP")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", password_hash, "nacho", "dorado", "3YYZKP")

	conexion.insertarEstadoPorraUsuario("nacho98")

	return conexion

def pytest_sessionstart(session):

	entorno=os.getenv("ENTORNO", "PRO")

	if entorno=="PRO":

		raise Exception("Los tests no se pueden ejecutar en PRO")

	print(f"Los tests se van a ejecutar en {entorno}")

def pytest_sessionfinish(session, exitstatus):

	con=Conexion()

	con.vaciarBBDD()

	con.cerrarConexion()

	print("\nLimpieza de la BBDD correcta")

	ruta_carpeta_imagenes_perfil=os.path.join(os.path.abspath(".."), "src", "static", "imagenes", "perfil")

	vaciarCarpeta(ruta_carpeta_imagenes_perfil)

	print("\nLimpieza de la carpeta imagenes correcta")