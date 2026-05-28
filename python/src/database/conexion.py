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

	# Metodo para eliminar un usuario
	def eliminarUsuario(self, usuario:str)->None:

		self.c.execute("""DELETE FROM usuarios
							WHERE Usuario=%s""",
							(usuario,))

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

		self.c.execute("""SELECT usuario, nombre, apellido,
								CASE WHEN Imagen_Perfil IS NULL
									THEN '-1'
									ELSE Imagen_Perfil
								END as Imagen
						FROM usuarios
						WHERE codigo_liga=%s""",
						(codigo_liga,))

		usuarios=self.c.fetchall()

		return list(map(lambda usuario: (usuario["usuario"],
										usuario["nombre"],
										usuario["apellido"],
										usuario["imagen"]) , usuarios))
		
	# Metodo para obtener la imagen de usuario
	def obtenerImagenPerfilUsuario(self, usuario:str)->Optional[str]:

		self.c.execute("""SELECT
							CASE WHEN Imagen_Perfil IS NULL
									THEN '-1'
									ELSE Imagen_Perfil
							END as Imagen
							FROM usuarios
							WHERE Usuario=%s""",
							(usuario,))

		imagen=self.c.fetchone()

		return None if not imagen else imagen["imagen"]

	# Metodo para actualizar la imagen de perfil del usuario
	def actualizarImagenPerfilUsuario(self, usuario:str, imagen:str)->None:

		self.c.execute("""UPDATE usuarios
							SET Imagen_Perfil=%s
							WHERE Usuario=%s""",
							(imagen, usuario))

		self.confirmar()

	# Metodo para obtener el estado de una porra de un usuario
	def obtenerEstadoPorraUsuario(self, usuario:str)->Optional[tuple]:

		self.c.execute("""SELECT grupos_completados, mejores_terceros_completados
							FROM estado_porra
							WHERE usuario=%s""",
							(usuario,))

		estado_porra_usuario=self.c.fetchone()

		return None if estado_porra_usuario is None else (estado_porra_usuario["grupos_completados"],
															estado_porra_usuario["mejores_terceros_completados"])

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

	# Metodo para insertar un equipo con posicion en grupo de un usuario
	def insertarEquipoGrupoPorraUsuario(self, usuario:str, grupo:str, equipo_id:str, posicion:int)->None:

		self.c.execute("""INSERT INTO grupo_equipos_porra (Usuario, Grupo, Equipo_Id, Posicion)
							VALUES (%s, %s, %s, %s)""",
							(usuario, grupo, equipo_id, posicion))

		self.confirmar()

	# Metodo para insertar los equipos con posiciones en grupo de un usuario
	def insertarEquipoGruposPorraUsuario(self, usuario:str, grupo:str, equipos:List[str])->None:

		valores=[(usuario, grupo, equipo, posicion) for posicion, equipo in enumerate(equipos, start=1)]

		self.c.executemany("""INSERT INTO grupo_equipos_porra (Usuario, Grupo, Equipo_Id, Posicion)
							VALUES (%s, %s, %s, %s)""",
							valores)

		self.confirmar()

	# Metodo para actualizar el estado de los grupos de la porra de un usuario
	def actualizarEstadoPorraGruposUsuario(self, usuario:str)->None:

		self.c.execute("""UPDATE estado_porra
							SET Grupos_Completados=True
							WHERE usuario=%s""",
							(usuario,))

		self.confirmar()

	# Metodo para saber si un usuario ha completado los grupos de la porra
	def gruposPorraCompleto(self, usuario:str)->bool:

		self.c.execute("""SELECT Grupos_Completados
							FROM estado_porra
							WHERE Usuario=%s""",
							(usuario,))

		grupos_completados=self.c.fetchone()

		return False if grupos_completados is None else grupos_completados["grupos_completados"]

	# Metodo para saber si un usuario puede editar los grupos de la porra
	def puedeEditarGruposPorra(self, usuario:str)->bool:

		return not self.gruposPorraCompleto(usuario)

	# Metodo para obtener los equipos terceros de los grupos de un usuario
	def obtenerTercerosGruposUsuario(self, usuario:str)->Optional[List[tuple]]:

		self.c.execute("""SELECT gep.grupo, e.equipo_id, e.nombre, e.escudo, e.bandera
						FROM grupo_equipos_porra gep
						JOIN equipos e
						ON gep.equipo_id=e.equipo_id
						WHERE gep.usuario=%s
						AND gep.posicion=3
						ORDER BY gep.grupo, e.nombre""",
						(usuario,))

		terceros_grupos=self.c.fetchall()

		return list(map(lambda tercero_grupo: (tercero_grupo["grupo"],
												tercero_grupo["equipo_id"],
												tercero_grupo["nombre"],
												tercero_grupo["escudo"],
												tercero_grupo["bandera"]) , terceros_grupos))

	# Metodo para actualizar el estado de los mejores terceros de la porra de un usuario
	def actualizarEstadoPorraMejoresTercerosUsuario(self, usuario:str)->None:

		self.c.execute("""UPDATE estado_porra
							SET Mejores_Terceros_Completados=True
							WHERE usuario=%s""",
							(usuario,))

		self.confirmar()

	# Metodo para saber si un usuario ha completado los mejores terceros de la porra
	def mejoresTercerosPorraCompleto(self, usuario:str)->bool:

		self.c.execute("""SELECT Mejores_Terceros_Completados
							FROM estado_porra
							WHERE Usuario=%s""",
							(usuario,))

		mejores_terceros_completados=self.c.fetchone()

		return False if mejores_terceros_completados is None else mejores_terceros_completados["mejores_terceros_completados"]

	# Metodo para saber si un usuario puede editar los mejores terceros de la porra
	def puedeEditarMejoresTercerosPorra(self, usuario:str)->bool:

		return not self.mejoresTercerosPorraCompleto(usuario)

	# Metodo para insertar un equipo con orden de mejor tercero de un usuario
	def insertarEquipoMejorTerceroPorraUsuario(self, usuario:str, grupo:str, equipo_id:str, orden:int)->None:

		self.c.execute("""INSERT INTO mejores_terceros_porra (Usuario, Grupo, Equipo_Id, Orden)
							VALUES (%s, %s, %s, %s)""",
							(usuario, grupo, equipo_id, orden))

		self.confirmar()

	# Metodo para insertar los equipos con orden de mejor tercero de un usuario
	def insertarEquipoMejoresTercerosPorraUsuario(self, usuario:str, equipos:List[str])->None:

	    valores=[(usuario, grupo, equipo_id, orden) for orden, (grupo, equipo_id) in enumerate(equipos, start=1)]

	    self.c.executemany("""INSERT INTO mejores_terceros_porra (Usuario, Grupo, Equipo_Id, Orden)
	        					VALUES (%s, %s, %s, %s)""",
	        					valores)

	    self.confirmar()

 	# Metodo para reiniciar porra grupos de un usuario
	def reiniciarGruposPorraUsuario(self, usuario:str)->None:

		self.c.execute("""DELETE FROM grupo_equipos_porra
							WHERE Usuario=%s""",
							(usuario,))

		self.confirmar()

 	# Metodo para reiniciar porra mejores terceros de un usuario
	def reiniciarMejoresTercerosPorraUsuario(self, usuario:str)->None:

		self.c.execute("""DELETE FROM mejores_terceros_porra
							WHERE Usuario=%s""",
							(usuario,))

		self.confirmar()

	# Metodo para reiniciar estado porra de un usuario
	def reiniciarEstadoPorraUsuario(self, usuario:str)->None:

		self.c.execute("""UPDATE estado_porra
							SET grupos_completados=False, mejores_terceros_completados=False
							WHERE Usuario=%s""",
							(usuario,))

		self.confirmar()