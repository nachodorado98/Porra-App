from flask import Blueprint, render_template, redirect
from flask_login import login_required, current_user

from src.database.conexion import Conexion


bp_clasificacion=Blueprint("clasificacion", __name__)

@bp_clasificacion.route("/clasificacion/<codigo>")
@login_required
def pagina_clasificacion(codigo:str):

	usuario=current_user.id

	codigo_liga=current_user.codigo_liga

	con=Conexion()

	if not con.existe_codigo_liga(codigo):

		con.cerrarConexion()

		return redirect("/porra")

	codigo_usuario=con.obtenerCodigoLigaUsuario(usuario)

	assert codigo_usuario==codigo_liga

	if codigo_usuario!=codigo:

		con.cerrarConexion()

		return redirect("/porra")

	usuarios_codigo=con.obtenerUsuariosCodigoLiga(codigo)

	usuarios_codigo_puntos=sorted([tuple(list(usuario_codigo)+[int("0")]) for usuario_codigo in usuarios_codigo], key=lambda x: (x[3], x[1]), reverse=True)

	return render_template("clasificacion.html",
							usuario=usuario,
							nombre=current_user.nombre,
							codigo_liga=codigo_liga,
							usuarios_codigo=usuarios_codigo_puntos)