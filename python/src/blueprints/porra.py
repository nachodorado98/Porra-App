from flask import Blueprint, render_template, request, jsonify, redirect
from flask_login import login_required, current_user
import json

from src.database.conexion import Conexion

from src.utilidades.utils import obtenerGruposEquiposLimpios, gruposPorraCorrectos, obtenerTercerosGruposEquiposLimpios, mejoresTercerosPorraCorrectos
from src.utilidades.utils import obtenerPasosPorra, obtenerCombinacionMejoresTerceros, crearBracketDieciseisavos, bracketEliminatoriasCorrecto
from src.utilidades.utils import obtenerEliminatoriasPorraLimpias

from src.config import URL_DATALAKE_PERFIL


bp_porra=Blueprint("porra", __name__)

@bp_porra.route("/porra")
@login_required
def pagina_porra():

	usuario=current_user.id

	codigo_liga=current_user.codigo_liga

	imagen_perfil=current_user.imagen_perfil

	paso_porra=current_user.paso_porra

	con=Conexion()

	porra_abierta=con.porraAbierta()

	con.cerrarConexion()

	return render_template("porra.html",
							usuario=usuario,
							nombre=current_user.nombre,
							codigo_liga=codigo_liga,
							imagen_perfil=imagen_perfil,
							paso_porra=paso_porra,
							porra_abierta=porra_abierta,
							url_imagen_usuario_perfil=f"{URL_DATALAKE_PERFIL}")

@bp_porra.route("/porra/grupos")
@login_required
def pagina_porra_grupos():

	usuario=current_user.id

	codigo_liga=current_user.codigo_liga

	imagen_perfil=current_user.imagen_perfil

	paso_porra=current_user.paso_porra

	con=Conexion()

	if not con.porraAbierta():

		con.cerrarConexion()

		return redirect("/porra")

	puede_editar=con.puedeEditarGruposPorra(usuario)

	if not puede_editar:

		con.cerrarConexion()

		return redirect("/porra")

	grupos=con.obtenerGruposEquipos()

	con.cerrarConexion()

	grupos_limpios=obtenerGruposEquiposLimpios(grupos)

	return render_template("porra_grupos.html",
							usuario=usuario,
							nombre=current_user.nombre,
							codigo_liga=codigo_liga,
							imagen_perfil=imagen_perfil,
							grupos=grupos_limpios,
							paso_porra=paso_porra,
							url_imagen_usuario_perfil=f"{URL_DATALAKE_PERFIL}")

@bp_porra.route("/porra/grupos/guardar", methods=["POST"])
@login_required
def pagina_porra_grupos_guardar():

	usuario=current_user.id

	codigo_liga=current_user.codigo_liga

	imagen_perfil=current_user.imagen_perfil

	con=Conexion()

	if not con.porraAbierta():

		con.cerrarConexion()

		return redirect("/porra")

	puede_editar=con.puedeEditarGruposPorra(usuario)

	if not puede_editar:

		con.cerrarConexion()

		return redirect("/porra")

	data=request.get_json()

	if not data or "grupos" not in data:

		con.cerrarConexion()

		return redirect("/porra/grupos")

	grupos_equipos_porra=data["grupos"]

	grupos_equipos_real=con.obtenerGruposEquipos()

	if not gruposPorraCorrectos(grupos_equipos_real, grupos_equipos_porra):

		con.cerrarConexion()

		return redirect("/porra/grupos")

	try:

		for grupo, equipos_grupo_porra in grupos_equipos_porra.items():

			con.insertarEquipoGruposPorraUsuario(usuario, grupo, equipos_grupo_porra)

		con.actualizarEstadoPorraGruposUsuario(usuario)

		con.cerrarConexion()

		return redirect("/porra/mejores_terceros")

	except Exception:

		con.cerrarConexion()

		return redirect("/porra/grupos")

