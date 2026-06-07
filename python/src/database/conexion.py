import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Optional, Dict
from datetime import datetime, timedelta

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

		self.c.execute("DELETE FROM maestro")

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

	# Metodo para comprobar si ya existe un correo
	def existe_correo(self, correo:str)->bool:

		self.c.execute("""SELECT *
						FROM usuarios
						WHERE correo=%s""",
						(correo,))

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

	# Metodo para obtener los datos (correos, nombres y usuarios) de todos de los usuarios
	def obtenerDatosUsuarios(self)->List[tuple]:

		self.c.execute("""SELECT usuario, nombre, correo, codigo_liga
							FROM usuarios
							ORDER BY nombre, apellido""")

		datos=self.c.fetchall()

		return list(map(lambda dato: (dato["usuario"],
										dato["nombre"],
										dato["correo"],
										dato["codigo_liga"]), datos))

	# Metodo para obtener los datos (correos, nombres y usuarios) de todos de los usuarios con la porra pendiente
	def obtenerDatosUsuariosPorraPendiente(self)->List[tuple]:

		self.c.execute("""SELECT u.usuario, u.nombre, u.correo, u.codigo_liga
							FROM usuarios u
							JOIN estado_porra ep
							ON u.usuario=ep.usuario
							WHERE ep.porra_completada=False
							ORDER BY nombre, apellido""")

		datos=self.c.fetchall()

		return list(map(lambda dato: (dato["usuario"],
										dato["nombre"],
										dato["correo"],
										dato["codigo_liga"]), datos))

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
						WHERE codigo_liga=%s
						ORDER BY nombre, apellido, usuario""",
						(codigo_liga,))

		usuarios=self.c.fetchall()

		return list(map(lambda usuario: (usuario["usuario"],
										usuario["nombre"],
										usuario["apellido"],
										usuario["imagen"]) , usuarios))

	# Metodo para obtener los usuarios del codigo liga con sus puntuaciones
	def obtenerPuntuacionesUsuariosCodigoLiga(self, codigo_liga:str)->Optional[List[tuple]]:

		self.c.execute("""SELECT u.usuario, u.nombre, u.apellido,
								CASE WHEN u.Imagen_Perfil IS NULL
									THEN '-1'
									ELSE u.Imagen_Perfil
								END as Imagen,
								COALESCE(p.puntos_grupos, 0) AS puntos_grupos,
								COALESCE(p.puntos_mejores_terceros, 0) AS puntos_mejores_terceros,
								COALESCE(p.puntos_eliminatorias, 0) AS puntos_eliminatorias,
								COALESCE(p.puntos_total, 0) AS puntos_total
						FROM usuarios u
						LEFT JOIN puntuaciones p
            			ON u.usuario=p.usuario
						WHERE u.codigo_liga=%s
						ORDER BY puntos_total DESC, u.nombre, u.apellido, u.usuario""",
						(codigo_liga,))

		usuarios=self.c.fetchall()

		return list(map(lambda usuario: (usuario["usuario"],
										usuario["nombre"],
										usuario["apellido"],
										usuario["imagen"],
										usuario["puntos_grupos"],
										usuario["puntos_mejores_terceros"],
										usuario["puntos_eliminatorias"],
										usuario["puntos_total"]) , usuarios))
		
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

	# Metodo para obtener los datos del cambio de contraseña del usuario
	def obtenerDatosCambioContrasenaUsuario(self, usuario:str)->Optional[tuple]:

		self.c.execute("""SELECT Cambios_Contrasena, Ultimo_Cambio_Contrasena
							FROM usuarios
							WHERE Usuario=%s""",
							(usuario,))

		datos_contrasena=self.c.fetchone()

		return None if not datos_contrasena else (datos_contrasena["cambios_contrasena"], datos_contrasena["ultimo_cambio_contrasena"])

	# Metodo para saber si un usuario puede cambiar la contraseña
	def puedeCambiarContrasena(self, usuario:str)->bool:

		try:

			cambios, ultimo_cambio=self.obtenerDatosCambioContrasenaUsuario(usuario)

			if cambios>=3:

				return False

			if not ultimo_cambio:

					return True

			return datetime.now()-ultimo_cambio>timedelta(days=1)

		except Exception:

			return False

	# Metodo para actualizar la contrasena del usuario
	def actualizarContrasenaUsuario(self, usuario:str, nueva_contrasena:str, cambios_contrasena:int, ultimo_cambio:str)->None:

		self.c.execute("""UPDATE usuarios
							SET Contrasena=%s, Cambios_Contrasena=%s, Ultimo_Cambio_Contrasena=%s
							WHERE Usuario=%s""",
							(nueva_contrasena, cambios_contrasena, ultimo_cambio, usuario))

		self.confirmar()

	# Metodo para obtener el estado de una porra de un usuario
	def obtenerEstadoPorraUsuario(self, usuario:str)->Optional[tuple]:

		self.c.execute("""SELECT grupos_completados, mejores_terceros_completados, eliminatorias_completadas, porra_completada
							FROM estado_porra
							WHERE usuario=%s""",
							(usuario,))

		estado_porra_usuario=self.c.fetchone()

		return None if estado_porra_usuario is None else (estado_porra_usuario["grupos_completados"],
															estado_porra_usuario["mejores_terceros_completados"],
															estado_porra_usuario["eliminatorias_completadas"],
															estado_porra_usuario["porra_completada"])

	# Metodo para insertar el estado de una porra de un usuario
	def insertarEstadoPorraUsuario(self, usuario:str)->None:

		self.c.execute("""INSERT INTO estado_porra
							VALUES (%s)""",
							(usuario,))

		self.confirmar()

	# Metodo para insertar la puntuacion de una porra de un usuario
	def insertarPuntuacionUsuario(self, usuario:str)->None:

		self.c.execute("""INSERT INTO puntuaciones
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
	def insertarEquipoGruposPorraUsuario(self, usuario:str, grupo:str, equipos:List[tuple])->None:

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
	def insertarEquipoMejoresTercerosPorraUsuario(self, usuario:str, equipos:List[tuple])->None:

		valores=[(usuario, grupo, equipo_id, orden) for orden, (grupo, equipo_id) in enumerate(equipos, start=1)]

		self.c.executemany("""INSERT INTO mejores_terceros_porra (Usuario, Grupo, Equipo_Id, Orden)
								VALUES (%s, %s, %s, %s)""",
								valores)

		self.confirmar()

	# Metodo para actualizar el estado de las eliminatorias de la porra de un usuario
	def actualizarEstadoPorraEliminatoriasUsuario(self, usuario:str)->None:

		self.c.execute("""UPDATE estado_porra
							SET Eliminatorias_Completadas=True
							WHERE usuario=%s""",
							(usuario,))

		self.confirmar()

	# Metodo para actualizar el estado de de la porra de un usuario
	def actualizarEstadoPorraUsuario(self, usuario:str)->None:

		self.c.execute("""UPDATE estado_porra
							SET Porra_Completada=True
							WHERE usuario=%s""",
							(usuario,))

		self.confirmar()

	# Metodo para saber si un usuario ha completado las eliminatorias de la porra
	def eliminatoriasPorraCompleto(self, usuario:str)->bool:

		self.c.execute("""SELECT Eliminatorias_Completadas
							FROM estado_porra
							WHERE Usuario=%s""",
							(usuario,))

		eliminatorias_completadas=self.c.fetchone()

		return False if eliminatorias_completadas is None else eliminatorias_completadas["eliminatorias_completadas"]

	# Metodo para saber si un usuario puede editar las eliminatorias de la porra
	def puedeEditarEliminatoriasPorra(self, usuario:str)->bool:

		return not self.eliminatoriasPorraCompleto(usuario)

	# Metodo para saber si un usuario ha completado la porra
	def porraCompleta(self, usuario:str)->bool:

		self.c.execute("""SELECT Porra_Completada
							FROM estado_porra
							WHERE Usuario=%s""",
							(usuario,))

		porra_completada=self.c.fetchone()

		return False if porra_completada is None else porra_completada["porra_completada"]

	# Metodo para saber si un usuario puede visualizar la porra
	def puedeVisualizarPorra(self, usuario:str)->bool:

		return self.porraCompleta(usuario)

	# Metodo para insertar un partido de ronda de eliminatorias de un usuario
	def insertarPartidoEliminatoriaPorraUsuario(self, usuario:str, ronda:str, partido:str, equipo_1_id:str, equipo_2_id:str, ganador_id:str)->None:

		self.c.execute("""INSERT INTO eliminatorias_porra (Usuario, Ronda, Partido, Equipo_1_Id, Equipo_2_Id, Ganador_Id)
							VALUES (%s, %s, %s, %s, %s, %s)""",
							(usuario, ronda, partido, equipo_1_id, equipo_2_id, ganador_id))

		self.confirmar()

	# Metodo para insertar los partidos de rondas de eliminatorias de un usuario
	def insertarPartidosEliminatoriasPorraUsuario(self, usuario:str, partidos:List[tuple])->None:

		valores=[(usuario, ronda, partido, equipo_1, equipo_2, ganador) for ronda, partido, equipo_1, equipo_2, ganador in partidos]

		self.c.executemany("""INSERT INTO eliminatorias_porra (Usuario, Ronda, Partido, Equipo_1_Id, Equipo_2_Id, Ganador_Id)
								VALUES (%s, %s, %s, %s, %s, %s)""",
								valores)

		self.confirmar()

	# Metodo para obtener los equipos primeros y segundos de los grupos de un usuario
	def obtenerPrimerosSegundosGruposUsuario(self, usuario:str)->Optional[List[tuple]]:

		self.c.execute("""SELECT gep.grupo, e.equipo_id, e.nombre, e.escudo, e.bandera, gep.posicion
						FROM grupo_equipos_porra gep
						JOIN equipos e
						ON gep.equipo_id=e.equipo_id
						WHERE gep.usuario=%s
						AND gep.posicion in (1, 2)
						ORDER BY gep.posicion, gep.grupo, e.nombre""",
						(usuario,))

		primero_segundos_grupos=self.c.fetchall()

		return list(map(lambda primero_segundo_grupo: (primero_segundo_grupo["grupo"],
														primero_segundo_grupo["equipo_id"],
														primero_segundo_grupo["nombre"],
														primero_segundo_grupo["escudo"],
														primero_segundo_grupo["bandera"],
														primero_segundo_grupo["posicion"]) , primero_segundos_grupos))

	# Metodo para obtener los mejores equipos terceros de un usuario
	def obtenerMejoresTercerosUsuario(self, usuario:str)->Optional[List[tuple]]:

		self.c.execute("""SELECT mtp.grupo, e.equipo_id, e.nombre, e.escudo, e.bandera
						FROM mejores_terceros_porra mtp
						JOIN equipos e
						ON mtp.equipo_id=e.equipo_id
						WHERE mtp.usuario=%s
						ORDER BY mtp.grupo, e.nombre""",
						(usuario,))

		mejores_terceros=self.c.fetchall()

		return list(map(lambda mejor_tercero: (mejor_tercero["grupo"],
												mejor_tercero["equipo_id"],
												mejor_tercero["nombre"],
												mejor_tercero["escudo"],
												mejor_tercero["bandera"],
												3) , mejores_terceros))

	# Metodo para obtener la combinacion de los partidos de los mejores_terceros
	def obtenerCombinacionPartidosMejoresTerceros(self, combinacion_mejores_terceros:str)->Optional[Dict]:

		self.c.execute("""SELECT M74, M77, M79, M80, M81, M82, M85, M87
						FROM lookup_bracket_mejores_terceros
						WHERE mejores_terceros=%s""",
						(combinacion_mejores_terceros,))

		combinacion_partidos_mejores_terceros=self.c.fetchone()

		return False if combinacion_partidos_mejores_terceros is None else  {partido.upper():equipo for partido, equipo in combinacion_partidos_mejores_terceros.items()}

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

	# Metodo para reiniciar porra eliminatorias de un usuario
	def reiniciarEliminatoriasPorraUsuario(self, usuario:str)->None:

		self.c.execute("""DELETE FROM eliminatorias_porra
							WHERE Usuario=%s""",
							(usuario,))

		self.confirmar()

	# Metodo para reiniciar estado porra de un usuario
	def reiniciarEstadoPorraUsuario(self, usuario:str)->None:

		self.c.execute("""UPDATE estado_porra
							SET grupos_completados=False, mejores_terceros_completados=False,
							eliminatorias_completadas=False, porra_completada=False
							WHERE Usuario=%s""",
							(usuario,))

		self.confirmar()

	# Metodo para obtener la porra de los grupos de un usuario
	def obtenerGruposPorraUsuario(self, usuario:str)->Optional[List[tuple]]:

		self.c.execute("""SELECT gep.grupo, e.equipo_id, e.nombre, e.escudo, e.bandera
							FROM grupo_equipos_porra gep
							JOIN equipos e
							ON gep.equipo_id = e.equipo_id
							WHERE gep.usuario=%s
							ORDER BY gep.grupo, gep.posicion""",
							(usuario,))

		grupos_porra=self.c.fetchall()

		return list(map(lambda grupo_porra: (grupo_porra["grupo"],
												grupo_porra["equipo_id"],
												grupo_porra["nombre"],
												grupo_porra["escudo"],
												grupo_porra["bandera"]), grupos_porra))

	# Metodo para obtener las eliminatorias de la porra de un usuario
	def obtenerEliminatoriasPorraUsuario(self, usuario:str)->Optional[List[tuple]]:

		self.c.execute("""SELECT ep.ronda, ep.partido, ep.equipo_1_id, e1.nombre AS equipo_1_nombre, e1.escudo AS equipo_1_escudo, e1.bandera AS equipo_1_bandera,
								ep.equipo_2_id, e2.nombre AS equipo_2_nombre, e2.escudo AS equipo_2_escudo, e2.bandera AS equipo_2_bandera,
								ep.ganador_id, eg.nombre AS ganador_nombre, eg.escudo AS ganador_escudo, eg.bandera AS ganador_bandera
							FROM eliminatorias_porra ep
							JOIN equipos e1
							ON ep.equipo_1_id=e1.equipo_id
							JOIN equipos e2
							ON ep.equipo_2_id=e2.equipo_id
							JOIN equipos eg
							ON ep.ganador_id=eg.equipo_id
							WHERE ep.usuario=%s
							ORDER BY CAST(SUBSTRING(ep.partido FROM 2) AS INTEGER)""",
							(usuario,))

		eliminatorias_porra=self.c.fetchall()

		return list(map(lambda eliminatoria_porra: (eliminatoria_porra["ronda"],
													eliminatoria_porra["partido"],
													eliminatoria_porra["equipo_1_id"],
													eliminatoria_porra["equipo_1_nombre"],
													eliminatoria_porra["equipo_1_escudo"],
													eliminatoria_porra["equipo_1_bandera"],
													eliminatoria_porra["equipo_2_id"],
													eliminatoria_porra["equipo_2_nombre"],
													eliminatoria_porra["equipo_2_escudo"],
													eliminatoria_porra["equipo_2_bandera"],
													eliminatoria_porra["ganador_id"],
													eliminatoria_porra["ganador_nombre"],
													eliminatoria_porra["ganador_escudo"],
													eliminatoria_porra["ganador_bandera"]), eliminatorias_porra))

	# Metodo para insertar un registro en la tabla maestro
	def insertarClaveValorMaestro(self, clave:str, valor:str)->None:

		self.c.execute("""INSERT INTO maestro VALUES (%s, %s)""",
						(clave, valor))

		self.confirmar()

	# Metodo para obtener el valor de una clave en la tabla maestro
	def obtenerValorClaveMaestro(self, clave:str)->Optional[str]:

		self.c.execute("""SELECT valor
						FROM maestro
						WHERE Clave=%s""",
						(clave,))

		valor=self.c.fetchone()

		return None if valor is None else valor["valor"]

	# Metodo para saber si la porra esta abierta
	def porraAbierta(self)->bool:

		fecha_cierre=self.obtenerValorClaveMaestro("fecha_cierre_porra")

		if fecha_cierre is None:

			return True

		return datetime.now()<=datetime.strptime(fecha_cierre, "%Y-%m-%d")