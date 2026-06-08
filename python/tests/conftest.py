import os
import sys
sys.path.append("..")

import pytest
from src import crear_app
from confmain import config
from src.database.conexion import Conexion
from src.datalake.conexion_data_lake import ConexionDataLake

from src.utilidades.utils import vaciarCarpeta

@pytest.fixture()
def entorno():

	entorno=os.getenv("ENTORNO", "DEV")

	return config[entorno].ENVIROMENT

@pytest.fixture()
def contenedor_dl(entorno):

	return entorno.lower()

@pytest.fixture()
def app(entorno):

	configuracion=config[entorno]

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

	conexion.insertarPuntuacionUsuario("nacho98")

	return conexion

@pytest.fixture
def porra_grupos():

	return {'A': ['republica-checa', 'seleccion-republica-corea', 'seleccion-mexico', 'seleccion-sudafrica'],
			'B': ['canada', 'seleccion-bosnia-herzegovina', 'seleccion-suiza', 'seleccion-qatar'],
			'C': ['seleccion-marruecos', 'seleccion-escocia', 'seleccion-brasil', 'haiti'],
			'D': ['seleccion-estados-unidos', 'seleccion-paraguay', 'seleccion-turquia', 'seleccion-australia'],
			'E': ['seleccion-ecuador', 'seleccion-costa-marfil', 'seleccion-alemania', 'curazao'],
			'F': ['seleccion-japon', 'seleccion-suecia', 'seleccion-holanda', 'seleccion-tunez'],
			'G': ['seleccion-egipto', 'seleccion-iran', 'seleccion-belgica', 'seleccion-nueva-zelanda'],
			'H': ['seleccion-uruguay', 'seleccion-arabia-saudi', 'seleccion-espanola', 'cabo-verde'],
			'I': ['seleccion-noruega', 'senegal', 'seleccion-francia', 'seleccion-iraq'],
			'J': ['seleccion-austria', 'seleccion-argelia', 'seleccion-argentina', 'jordania'],
			'K': ['seleccion-colombia', 'rd-congo', 'seleccion-portugal', 'seleccion-uzbekistan'],
			'L': ['seleccion-croacia', 'seleccion-ghana', 'seleccion-inglaterra', 'panama-seleccion']}

@pytest.fixture
def porra_mejores_terceros():

	return [{'equipo_id': 'seleccion-brasil', 'grupo': 'C'},
				{'equipo_id': 'seleccion-espanola', 'grupo': 'H'},
				{'equipo_id': 'seleccion-alemania', 'grupo': 'E'},
				{'equipo_id': 'seleccion-holanda', 'grupo': 'F'},
				{'equipo_id': 'seleccion-francia', 'grupo': 'I'},
				{'equipo_id': 'seleccion-argentina', 'grupo': 'J'},
				{'equipo_id': 'seleccion-portugal', 'grupo': 'K'},
				{'equipo_id': 'seleccion-inglaterra', 'grupo': 'L'}]

@pytest.fixture
def bracket_16avos_real():
	return {'M73': [('seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR'), ('seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH')],
			'M74': [('seleccion-ecuador', 'Ecuador', 3771, 'ECU'), ('seleccion-brasil', 'Brasil', 3775, 'BRA')],
			'M75': [('seleccion-japon', 'Japón', 3798, 'JPN'), ('seleccion-escocia', 'Escocia', 3758, 'SCO')],
			'M76': [('seleccion-marruecos', 'Marruecos', 3780, 'MAR'), ('seleccion-suecia', 'Suecia', 3074, 'SWE')],
			'M77': [('seleccion-noruega', 'Noruega', 3759, 'NOR'), ('seleccion-holanda', 'Países Bajos', 3761, 'NLD')],
			'M78': [('seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV'), ('senegal', 'Senegal', 5658, 'SEN')],
			'M79': [('republica-checa', 'República Checa', 6188, 'CZE'), ('seleccion-alemania', 'Alemania', 3734, 'DEU')],
			'M80': [('seleccion-croacia', 'Croacia', 3766, 'HRV'), ('seleccion-portugal', 'Portugal', 3762, 'PRT')],
			'M81': [('seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'), ('seleccion-francia', 'Francia', 3750, 'FRA')],
			'M82': [('seleccion-egipto', 'Egipto', 3788, 'EGY'), ('seleccion-espanola', 'España', 3850, 'ESP')],
			'M83': [('rd-congo', 'RD Congo', 11591, 'COD'), ('seleccion-ghana', 'Ghana', 3791, 'GHA')],
			'M84': [('seleccion-uruguay', 'Uruguay', 3768, 'URY'), ('seleccion-argelia', 'Argelia', 3787, 'DZA')],
			'M85': [('canada', 'Canadá', 5577, 'CAN'), ('seleccion-argentina', 'Argentina', 3770, 'ARG')],
			'M86': [('seleccion-austria', 'Austria', 3767, 'AUT'), ('seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU')],
			'M87': [('seleccion-colombia', 'Colombia', 3774, 'COL'), ('seleccion-inglaterra', 'Inglaterra', 3745, 'ENG')],
			'M88': [('seleccion-paraguay', 'Paraguay', 3773, 'PRY'), ('seleccion-iran', 'Irán', 3806, 'IRN')]}

