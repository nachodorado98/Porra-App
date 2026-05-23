from flask import Blueprint, render_template
from flask_login import login_required, current_user

from src.database.conexion import Conexion


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