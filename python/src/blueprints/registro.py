from flask import Blueprint, render_template, request, redirect, flash
from flask import jsonify
import random
import string
from unittest.mock import patch
import requests
import os

from src.database.conexion import Conexion

from src.utilidades.utils import codigo_valido, usuario_correcto, nombre_correcto, apellido_correcto, contrasena_correcta
from src.utilidades.utils import correo_correcto, generarHash

bp_registro=Blueprint("registro", __name__)


@bp_registro.route("/registro")
def registro():

	return render_template("registro.html")

@bp_registro.route("/registro/generar_codigo")
def generarCodigo():

    DIGITOS=6

    caracteres=string.ascii_uppercase+string.digits

    codigo=''.join(random.choices(caracteres, k=DIGITOS))

    con=Conexion()

    existe_codigo=con.existe_codigo_liga(codigo)

    con.cerrarConexion()

    if not existe_codigo:

        return jsonify({"codigo": codigo}), 200

    else:
        
        return jsonify({"error": "Codigo No Valido"}), 404

@bp_registro.route("/registro/verificar_codigo/<codigo>")
def verificarCodigo(codigo:str):

    codigo_validado=codigo_valido(codigo)

    if not codigo_validado:
        
        return jsonify({"error": "Codigo No Valido"}), 404

    con=Conexion()

    existe_codigo=con.existe_codigo_liga(codigo)

    con.cerrarConexion()

    if existe_codigo:

        return jsonify({"valido": codigo_validado}), 200

    else:
        
        return jsonify({"error": "Codigo No Existente"}), 404

@bp_registro.route("/singup", methods=["POST"])
def singup():

    usuario=request.form.get("usuario")
    correo=request.form.get("correo")
    contrasena=request.form.get("contrasena")
    nombre=request.form.get("nombre")
    apellido=request.form.get("apellido")
    accion_liga=request.form.get("accion_liga")
    codigo_final=request.form.get("codigo_final")

    if not usuario_correcto(usuario):

        flash("El usuario no es válido", "error")

        return redirect("/registro")

    if not contrasena_correcta(contrasena):

        flash("La contraseña debe tener al menos 8 caracteres y no contener espacios", "error")

        return redirect("/registro")

    if not nombre_correcto(nombre):

        flash("El nombre introducido no es válido", "error")

        return redirect("/registro")

    if not apellido_correcto(apellido):

        flash("El apellido introducido no es válido", "error")

        return redirect("/registro")

    if not correo_correcto(correo):

        flash("El correo electrónico no es válido", "error")

        return redirect("/registro")

    if not codigo_final or not codigo_valido(codigo_final):

        flash("El código de liga no es válido", "error")

        return redirect("/registro")

    if accion_liga not in ["crear", "unirse"]:

        flash("Debes seleccionar si quieres crear o unirte a una liga", "error")
    
        return redirect("/registro")

    con=Conexion()

    if not con.porraAbierta():

        flash("El registro está cerrado actualmente", "error")

        con.cerrarConexion()

        return redirect("/registro")

    if con.existe_usuario(usuario):

        flash("El usuario introducido ya existe", "error")

        con.cerrarConexion()

        return redirect("/registro")

    if con.existe_correo(correo):

        flash("El correo introducido ya está registrado", "error")

        con.cerrarConexion()

        return redirect("/registro")

    insertar_codigo_nuevo=True if accion_liga=="crear" else False

    if insertar_codigo_nuevo:

        existe_codigo=con.existe_codigo_liga(codigo_final)

        if existe_codigo:

            flash("El código de liga introducido ya existe", "error")

            con.cerrarConexion()

            return redirect("/registro")

        con.insertarCodigoLiga(codigo_final)

    else:

        existe_codigo=con.existe_codigo_liga(codigo_final)

        if not existe_codigo:

            flash("El código de liga introducido no existe", "error")

            con.cerrarConexion()

            return redirect("/registro")

    hash_contrasena=generarHash(contrasena)

    con.insertarUsuario(usuario, correo, hash_contrasena, nombre, apellido, codigo_final)

    con.insertarEstadoPorraUsuario(usuario)

    con.insertarPuntuacionUsuario(usuario)

    try:

        AZURE_FUNCTION=os.getenv("AZURE_FUNCTION", "nombre_azure_function")
        
        ENDPOINT_AZURE_FUNCTION=os.getenv("ENDPOINT_AZURE_FUNCTION", "endpoint_azure_function")

        URL_AZURE_FUNCTION=f"https://{AZURE_FUNCTION}.azurewebsites.net/api/{ENDPOINT_AZURE_FUNCTION}"

        payload={"correo_destino":correo, "nombre":nombre, "usuario":usuario, "codigo":codigo_final, "tipo":"bienvenida"}

        response=requests.post(URL_AZURE_FUNCTION, json=payload, timeout=10)

    except Exception:

        pass

    return render_template("singup.html", nombre=nombre, nuevo=insertar_codigo_nuevo, codigo=codigo_final)