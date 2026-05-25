from flask import Blueprint, render_template
from flask_login import login_required, current_user

from src.database.conexion import Conexion

from src.utilidades.utils import obtenerGruposEquiposLimpios


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