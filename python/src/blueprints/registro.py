from flask import Blueprint, render_template, request, redirect
from flask import jsonify
import random
import string

from src.utilidades.utils import codigo_valido, datos_correctos

bp_registro=Blueprint("registro", __name__)


@bp_registro.route("/registro")
def registro():

	return render_template("registro.html")

@bp_registro.route("/registro/generar_codigo")
def generarCodigo():

    DIGITOS=6

    caracteres=string.ascii_uppercase+string.digits

    codigo=''.join(random.choices(caracteres, k=DIGITOS))

    return jsonify({"codigo": codigo})

@bp_registro.route("/registro/verificar_codigo/<codigo>")
def verificarCodigo(codigo):

    valido=codigo_valido(codigo)

    return jsonify({"valido": valido})

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

    if not codigo_final:

        return redirect("/registro")

    if not codigo_valido(codigo_final):

        return redirect("/registro")

    insertar_codigo_nuevo=True if accion_liga=="crear" else False

    return render_template("singup.html", nombre=nombre, nuevo=insertar_codigo_nuevo, codigo=codigo_final)