@pytest.fixture
def partidos_bracket():

	return [{'ronda': 'dieciseisavos', 'partido': 'M73', 'equipo_1_id': 'seleccion-republica-corea', 'equipo_2_id': 'seleccion-bosnia-herzegovina', 'ganador_id': 'seleccion-republica-corea'},
			{'ronda': 'dieciseisavos', 'partido': 'M74', 'equipo_1_id': 'seleccion-ecuador', 'equipo_2_id': 'seleccion-brasil', 'ganador_id': 'seleccion-brasil'},
			{'ronda': 'dieciseisavos', 'partido': 'M75', 'equipo_1_id': 'seleccion-japon', 'equipo_2_id': 'seleccion-escocia', 'ganador_id': 'seleccion-japon'},
			{'ronda': 'dieciseisavos', 'partido': 'M76', 'equipo_1_id': 'seleccion-marruecos', 'equipo_2_id': 'seleccion-suecia', 'ganador_id': 'seleccion-marruecos'},
			{'ronda': 'dieciseisavos', 'partido': 'M77', 'equipo_1_id': 'seleccion-noruega', 'equipo_2_id': 'seleccion-holanda', 'ganador_id': 'seleccion-holanda'},
			{'ronda': 'dieciseisavos', 'partido': 'M78', 'equipo_1_id': 'seleccion-costa-marfil', 'equipo_2_id': 'senegal', 'ganador_id': 'senegal'},
			{'ronda': 'dieciseisavos', 'partido': 'M79', 'equipo_1_id': 'republica-checa', 'equipo_2_id': 'seleccion-alemania', 'ganador_id': 'seleccion-alemania'},
			{'ronda': 'dieciseisavos', 'partido': 'M80', 'equipo_1_id': 'seleccion-croacia', 'equipo_2_id': 'seleccion-portugal', 'ganador_id': 'seleccion-portugal'},
			{'ronda': 'dieciseisavos', 'partido': 'M81', 'equipo_1_id': 'seleccion-estados-unidos', 'equipo_2_id': 'seleccion-francia', 'ganador_id': 'seleccion-francia'},
			{'ronda': 'dieciseisavos', 'partido': 'M82', 'equipo_1_id': 'seleccion-egipto', 'equipo_2_id': 'seleccion-espanola', 'ganador_id': 'seleccion-espanola'},
			{'ronda': 'dieciseisavos', 'partido': 'M83', 'equipo_1_id': 'rd-congo', 'equipo_2_id': 'seleccion-ghana', 'ganador_id': 'seleccion-ghana'},
			{'ronda': 'dieciseisavos', 'partido': 'M84', 'equipo_1_id': 'seleccion-uruguay', 'equipo_2_id': 'seleccion-argelia', 'ganador_id': 'seleccion-uruguay'},
			{'ronda': 'dieciseisavos', 'partido': 'M85', 'equipo_1_id': 'canada', 'equipo_2_id': 'seleccion-argentina', 'ganador_id': 'seleccion-argentina'},
			{'ronda': 'dieciseisavos', 'partido': 'M86', 'equipo_1_id': 'seleccion-austria', 'equipo_2_id': 'seleccion-arabia-saudi', 'ganador_id': 'seleccion-austria'},
			{'ronda': 'dieciseisavos', 'partido': 'M87', 'equipo_1_id': 'seleccion-colombia', 'equipo_2_id': 'seleccion-inglaterra', 'ganador_id': 'seleccion-inglaterra'},
			{'ronda': 'dieciseisavos', 'partido': 'M88', 'equipo_1_id': 'seleccion-paraguay', 'equipo_2_id': 'seleccion-iran', 'ganador_id': 'seleccion-paraguay'},
			{'ronda': 'octavos', 'partido': 'M89', 'equipo_1_id': 'seleccion-brasil', 'equipo_2_id': 'seleccion-holanda', 'ganador_id': 'seleccion-brasil'},
			{'ronda': 'octavos', 'partido': 'M90', 'equipo_1_id': 'seleccion-republica-corea', 'equipo_2_id': 'seleccion-japon', 'ganador_id': 'seleccion-japon'},
			{'ronda': 'octavos', 'partido': 'M91', 'equipo_1_id': 'seleccion-marruecos', 'equipo_2_id': 'senegal', 'ganador_id': 'senegal'},
			{'ronda': 'octavos', 'partido': 'M92', 'equipo_1_id': 'seleccion-alemania', 'equipo_2_id': 'seleccion-portugal', 'ganador_id': 'seleccion-alemania'},
			{'ronda': 'octavos', 'partido': 'M93', 'equipo_1_id': 'seleccion-ghana', 'equipo_2_id': 'seleccion-uruguay', 'ganador_id': 'seleccion-uruguay'},
			{'ronda': 'octavos', 'partido': 'M94', 'equipo_1_id': 'seleccion-francia', 'equipo_2_id': 'seleccion-espanola', 'ganador_id': 'seleccion-espanola'},
			{'ronda': 'octavos', 'partido': 'M95', 'equipo_1_id': 'seleccion-austria', 'equipo_2_id': 'seleccion-paraguay', 'ganador_id': 'seleccion-austria'},
			{'ronda': 'octavos', 'partido': 'M96', 'equipo_1_id': 'seleccion-argentina', 'equipo_2_id': 'seleccion-inglaterra', 'ganador_id': 'seleccion-argentina'},
			{'ronda': 'cuartos', 'partido': 'M97', 'equipo_1_id': 'seleccion-brasil', 'equipo_2_id': 'seleccion-japon', 'ganador_id': 'seleccion-brasil'},
			{'ronda': 'cuartos', 'partido': 'M98', 'equipo_1_id': 'seleccion-uruguay', 'equipo_2_id': 'seleccion-espanola', 'ganador_id': 'seleccion-espanola'},
			{'ronda': 'cuartos', 'partido': 'M99', 'equipo_1_id': 'seleccion-alemania', 'equipo_2_id': 'senegal', 'ganador_id': 'seleccion-alemania'},
			{'ronda': 'cuartos', 'partido': 'M100', 'equipo_1_id': 'seleccion-argentina', 'equipo_2_id': 'seleccion-austria', 'ganador_id': 'seleccion-argentina'},
			{'ronda': 'semifinales', 'partido': 'M101', 'equipo_1_id': 'seleccion-brasil', 'equipo_2_id': 'seleccion-espanola', 'ganador_id': 'seleccion-espanola'},
			{'ronda': 'semifinales', 'partido': 'M102', 'equipo_1_id': 'seleccion-alemania', 'equipo_2_id': 'seleccion-argentina', 'ganador_id': 'seleccion-argentina'},
			{'ronda': 'tercer_puesto', 'partido': 'M103', 'equipo_1_id': 'seleccion-brasil', 'equipo_2_id': 'seleccion-alemania', 'ganador_id': 'seleccion-brasil'},
			{'ronda': 'final', 'partido': 'M104', 'equipo_1_id': 'seleccion-espanola', 'equipo_2_id': 'seleccion-argentina', 'ganador_id': 'seleccion-espanola'}]

