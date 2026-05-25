from flask import Blueprint, render_template, request, jsonify, redirect
from flask_login import login_required, current_user

from src.database.conexion import Conexion

from src.utilidades.utils import obtenerGruposEquiposLimpios, gruposPorraCorrectos


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

	data=request.get_json()

	if not data or "grupos" not in data:

		return redirect("/porra/grupos")

	grupos_equipos_porra=data["grupos"]

	usuario=current_user.id

	codigo_liga=current_user.codigo_liga

	con=Conexion()

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