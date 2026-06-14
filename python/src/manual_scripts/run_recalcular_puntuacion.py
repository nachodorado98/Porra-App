import os
import sys
sys.path.append("../..")

from src.database.conexion import Conexion

from src.utilidades.utils import calcularPuntosTotalesGrupos, calcularPuntosTotalesMejoresTerceros


def recalcularPuntuacionUsuarios()->None:

	try:

		con=Conexion()

		usuarios_porra_completada=con.obtenerDatosUsuariosPorraCompleta()

		grupos_real=con.obtenerGruposRealPuntuacion()

		mejores_terceros_real=con.obtenerMejoresTercerosReal()

		eliminatorias_real=con.obtenerEliminatoriasReal()

		for usuario_porra, nombre, correo, codigo_liga in usuarios_porra_completada:

			print(f"Calculando usuario: {usuario_porra}", flush=True)

			grupos_porra=con.obtenerGruposPorraUsuarioPuntuacion(usuario_porra)

			puntos_grupos=calcularPuntosTotalesGrupos(grupos_real, grupos_porra)

			mejores_terceros_porra=con.obtenerMejoresTercerosUsuario(usuario_porra)

			puntos_mejores_terceros=calcularPuntosTotalesMejoresTerceros(mejores_terceros_real, mejores_terceros_porra)
			
			eliminatorias_porra=con.obtenerEliminatoriasPorraUsuario(usuario_porra)

			puntos_eliminatorias=calcularPuntosTotalesEliminatorias(eliminatorias_real, eliminatorias_porra)

			bonus_campeon=calcularBonusCampeonEliminatorias(eliminatorias_real, eliminatorias_porra)

			bonus_final=calcularBonusFinalExactaEliminatorias(eliminatorias_real, eliminatorias_porra)

			con.actualizarPuntuacionUsuarioSinCommit(usuario_porra, puntos_grupos, puntos_mejores_terceros, puntos_eliminatorias+bonus_campeon+bonus_final)

			print(f"Grupos: {puntos_grupos} pts | "
					f"Mejores terceros: {puntos_mejores_terceros} pts",
					f"Eliminatorias: {puntos_eliminatorias} pts",
					f"Bonus Campeon: {bonus_campeon} pts",
					f"Bonus Final: {bonus_final} pts",
					flush=True)

		con.confirmar()

		con.cerrarConexion()

		print("Puntos calculados correctamente", flush=True)

	except Exception as e:

	    con.cerrarConexion()

	    raise e

print("-"*50)
print("EJECUTAR CALCULAR PUNTOS PORRA")
print("-"*50)

recalcularPuntuacionUsuarios()