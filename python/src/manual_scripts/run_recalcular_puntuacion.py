import os
import sys
sys.path.append("../..")

from src.database.conexion import Conexion

from src.utilidades.utils import calcularPuntosTotalesGrupos


def recalcularPuntuacionUsuarios()->None:

	try:

		con=Conexion()

		usuarios_porra_completada=con.obtenerDatosUsuariosPorraCompleta()

		grupos_real=con.obtenerGruposRealPuntuacion()

		for usuario_porra, nombre, correo, codigo_liga in usuarios_porra_completada:

			grupos_porra=con.obtenerGruposPorraUsuarioPuntuacion(usuario_porra)

			puntos_grupos=calcularPuntosTotalesGrupos(grupos_real, grupos_porra)

			con.actualizarPuntuacionUsuarioSinCommit(usuario_porra, puntos_grupos, 0, 0)

			print(f"{usuario_porra}: {puntos_grupos} puntos")

		con.confirmar()

		con.cerrarConexion()

		print("Puntos calculados correctamente", flush=True)

	except Exception as e:

	    con.cerrarConexion()

	    raise e


recalcularPuntuacionUsuarios()