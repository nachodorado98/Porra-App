from flask import Blueprint, render_template
import random
import string
from flask import jsonify

bp_registro=Blueprint("registro", __name__)


@bp_registro.route("/registro")
def registro():

	return render_template("registro.html")

@bp_registro.route("/registro/generar_codigo")
def generar_codigo():

    DIGITOS=6

    caracteres=string.ascii_uppercase+string.digits

    codigo=''.join(random.choices(caracteres, k=DIGITOS))

    return jsonify({"codigo": codigo})

@bp_registro.route("/registro/verificar_codigo/<codigo>")
def verificar_codigo(codigo):

    codigo_upper=codigo.upper()

    valido=True if codigo_upper.isalnum() and codigo_upper.isupper() and len(codigo_upper)==6 else False

    return jsonify({"valido": valido})