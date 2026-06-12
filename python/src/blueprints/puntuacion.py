from flask import Blueprint, render_template, redirect
from flask_login import login_required, current_user

from src.database.conexion import Conexion

from src.config import URL_DATALAKE_PERFIL

from src.utilidades.utils import calcularPuntosTotalesGrupos, compararGruposDisponiblesDataFrameDetalle, calcularPuntosTotalesGrupos
from src.utilidades.utils import limpiarDataFrameDetalleGrupos, compararMejoresTercerosDataFrameDetalle, calcularPuntosTotalesMejoresTerceros


bp_puntuacion=Blueprint("puntuacion", __name__)

@bp_puntuacion.route("/puntuacion/calcular_puntuacion", methods=["PUT"])
@login_required
def pagina_puntuacion_calcular_puntuacion():

	usuario=current_user.id

	codigo_liga=current_user.codigo_liga

	imagen_perfil=current_user.imagen_perfil

	paso_porra=current_user.paso_porra

	try:

		con=Conexion()

		if not current_user.admin:

			con.cerrarConexion()

			return redirect("/porra")

		usuarios_porra_completada=con.obtenerDatosUsuariosPorraCompleta()

		grupos_real=con.obtenerGruposRealPuntuacion()

		mejores_terceros_real=con.obtenerMejoresTercerosReal()

		for usuario_porra, nombre, correo, codigo_liga in usuarios_porra_completada:

			print(f"Calculando usuario: {usuario_porra}", flush=True)

			grupos_porra=con.obtenerGruposPorraUsuarioPuntuacion(usuario_porra)

			puntos_grupos=calcularPuntosTotalesGrupos(grupos_real, grupos_porra)

			mejores_terceros_porra=con.obtenerMejoresTercerosUsuario(usuario_porra)

			puntos_mejores_terceros=calcularPuntosTotalesMejoresTerceros(mejores_terceros_real, mejores_terceros_porra)

			con.actualizarPuntuacionUsuarioSinCommit(usuario_porra, puntos_grupos, puntos_mejores_terceros, 0)

			print(f"Grupos: {puntos_grupos} pts | "
					f"Mejores terceros: {puntos_mejores_terceros} pts",
					flush=True)

		con.confirmar()

		con.cerrarConexion()

		print("Puntos calculados correctamente", flush=True)

		return redirect("/settings")

	except Exception as e:

		con.cerrarConexion()

		raise e

@bp_puntuacion.route("/puntuacion/detalle/<usuario_porra>")
@login_required
def pagina_puntuacion_detalle_usuario(usuario_porra:str):

	usuario=current_user.id

	codigo_liga=current_user.codigo_liga

	imagen_perfil=current_user.imagen_perfil

	paso_porra=current_user.paso_porra

	con=Conexion()

	if not con.existe_usuario(usuario_porra):

		con.cerrarConexion()

		return redirect("/porra")

	if usuario_porra!=usuario:

		con.cerrarConexion()

		return redirect("/porra")

	puede_ver_resultados=con.puedeVerResultados(usuario)

	if not puede_ver_resultados:

		con.cerrarConexion()

		return redirect("/porra")

	grupos_real=con.obtenerGruposRealPuntuacion()

	grupos_porra=con.obtenerGruposPorraUsuarioPuntuacion(usuario_porra)

	imagen_perfil_usuario_porra=con.obtenerImagenPerfilUsuario(usuario_porra)

	mejores_terceros_real=con.obtenerMejoresTercerosReal()

	mejores_terceros_porra=con.obtenerMejoresTercerosUsuario(usuario_porra)

	puede_ver_resultados=con.puedeVerResultados(usuario)

	con.cerrarConexion()

	df_detalle_grupos=compararGruposDisponiblesDataFrameDetalle(grupos_real, grupos_porra)

	puntos_grupos=calcularPuntosTotalesGrupos(grupos_real, grupos_porra)

	detalle_grupos_limpio=limpiarDataFrameDetalleGrupos(df_detalle_grupos)

	df_detalle_mejores_terceros=compararMejoresTercerosDataFrameDetalle(mejores_terceros_real, mejores_terceros_porra)

	detalle_mejores_terceros=df_detalle_mejores_terceros.to_dict("records")

	puntos_mejores_terceros=calcularPuntosTotalesMejoresTerceros(mejores_terceros_real, mejores_terceros_porra)

	puntos_total=puntos_grupos+puntos_mejores_terceros

	return render_template("detalle_puntuacion.html",
							usuario=usuario,
							nombre=current_user.nombre,
							codigo_liga=codigo_liga,
							imagen_perfil=imagen_perfil,
							usuario_porra=usuario_porra,
							imagen_perfil_usuario_porra=imagen_perfil_usuario_porra,
							detalle_grupos_limpio=detalle_grupos_limpio,
							puntos_grupos=puntos_grupos,
							detalle_mejores_terceros=detalle_mejores_terceros,
							puntos_mejores_terceros=puntos_mejores_terceros,
							puntos_total=puntos_total,
							paso_porra=paso_porra,
							puede_ver_resultados=puede_ver_resultados,
							url_imagen_usuario_perfil=f"{URL_DATALAKE_PERFIL}")