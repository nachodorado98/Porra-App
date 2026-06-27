from flask import Blueprint, render_template, request, redirect, flash
import secrets
import requests
from datetime import datetime, timedelta
import os

from src.database.conexion import Conexion

from src.utilidades.utils import generarHashToken


bp_forgot_password=Blueprint("forgot_password", __name__)


@bp_forgot_password.route("/forgot_password")
def forgot_password():

	return render_template("forgot_password.html")

@bp_forgot_password.route("/forgot_password/solicitar", methods=["POST"])
def forgot_password_solicitar():

	correo=request.form.get("correo")

	con=Conexion()

	usuario_correo_nombre=con.obtenerUsuarioPorCorreo(correo)

	if not usuario_correo_nombre:

		flash("El correo introducido no existe", "error")

		con.cerrarConexion()

		return redirect("/forgot_password")

	if con.existe_token_reciente(usuario_correo_nombre[0]):

		flash("Ya se ha enviado un enlace recientemente. Espera unos minutos antes de solicitar otro", "error")

		con.cerrarConexion()

		return redirect("/forgot_password")

	token=secrets.token_urlsafe(32)

	hash_token=generarHashToken(token)

	expires_at=datetime.now()+timedelta(minutes=30)

	con.actualizarTokensUsuario(usuario_correo_nombre[0])

	con.insertarToken(usuario_correo_nombre[0], hash_token, expires_at)

	try:

		AZURE_FUNCTION=os.getenv("AZURE_FUNCTION", "nombre_azure_function")
		
		ENDPOINT_AZURE_FUNCTION=os.getenv("ENDPOINT_AZURE_FUNCTION", "endpoint_azure_function")

		URL_AZURE_FUNCTION=f"https://{AZURE_FUNCTION}.azurewebsites.net/api/{ENDPOINT_AZURE_FUNCTION}"

		payload={"correo_destino":correo, "nombre":usuario_correo_nombre[2], "usuario":usuario_correo_nombre[0], "token":token, "tipo":"reset_password"}

		response=requests.post(URL_AZURE_FUNCTION, json=payload, timeout=10)

	except Exception:

		flash("El correo no ha sido enviado", "error")

		con.cerrarConexion()

		return redirect("/forgot_password")

	flash("El correo de recuperacion ha sido enviado", "correcto")

	con.cerrarConexion()

	return redirect("/")