from flask import Blueprint, render_template, request, jsonify, redirect
from flask_login import login_required, current_user

from src.database.conexion import Conexion

from src.utilidades.utils import obtenerGruposEquiposLimpios, gruposPorraCorrectos, obtenerTercerosGruposEquiposLimpios


bp_porra=Blueprint("porra", __name__)

@bp_porra.route("/porra")
@login_required
def pagina_porra():

	usuario=current_user.id

	codigo_liga=current_user.codigo_liga

	return render_template("porra.html",
							usuario=usuario,
							nombre=current_user.nombre,
							codigo_liga=codigo_liga)

@bp_porra.route("/porra/grupos")
@login_required
def pagina_porra_grupos():

	usuario=current_user.id

	codigo_liga=current_user.codigo_liga

	con=Conexion()

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
							grupos=grupos_limpios)

@bp_porra.route("/porra/grupos/guardar", methods=["POST"])
@login_required
def pagina_porra_grupos_guardar():

	usuario=current_user.id

	codigo_liga=current_user.codigo_liga

	con=Conexion()

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

	con=Conexion()

	grupos_completos=con.gruposPorraCompleto(usuario)

	if not grupos_completos:

		con.cerrarConexion()

		return redirect("/porra/grupos")

	terceros_grupos=con.obtenerTercerosGruposUsuario(usuario)

	con.cerrarConexion()

	terceros_grupos_limpios=obtenerTercerosGruposEquiposLimpios(terceros_grupos)

	return render_template("porra_mejores_terceros.html",
							usuario=usuario,
							nombre=current_user.nombre,
							codigo_liga=codigo_liga,
							terceros=terceros_grupos_limpios)