from flask import Blueprint, render_template, request, jsonify, redirect
from flask_login import login_required, current_user
import os

from src.database.conexion import Conexion

from src.utilidades.utils import crearCarpeta, extraerExtension, vaciarCarpeta


bp_settings=Blueprint("settings", __name__)


@bp_settings.route("/settings")
@login_required
def pagina_settings():

	usuario=current_user.id

	codigo_liga=current_user.codigo_liga

	imagen_perfil=current_user.imagen_perfil

	return render_template("settings.html",
							usuario=usuario,
							nombre=current_user.nombre,
							codigo_liga=codigo_liga,
							imagen_perfil=imagen_perfil)

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

@bp_settings.route("/settings/actualizar_imagen_perfil", methods=["POST"])
@login_required
def pagina_settings_actualizar_imagen_perfil():

	usuario=current_user.id

	codigo_liga=current_user.codigo_liga

	imagen_perfil=current_user.imagen_perfil

	archivos=request.files

	con=Conexion()

	ruta=os.path.dirname(os.path.join(os.path.dirname(__file__)))

	crearCarpeta(os.path.join(ruta, "static", "imagenes", "perfil", usuario))

	if "imagen" in archivos:

		imagen=archivos["imagen"]

		extension=extraerExtension(imagen.filename)

		if imagen.filename!="" and extension in ("png", "jpg", "jpeg"):

			ruta_carpeta=os.path.join(ruta, "static", "imagenes", "perfil", usuario)

			vaciarCarpeta(ruta_carpeta)

			archivo_imagen=f"{usuario}_perfil.{extension}"

			ruta_imagen=os.path.join(ruta_carpeta, archivo_imagen)

			try:

				imagen.save(ruta_imagen)

				con.actualizarImagenPerfilUsuario(usuario, archivo_imagen)

			except Exception:

				print(f"Error al subir imagen {archivo_imagen}")

	con.cerrarConexion()

	return redirect("/settings")