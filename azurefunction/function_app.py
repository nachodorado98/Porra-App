import azure.functions as func
import datetime
import json
import logging

from utils import enviarCorreo

from config import EMAIL_ACCOUNT, CONTRASENA_LOGIN, SERVIDOR_CORREO, PUERTO_CORREO, ASUNTO_CORREO_BIENVENIDA, HTML_CORREO_BIENVENIDA
from config import ASUNTO_CORREO_LANZAMIENTO, HTML_CORREO_LANZAMIENTO, URL_APP

app = func.FunctionApp()

@app.route(route="enviarCorreoBienvenida", auth_level=func.AuthLevel.ANONYMOUS)
def enviarCorreoBienvenida(req: func.HttpRequest) -> func.HttpResponse:

    logging.info('Python HTTP trigger function processed a request.')

    try:

        body=req.get_json()
        nombre=body["nombre"]
        codigo=body["codigo"]
        correo_destino=body["correo_destino"]

    except Exception:

        return func.HttpResponse(json.dumps({"ok": False, "error": "El body no es correcto"}),
                                status_code=500,
                                mimetype="application/json")

    try:

        nombre_usuario=nombre if nombre else "DESCONOCIDO"

        enviarCorreo(correo_destino, ASUNTO_CORREO_BIENVENIDA, HTML_CORREO_BIENVENIDA.format(nombre=nombre_usuario, codigo=codigo), EMAIL_ACCOUNT, CONTRASENA_LOGIN, SERVIDOR_CORREO, PUERTO_CORREO)

        return func.HttpResponse(json.dumps({"ok": True}),
                                status_code=500,
                                mimetype="application/json")

    except Exception as e:

        logging.error(str(e))

        return func.HttpResponse(json.dumps({"ok": False, "error": str(e)}),
                                status_code=500,
                                mimetype="application/json")

@app.route(route="enviarCorreoLanzamiento", auth_level=func.AuthLevel.ANONYMOUS)
def enviarCorreoLanzamiento(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:

        body=req.get_json()
        nombre=body["nombre"]
        usuario=body["usuario"]
        codigo=body["codigo"]
        correo_destino=body["correo_destino"]

    except Exception:

        return func.HttpResponse(json.dumps({"ok": False, "error": "El body no es correcto"}),
                                status_code=500,
                                mimetype="application/json")

    try:

        nombre_usuario=nombre if nombre else "DESCONOCIDO"

        enviarCorreo(correo_destino, ASUNTO_CORREO_LANZAMIENTO, HTML_CORREO_LANZAMIENTO.format(nombre=nombre_usuario, usuario=usuario, codigo=codigo, url_app=URL_APP), EMAIL_ACCOUNT, CONTRASENA_LOGIN, SERVIDOR_CORREO, PUERTO_CORREO)

        return func.HttpResponse(json.dumps({"ok": True}),
                                status_code=500,
                                mimetype="application/json")

    except Exception as e:

        logging.error(str(e))

        return func.HttpResponse(json.dumps({"ok": False, "error": str(e)}),
                                status_code=500,
                                mimetype="application/json")