@bp_porra.route("/porra/mejores_terceros")
@login_required
def pagina_porra_mejores_terceros():

	usuario=current_user.id

	codigo_liga=current_user.codigo_liga

	imagen_perfil=current_user.imagen_perfil

	paso_porra=current_user.paso_porra

	con=Conexion()

	if not con.porraAbierta():

		con.cerrarConexion()

		return redirect("/porra")

	grupos_completos=con.gruposPorraCompleto(usuario)

	if not grupos_completos:

		con.cerrarConexion()

		return redirect("/porra/grupos")

	puede_editar=con.puedeEditarMejoresTercerosPorra(usuario)

	if not puede_editar:

		con.cerrarConexion()

		return redirect("/porra")

	terceros_grupos=con.obtenerTercerosGruposUsuario(usuario)

	con.cerrarConexion()

	terceros_grupos_limpios=obtenerTercerosGruposEquiposLimpios(terceros_grupos)

	return render_template("porra_mejores_terceros.html",
							usuario=usuario,
							nombre=current_user.nombre,
							codigo_liga=codigo_liga,
							imagen_perfil=imagen_perfil,
							terceros=terceros_grupos_limpios,
							paso_porra=paso_porra,
							url_imagen_usuario_perfil=f"{URL_DATALAKE_PERFIL}")

@bp_porra.route("/porra/mejores_terceros/guardar", methods=["POST"])
@login_required
def pagina_porra_mejores_terceros_guardar():

	usuario=current_user.id

	codigo_liga=current_user.codigo_liga

	imagen_perfil=current_user.imagen_perfil

	con=Conexion()

	if not con.porraAbierta():

		con.cerrarConexion()

		return redirect("/porra")

	grupos_completos=con.gruposPorraCompleto(usuario)

	if not grupos_completos:

		con.cerrarConexion()

		return redirect("/porra/grupos")

	puede_editar=con.puedeEditarMejoresTercerosPorra(usuario)

	if not puede_editar:

		con.cerrarConexion()

		return redirect("/porra")

	data=request.get_json()

	if not data or "equipos" not in data:

		con.cerrarConexion()

		return redirect("/porra/mejores_terceros")

	mejores_terceros_equipos_porra=data["equipos"]

	terceros_grupos_reales_usuario=con.obtenerTercerosGruposUsuario(usuario)

	if not mejoresTercerosPorraCorrectos(terceros_grupos_reales_usuario, mejores_terceros_equipos_porra):

		con.cerrarConexion()

		return redirect("/porra/mejores_terceros")

	try:

		mejores_terceros_equipos_porra_insertar=[(mejor_tercer_equipo_porra["grupo"], mejor_tercer_equipo_porra["equipo_id"])
													for mejor_tercer_equipo_porra in mejores_terceros_equipos_porra]

		con.insertarEquipoMejoresTercerosPorraUsuario(usuario, mejores_terceros_equipos_porra_insertar)

		con.actualizarEstadoPorraMejoresTercerosUsuario(usuario)

		con.cerrarConexion()

		return redirect("/porra/eliminatorias")

	except Exception:

		con.cerrarConexion()

		return redirect("/porra/mejores_terceros")

