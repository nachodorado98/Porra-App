from flask import Blueprint, render_template, request, jsonify, redirect
from flask_login import login_required, current_user

from src.database.conexion import Conexion


bp_settings=Blueprint("settings", __name__)


@bp_settings.route("/settings")
@login_required
def pagina_settings():

	usuario=current_user.id

	codigo_liga=current_user.codigo_liga

	return render_template("settings.html",
							usuario=usuario,
							nombre=current_user.nombre,
							codigo_liga=codigo_liga)

@bp_settings.route("/settings/eliminar_cuenta")
@login_required
def pagina_settings_eliminar_cuenta():

	usuario=current_user.id

	codigo_liga=current_user.codigo_liga

	con=Conexion()

	try:

		con.eliminarUsuario(usuario)

		con.cerrarConexion()

		return redirect("/")

	except Exception:

		con.cerrarConexion()

		return redirect("/")