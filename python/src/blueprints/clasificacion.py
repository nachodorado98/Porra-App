from flask import Blueprint, render_template, redirect
from flask_login import login_required, current_user

from src.database.conexion import Conexion

from src.config import URL_DATALAKE_PERFIL


bp_clasificacion=Blueprint("clasificacion", __name__)

@bp_clasificacion.route("/clasificacion/<codigo>")
@login_required
def pagina_clasificacion(codigo:str):

	usuario=current_user.id

	codigo_liga=current_user.codigo_liga

	imagen_perfil=current_user.imagen_perfil

	paso_porra=current_user.paso_porra

	con=Conexion()

	if not con.existe_codigo_liga(codigo):

		con.cerrarConexion()

		return redirect("/porra")

	codigo_usuario=con.obtenerCodigoLigaUsuario(usuario)

	if codigo_usuario!=codigo:

		con.cerrarConexion()

		return redirect("/porra")

	assert codigo_usuario==codigo_liga

	usuarios_codigo_puntos=con.obtenerPuntuacionesUsuariosCodigoLiga(codigo)

	porra_abierta=con.porraAbierta()

	puede_ver_resultados=con.puedeVerResultados(usuario)

	con.cerrarConexion()

	puede_pinchar=False if not current_user.admin and porra_abierta else True

	return render_template("clasificacion.html",
							usuario=usuario,
							nombre=current_user.nombre,
							codigo_liga=codigo_liga,
							imagen_perfil=imagen_perfil,
							usuarios_codigo=usuarios_codigo_puntos,
							puede_pinchar=puede_pinchar,
							paso_porra=paso_porra,
							puede_ver_resultados=puede_ver_resultados,
							url_imagen_usuario_perfil=f"{URL_DATALAKE_PERFIL}")