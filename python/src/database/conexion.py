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

	# Metodo para obtener la contrasena de un usuario
	def obtenerContrasenaUsuario(self, usuario:str)->Optional[str]:

		self.c.execute("""SELECT contrasena
						FROM usuarios
						WHERE usuario=%s""",
						(usuario,))

		contrasena=self.c.fetchone()

		return None if contrasena is None else contrasena["contrasena"]

	# Metodo para obtener el nombre de usuario
	def obtenerNombre(self, usuario:str)->Optional[str]:

		self.c.execute("""SELECT nombre
						FROM usuarios
						WHERE usuario=%s""",
						(usuario,))

		nombre=self.c.fetchone()

		return None if nombre is None else nombre["nombre"]

	# Metodo para obtener si el usuario es admin
	def obtenerAdmin(self, usuario:str)->bool:

		self.c.execute("""SELECT admin
						FROM usuarios
						WHERE usuario=%s""",
						(usuario,))

		admin=self.c.fetchone()

		return False if admin is None else admin["admin"]

	# Metodo para obtener el codigo liga de un usuario
	def obtenerCodigoLigaUsuario(self, usuario:str)->Optional[str]:

		self.c.execute("""SELECT codigo_liga
						FROM usuarios
						WHERE usuario=%s""",
						(usuario,))

		codigo_liga=self.c.fetchone()

		return None if codigo_liga is None else codigo_liga["codigo_liga"]

	# Metodo para obtener los usuarios del codigo liga
	def obtenerUsuariosCodigoLiga(self, codigo_liga:str)->Optional[List[tuple]]:

		self.c.execute("""SELECT usuario, nombre, apellido
						FROM usuarios
						WHERE codigo_liga=%s""",
						(codigo_liga,))

		usuarios=self.c.fetchall()

		return list(map(lambda usuario: (usuario["usuario"],
										usuario["nombre"],
										usuario["apellido"]) , usuarios))

	# Metodo para insertar el estado de una porra de un usuario
	def insertarEstadoPorraUsuario(self, usuario:str)->None:

		self.c.execute("""INSERT INTO estado_porra
							VALUES (%s)""",
							(usuario,))

		self.confirmar()

	# Metodo para obtener los grupos con sus equipos
	def obtenerGruposEquipos(self)->Optional[List[tuple]]:

		self.c.execute("""SELECT ge.grupo, e.equipo_id, e.nombre, e.escudo, e.bandera
						FROM grupo_equipos ge
						JOIN equipos e
						ON ge.equipo_id=e.equipo_id
						ORDER BY ge.grupo, e.nombre""")

		grupos_equipos=self.c.fetchall()

		return list(map(lambda grupo_equipo: (grupo_equipo["grupo"],
												grupo_equipo["equipo_id"],
												grupo_equipo["nombre"],
												grupo_equipo["escudo"],
												grupo_equipo["bandera"]) , grupos_equipos))