@bp_porra.route("/porra/eliminatorias")
@login_required
def pagina_porra_eliminatorias():

	usuario=current_user.id

	codigo_liga=current_user.codigo_liga

	imagen_perfil=current_user.imagen_perfil

	paso_porra=current_user.paso_porra

	con=Conexion()

	if not con.porraAbierta():

		con.cerrarConexion()

		return redirect("/porra")

	mejores_terceros_completos=con.mejoresTercerosPorraCompleto(usuario)

	if not mejores_terceros_completos:

		con.cerrarConexion()

		return redirect("/porra/mejores_terceros")

	puede_editar=con.puedeEditarEliminatoriasPorra(usuario)

	if not puede_editar:

		con.cerrarConexion()

		return redirect("/porra")

	primeros_segundos=con.obtenerPrimerosSegundosGruposUsuario(usuario)

	mejores_terceros_grupos=con.obtenerMejoresTercerosUsuario(usuario)

	combinacion_mejores_terceros=obtenerCombinacionMejoresTerceros(mejores_terceros_grupos)

	partidos_variables_equipo_tercero=con.obtenerCombinacionPartidosMejoresTerceros(combinacion_mejores_terceros)

	con.cerrarConexion()

	bracket_16avos=crearBracketDieciseisavos(partidos_variables_equipo_tercero, primeros_segundos, mejores_terceros_grupos)

	return render_template("porra_eliminatorias.html",
							usuario=usuario,
							nombre=current_user.nombre,
							codigo_liga=codigo_liga,
							imagen_perfil=imagen_perfil,
							bracket_16avos=bracket_16avos,
							paso_porra=paso_porra,
							url_imagen_usuario_perfil=f"{URL_DATALAKE_PERFIL}")

@bp_porra.route("/porra/eliminatorias/guardar", methods=["POST"])
@login_required
def pagina_porra_eliminatorias_guardar():

	usuario=current_user.id

	codigo_liga=current_user.codigo_liga

	con=Conexion()

	if not con.porraAbierta():

		con.cerrarConexion()

		return redirect("/porra")

	mejores_terceros_completos=con.mejoresTercerosPorraCompleto(usuario)

	if not mejores_terceros_completos:

		con.cerrarConexion()

		return redirect("/porra/mejores_terceros")

	puede_editar=con.puedeEditarEliminatoriasPorra(usuario)

	if not puede_editar:

		con.cerrarConexion()

		return redirect("/porra")

	bracket_json=request.form.get("elecciones_eliminatorias")

	try:

		bracket=json.loads(bracket_json)

	except Exception:

		con.cerrarConexion()

		return redirect("/porra/eliminatorias")

	primeros_segundos=con.obtenerPrimerosSegundosGruposUsuario(usuario)

	mejores_terceros_grupos=con.obtenerMejoresTercerosUsuario(usuario)

	combinacion_mejores_terceros=obtenerCombinacionMejoresTerceros(mejores_terceros_grupos)

	partidos_variables_equipo_tercero=con.obtenerCombinacionPartidosMejoresTerceros(combinacion_mejores_terceros)

	bracket_16avos=crearBracketDieciseisavos(partidos_variables_equipo_tercero, primeros_segundos, mejores_terceros_grupos)

	if not bracketEliminatoriasCorrecto(bracket, bracket_16avos):

		con.cerrarConexion()

		return redirect("/porra/eliminatorias")

	try:

		bracket_porra_insertar=[(bracket_porra["ronda"], bracket_porra["partido"], bracket_porra["equipo_1_id"], bracket_porra["equipo_2_id"], bracket_porra["ganador_id"])
								for bracket_porra in bracket]

		con.insertarPartidosEliminatoriasPorraUsuario(usuario, bracket_porra_insertar)

		con.actualizarEstadoPorraEliminatoriasUsuario(usuario)

		con.actualizarEstadoPorraUsuario(usuario)

		con.cerrarConexion()

		return redirect("/porra/mi_porra")

	except Exception:

		con.cerrarConexion()

		return redirect("/porra/eliminatorias")

@bp_porra.route("/porra/reiniciar")
@login_required
def pagina_porra_reiniciar():

	usuario=current_user.id

	codigo_liga=current_user.codigo_liga

	imagen_perfil=current_user.imagen_perfil

	con=Conexion()

	try:

		if not con.porraAbierta():

			con.cerrarConexion()

			return redirect("/porra")

		con.reiniciarGruposPorraUsuario(usuario)

		con.reiniciarMejoresTercerosPorraUsuario(usuario)

		con.reiniciarEliminatoriasPorraUsuario(usuario)

		con.reiniciarEstadoPorraUsuario(usuario)

		con.cerrarConexion()

		return redirect("/porra")

	except Exception:

		con.cerrarConexion()

		return redirect("/porra")

