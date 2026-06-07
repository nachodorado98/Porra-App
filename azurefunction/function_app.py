import azure.functions as func
import datetime
import json
import logging

from utils import enviarCorreoBase

from config import EMAIL_ACCOUNT, CONTRASENA_LOGIN, SERVIDOR_CORREO, PUERTO_CORREO, ASUNTO_CORREO_BIENVENIDA, HTML_CORREO_BIENVENIDA
from config import ASUNTO_CORREO_LANZAMIENTO, HTML_CORREO_LANZAMIENTO, URL_APP
from config import ASUNTO_CORREO_RECORDATORIO_PORRA, HTML_CORREO_RECORDATORIO_PORRA
from config import ASUNTO_CORREO_CIERRE_PORRA, HTML_CORREO_CIERRE_PORRA

app = func.FunctionApp()

@app.route(route="enviarCorreo", auth_level=func.AuthLevel.ANONYMOUS)
def enviarCorreo(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:

        body=req.get_json()
        nombre=body["nombre"]
        usuario=body["usuario"]
        codigo=body["codigo"]
        correo_destino=body["correo_destino"]
        tipo_correo=body["tipo"]

    except Exception:

        return func.HttpResponse(json.dumps({"ok": False, "error": "El body no es correcto"}),
                                status_code=500,
                                mimetype="application/json")

    try:

        nombre_usuario=nombre if nombre else "DESCONOCIDO"

        MAPEO_CORREO={"bienvenida":{"ASUNTO":ASUNTO_CORREO_BIENVENIDA,
                                    "FORMATO_HTML":HTML_CORREO_BIENVENIDA.format(nombre=nombre_usuario, codigo=codigo)},
                        "lanzamiento":{"ASUNTO":ASUNTO_CORREO_LANZAMIENTO,
                                        "FORMATO_HTML":HTML_CORREO_LANZAMIENTO.format(nombre=nombre_usuario, usuario=usuario, codigo=codigo, url_app=URL_APP)},
                        "recordatorio_porra_pendiente":{"ASUNTO":ASUNTO_CORREO_RECORDATORIO_PORRA,
                                                        "FORMATO_HTML":HTML_CORREO_RECORDATORIO_PORRA.format(nombre=nombre_usuario, url_app=URL_APP)},
                        "cierre_porra":{"ASUNTO":ASUNTO_CORREO_CIERRE_PORRA,
                                                        "FORMATO_HTML":HTML_CORREO_CIERRE_PORRA.format(nombre=nombre_usuario, url_app=URL_APP)}}

        if tipo_correo not in MAPEO_CORREO.keys():

            return func.HttpResponse(json.dumps({"ok": False, "error": "El tipo de correo no es correcto"}),
                            status_code=500,
                            mimetype="application/json")


        enviarCorreoBase(correo_destino, MAPEO_CORREO[tipo_correo]["ASUNTO"], MAPEO_CORREO[tipo_correo]["FORMATO_HTML"], EMAIL_ACCOUNT, CONTRASENA_LOGIN, SERVIDOR_CORREO, PUERTO_CORREO)

        return func.HttpResponse(json.dumps({"ok": True}),
                                status_code=500,
                                mimetype="application/json")

    except Exception as e:

        logging.error(str(e))

        return func.HttpResponse(json.dumps({"ok": False, "error": str(e)}),
                                status_code=500,
                                mimetype="application/json")