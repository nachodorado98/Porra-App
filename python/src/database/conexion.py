import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Optional

from .confconexion import *

# Clase para la conexion a la BBDD
class Conexion:

	def __init__(self)->None:

		try:

			self.bbdd=psycopg2.connect(host=HOST, user=USUARIO, password=CONTRASENA, port=PUERTO, database=DATABASE)
			self.c=self.bbdd.cursor(cursor_factory=RealDictCursor)

		except psycopg2.OperationalError as e:

			print(e)
			raise Exception("Error en la conexion a la BBDD")

	# Metodo para cerrar la conexion a la BBDD
	def cerrarConexion(self)->None:

		self.c.close()
		self.bbdd.close()

	# Metodo para confirmar una accion
	def confirmar(self)->None:

		self.bbdd.commit()

	# Metodo para vaciar la BBDD
	def vaciarBBDD(self)->None:

		self.c.execute("DELETE FROM codigos")

		self.confirmar()

	# Metodo para obtener los codigos de las ligas
	def obtenerCodigosLigas(self)->List[str]:

		self.c.execute("""SELECT * FROM codigos""")

		codigos=self.c.fetchall()

		return list(map(lambda codigo: codigo["codigo_liga"], codigos))

	# Metodo para comprobar si ya existe un usuario
	def existe_usuario(self, usuario:str)->bool:

		self.c.execute("""SELECT *
						FROM usuarios
						WHERE usuario=%s""",
						(usuario,))

		return False if not self.c.fetchone() else True

	# Metodo para comprobar si existe un codigo de liga
	def existe_codigo_liga(self, codigo_liga:str)->bool:

		self.c.execute("""SELECT *
						FROM codigos
						WHERE codigo_liga=%s""",
						(codigo_liga,))

		return False if not self.c.fetchone() else True

	# Metodo para insertar un codigo de liga
	def insertarCodigoLiga(self, codigo_liga:str)->None:

		self.c.execute("""INSERT INTO codigos VALUES (%s)""",
						(codigo_liga,))

		self.confirmar()

	# Metodo para insertar un usuario
	def insertarUsuario(self, usuario:str, correo:str, contrasena:str, nombre:str, apellido:str, codigo_liga:str)->None:

		self.c.execute("""INSERT INTO usuarios
							VALUES (%s, %s, %s, %s, %s, %s)""",
							(usuario, correo, contrasena, nombre, apellido, codigo_liga))

		self.confirmar()