@bp_porra.route("/porra/mi_porra")
@login_required
def pagina_porra_mi_porra():

	usuario=current_user.id

	codigo_liga=current_user.codigo_liga

	imagen_perfil=current_user.imagen_perfil

	paso_porra=current_user.paso_porra

	con=Conexion()

	puede_ver_porra=con.puedeVisualizarPorra(usuario)

	if not puede_ver_porra:

		con.cerrarConexion()

		return redirect("/porra")

	grupos_porra=con.obtenerGruposPorraUsuario(usuario)

	mejores_terceros_porra=con.obtenerMejoresTercerosUsuario(usuario)

	eliminatorias_porra=con.obtenerEliminatoriasPorraUsuario(usuario)

	con.cerrarConexion()

	grupos_porra_limpios=obtenerGruposEquiposLimpios(grupos_porra)

	mejores_terceros_porra_limpios=obtenerTercerosGruposEquiposLimpios(mejores_terceros_porra)

	eliminatorias_porra_limpias=obtenerEliminatoriasPorraLimpias(eliminatorias_porra)

	return render_template("mi_porra.html",
							usuario=usuario,
							nombre=current_user.nombre,
							codigo_liga=codigo_liga,
							imagen_perfil=imagen_perfil,
							grupos_porra=grupos_porra_limpios,
							mejores_terceros=mejores_terceros_porra_limpios,
							eliminatorias=eliminatorias_porra_limpias,
							paso_porra=paso_porra,
							url_imagen_usuario_perfil=f"{URL_DATALAKE_PERFIL}")

@bp_porra.route("/porra/<usuario_porra>")
@login_required
def pagina_porra_usuario(usuario_porra:str):

	usuario=current_user.id

	codigo_liga=current_user.codigo_liga

	imagen_perfil=current_user.imagen_perfil

	paso_porra=current_user.paso_porra

	con=Conexion()

	if not con.existe_usuario(usuario_porra):

		con.cerrarConexion()

		return redirect("/porra")

	porra_abierta=con.porraAbierta()

	if not current_user.admin and porra_abierta:

		con.cerrarConexion()

		return redirect("/porra")

	puede_ver_porra=con.puedeVisualizarPorra(usuario_porra)

	if not puede_ver_porra:

		con.cerrarConexion()

		return redirect("/porra")

	if usuario_porra==usuario:

		return redirect("/porra/mi_porra")

	grupos_porra=con.obtenerGruposPorraUsuario(usuario_porra)

	mejores_terceros_porra=con.obtenerMejoresTercerosUsuario(usuario_porra)

	eliminatorias_porra=con.obtenerEliminatoriasPorraUsuario(usuario_porra)

	imagen_perfil_usuario_porra=con.obtenerImagenPerfilUsuario(usuario_porra)

	con.cerrarConexion()

	grupos_porra_limpios=obtenerGruposEquiposLimpios(grupos_porra)

	mejores_terceros_porra_limpios=obtenerTercerosGruposEquiposLimpios(mejores_terceros_porra)

	eliminatorias_porra_limpias=obtenerEliminatoriasPorraLimpias(eliminatorias_porra)

	return render_template("porra_usuario.html",
							usuario=usuario,
							nombre=current_user.nombre,
							codigo_liga=codigo_liga,
							imagen_perfil=imagen_perfil,
							grupos_porra=grupos_porra_limpios,
							mejores_terceros=mejores_terceros_porra_limpios,
							eliminatorias=eliminatorias_porra_limpias,
							usuario_porra=usuario_porra,
							imagen_perfil_usuario_porra=imagen_perfil_usuario_porra,
							paso_porra=paso_porra,
							url_imagen_usuario_perfil=f"{URL_DATALAKE_PERFIL}")