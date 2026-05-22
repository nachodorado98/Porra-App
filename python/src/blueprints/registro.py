from flask import Blueprint, render_template, request, redirect
from flask import jsonify
import random
import string
from unittest.mock import patch
import requests
import os

from src.database.conexion import Conexion

from src.utilidades.utils import codigo_valido, datos_correctos, generarHash

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
def verificarCodigo(codigo):

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

    if not datos_correctos(usuario, nombre, apellido, contrasena, correo):

        return redirect("/registro")

    if not codigo_final or not codigo_valido(codigo_final):

        return redirect("/registro")

    if accion_liga not in ["crear", "unirse"]:
    
        return redirect("/registro")

    con=Conexion()

    if con.existe_usuario(usuario):

        con.cerrarConexion()

        return redirect("/registro")

    insertar_codigo_nuevo=True if accion_liga=="crear" else False

    if insertar_codigo_nuevo:

        existe_codigo=con.existe_codigo_liga(codigo_final)

        if existe_codigo:

            con.cerrarConexion()

            return redirect("/registro")

        con.insertarCodigoLiga(codigo_final)

    else:

        existe_codigo=con.existe_codigo_liga(codigo_final)

        if not existe_codigo:

            con.cerrarConexion()

            return redirect("/registro")

    hash_contrasena=generarHash(contrasena)

    con.insertarUsuario(usuario, correo, hash_contrasena, nombre, apellido, codigo_final)

    try:

        AZURE_FUNCTION=os.getenv("AZURE_FUNCTION", "nombre_azure_function")
        
        ENDPOINT_AZURE_FUNCTION=os.getenv("ENDPOINT_AZURE_FUNCTION", "endpoint_azure_function")

        URL_AZURE_FUNCTION=f"https://{AZURE_FUNCTION}.azurewebsites.net/api/{ENDPOINT_AZURE_FUNCTION}"

        payload={"correo_destino":correo, "nombre":nombre}

        response=requests.post(URL_AZURE_FUNCTION, json=payload)

    except Exception:

        pass

    return render_template("singup.html", nombre=nombre, nuevo=insertar_codigo_nuevo, codigo=codigo_final)