@pytest.fixture()
def datalake():

	return ConexionDataLake()

def pytest_sessionstart(session):

	entorno=os.getenv("ENTORNO", "DEV")
	contendor_dl=entorno.lower()

	if entorno=="PRO":

		raise Exception("Los tests no se pueden ejecutar en PRO")

	print(f"Los tests se van a ejecutar en {entorno}")

	dl=ConexionDataLake()

	if not dl.existe_contenedor(contendor_dl):

		print(f"Contenedor {contendor_dl} no existe.")

		dl.crearContenedor(contendor_dl)

		print(f"Contenedor {contendor_dl} CREADO.")

	if not dl.existe_carpeta(contendor_dl, "perfil"):

		print("Carpeta perfil no existe.")

		dl.crearCarpeta(contendor_dl, "perfil")

		print("Carpeta perfil CREADA.")

	else:

		print("Carpeta perfil ELIMINADA.")

		dl.eliminarCarpeta(contendor_dl, "perfil")

		dl.crearCarpeta(contendor_dl, "perfil")

		print("Carpeta perfil RECREADA.")

	dl.cerrarConexion()

	print(f"\nEntorno del DataLake de {entorno} creado")

def pytest_sessionfinish(session, exitstatus):

	entorno=os.getenv("ENTORNO", "DEV")
	contendor_dl=entorno.lower()

	con=Conexion()

	con.vaciarBBDD()

	con.cerrarConexion()

	print("\nLimpieza de la BBDD correcta")

	ruta_carpeta_imagenes_perfil_usuario=os.path.join(os.path.abspath(".."), "src", "static", "imagenes", "perfil", "nacho98")

	vaciarCarpeta(ruta_carpeta_imagenes_perfil_usuario)

	ruta_carpeta_imagenes_perfil=os.path.join(os.path.abspath(".."), "src", "static", "imagenes", "perfil")

	vaciarCarpeta(ruta_carpeta_imagenes_perfil)

	print("\nLimpieza de la carpeta imagenes correcta")

	dl=ConexionDataLake()

	if dl.existe_carpeta(contendor_dl, "perfil"):

		print("Carpeta perfil ELIMINADA.")

		dl.eliminarCarpeta(contendor_dl, "perfil")

		dl.crearCarpeta(contendor_dl, "perfil")

		print("Carpeta perfil RECREADA.")

	else:

		dl.crearCarpeta(contendor_dl, "perfil")

		print("Carpeta perfil CREADA.")

	dl.cerrarConexion()

	print("\nLimpieza del DataLake correcta")