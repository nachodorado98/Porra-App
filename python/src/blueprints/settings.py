from flask import Blueprint, render_template, request, jsonify, redirect
from flask_login import login_required, current_user
import os
from datetime import datetime, timedelta
from threading import Thread
import time

from src.database.conexion import Conexion

from src.utilidades.utils import crearCarpeta, extraerExtension, vaciarCarpeta, contrasena_correcta, comprobarHash, generarHash
from src.utilidades.utils import crearCarpetaDataLakePerfilUsuario, subirImagenPerfilUsuarioDataLake

from src.config import URL_DATALAKE_PERFIL, CONTENEDOR_DL


bp_settings=Blueprint("settings", __name__)


@bp_settings.route("/settings")
@login_required
def pagina_settings():

	usuario=current_user.id

	codigo_liga=current_user.codigo_liga

	imagen_perfil=current_user.imagen_perfil

	paso_porra=current_user.paso_porra

	con=Conexion()

	puede_cambio_contrasena=con.puedeCambiarContrasena(usuario)

	con.cerrarConexion()

	return render_template("settings.html",
							usuario=usuario,
							nombre=current_user.nombre,
							codigo_liga=codigo_liga,
							imagen_perfil=imagen_perfil,
							puede_cambio_contrasena=puede_cambio_contrasena,
							es_admin=current_user.admin,
							paso_porra=paso_porra,
							url_imagen_usuario_perfil=f"{URL_DATALAKE_PERFIL}")

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

			if not crearCarpetaDataLakePerfilUsuario(usuario, CONTENEDOR_DL):

				con.cerrarConexion()

				print(f"No se pudo crear la carpeta de perfil en DataLake para {usuario}")

				return redirect("/settings")

			archivo_imagen=f"{usuario}_perfil.{extension}"

			ruta_imagen=os.path.join(ruta_carpeta, archivo_imagen)

			try:

				imagen.save(ruta_imagen)

				Thread(target=subirImagenPerfilUsuarioDataLake, args=(usuario, archivo_imagen, ruta_carpeta, CONTENEDOR_DL), daemon=True).start()

				time.sleep(2)
				
				con.actualizarImagenPerfilUsuario(usuario, archivo_imagen)

			except Exception:

				print(f"Error al subir imagen {archivo_imagen}")

	con.cerrarConexion()

	return redirect("/settings")

@bp_settings.route("/settings/cambiar_contrasena", methods=["POST"])
@login_required
def pagina_settings_cambiar_contrasena():

	usuario=current_user.id

	codigo_liga=current_user.codigo_liga

	contrasena_actual=request.form.get("contrasena_actual")
	nueva_contrasena=request.form.get("nueva_contrasena")
	repetir_contrasena=request.form.get("repetir_contrasena")

	if not contrasena_actual or not nueva_contrasena or not repetir_contrasena:

		return redirect("/settings")

	if contrasena_actual==nueva_contrasena:

		return redirect("/settings")
		
	if nueva_contrasena!=repetir_contrasena:

		return redirect("/settings")

	if not contrasena_correcta(nueva_contrasena):

		return redirect("/settings")

	con=Conexion()

	if not con.puedeCambiarContrasena(usuario):

		con.cerrarConexion()

		return redirect("/settings")

	contrasena_hash_usuario=con.obtenerContrasenaUsuario(usuario)

	if not comprobarHash(contrasena_actual, contrasena_hash_usuario):

		con.cerrarConexion()

		return redirect("/settings")

	if comprobarHash(nueva_contrasena, contrasena_hash_usuario):

		con.cerrarConexion()

		return redirect("/settings")

	nueva_contrasena_hash=generarHash(nueva_contrasena)

	cambios, ultimo_cambio=con.obtenerDatosCambioContrasenaUsuario(usuario)

	ahora=datetime.now()

	con.actualizarContrasenaUsuario(usuario, nueva_contrasena_hash, cambios+1, ahora)
	
	con.cerrarConexion()

	return redirect("/settings")

@bp_settings.route("/settings/verificar_usuario/<usuario>")
def verificarUsuario(usuario:str):

	usuario=usuario.strip()

	if not usuario:

		return jsonify({"error": "Usuario vacío"}), 400

	con=Conexion()

	existe_usuario=con.existe_usuario(usuario)

	con.cerrarConexion()

	if existe_usuario:

		return jsonify({"valido": True}), 200

	else:

		return jsonify({"error": "Usuario no existente"}), 404

@bp_settings.route("/settings/admin/cambiar_contrasena_usuario", methods=["POST"])
@login_required
def pagina_settings_admin_cambiar_contrasena_usuario():

	usuario=current_user.id

	codigo_liga=current_user.codigo_liga

	imagen_perfil=current_user.imagen_perfil

	usuario_cambiar=request.form.get("usuario")
	nueva_contrasena=request.form.get("nueva_contrasena")

	con=Conexion()

	if not current_user.admin:

		con.cerrarConexion()

		return redirect("/settings")

	if not con.existe_usuario(usuario_cambiar):

		con.cerrarConexion()

		return redirect("/settings")

	if not contrasena_correcta(nueva_contrasena):

		con.cerrarConexion()

		return redirect("/settings")

	contrasena_hash_usuario_cambiar=con.obtenerContrasenaUsuario(usuario_cambiar)

	if comprobarHash(nueva_contrasena, contrasena_hash_usuario_cambiar):

		con.cerrarConexion()

		return redirect("/settings")

	nueva_contrasena_hash=generarHash(nueva_contrasena)

	cambios, ultimo_cambio=con.obtenerDatosCambioContrasenaUsuario(usuario_cambiar)

	con.actualizarContrasenaUsuario(usuario_cambiar, nueva_contrasena_hash, cambios, ultimo_cambio)
	
	con.cerrarConexion()

	return redirect("/settings")