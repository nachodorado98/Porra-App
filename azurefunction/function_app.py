import azure.functions as func
import datetime
import json
import logging

from utils import enviarCorreoBase

from config import EMAIL_ACCOUNT, CONTRASENA_LOGIN, SERVIDOR_CORREO, PUERTO_CORREO, ASUNTO_CORREO_BIENVENIDA, HTML_CORREO_BIENVENIDA
from config import ASUNTO_CORREO_LANZAMIENTO, HTML_CORREO_LANZAMIENTO, URL_APP
from config import ASUNTO_CORREO_RECORDATORIO_PORRA, HTML_CORREO_RECORDATORIO_PORRA
from config import ASUNTO_CORREO_CIERRE_PORRA, HTML_CORREO_CIERRE_PORRA
from config import ASUNTO_CORREO_INICIO_MUNDIAL, HTML_CORREO_INICIO_MUNDIAL
from config import ASUNTO_CORREO_MITAD_GRUPOS, HTML_CORREO_MITAD_GRUPOS
from config import ASUNTO_CORREO_RESET_PASSWORD, HTML_CORREO_RESET_PASSWORD
from config import ASUNTO_CORREO_FIN_GRUPOS, HTML_CORREO_FIN_GRUPOS

app = func.FunctionApp()

@app.route(route="enviarCorreo", auth_level=func.AuthLevel.ANONYMOUS)
def enviarCorreo(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:

        body=req.get_json()
        nombre=body.get("nombre")
        usuario=body.get("usuario")
        codigo=body.get("codigo")
        correo_destino=body["correo_destino"]
        tipo_correo=body["tipo"]
        token=body.get("token")
        reset_link=f"{URL_APP}/reset_password/{token}"

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
                                        "FORMATO_HTML":HTML_CORREO_CIERRE_PORRA.format(nombre=nombre_usuario, url_app=URL_APP)},
                        "inicio_mundial":{"ASUNTO":ASUNTO_CORREO_INICIO_MUNDIAL,
                                            "FORMATO_HTML":HTML_CORREO_INICIO_MUNDIAL.format(nombre=nombre_usuario, url_app=URL_APP)},
                        "mitad_grupos":{"ASUNTO":ASUNTO_CORREO_MITAD_GRUPOS,
                                        "FORMATO_HTML":HTML_CORREO_MITAD_GRUPOS.format(nombre=nombre_usuario, url_app=URL_APP)},
                        "reset_password":{"ASUNTO": ASUNTO_CORREO_RESET_PASSWORD,
                                            "FORMATO_HTML": HTML_CORREO_RESET_PASSWORD.format(nombre=nombre_usuario, reset_link=reset_link)},
                        "fin_grupos":{"ASUNTO": ASUNTO_CORREO_FIN_GRUPOS,
                                        "FORMATO_HTML": HTML_CORREO_FIN_GRUPOS.format(nombre=nombre_usuario, url_app=URL_APP)}}

        if tipo_correo not in MAPEO_CORREO.keys():

            return func.HttpResponse(json.dumps({"ok": False, "error": "El tipo de correo no es correcto"}),
                            status_code=500,
                            mimetype="application/json")


        enviarCorreoBase(correo_destino, MAPEO_CORREO[tipo_correo]["ASUNTO"], MAPEO_CORREO[tipo_correo]["FORMATO_HTML"], EMAIL_ACCOUNT, CONTRASENA_LOGIN, SERVIDOR_CORREO, PUERTO_CORREO)

        return func.HttpResponse(json.dumps({"ok": True}),
                                status_code=200,
                                mimetype="application/json")

    except Exception as e:

        logging.error(str(e))

        return func.HttpResponse(json.dumps({"ok": False, "error": str(e)}),
                                status_code=500,
                                mimetype="application/json")