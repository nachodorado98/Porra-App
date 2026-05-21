import azure.functions as func
import datetime
import json
import logging
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

app = func.FunctionApp()

def enviarCorreoBienvenida(destino:str, asunto:str, template_correo:str, origen:str, contrasena:str, servidor:str, puerto:int)->None:

    mensaje=MIMEMultipart()

    mensaje["From"]=origen
    mensaje["To"]=destino
    mensaje["Subject"]=asunto

    mensaje.attach(MIMEText(template_correo, "html"))

    try:

        servidor=smtplib.SMTP(servidor, puerto)

        servidor.starttls()

        servidor.login(origen, contrasena)

        cuerpo=mensaje.as_string()

        servidor.sendmail(origen, destino, cuerpo)

    except Exception:

        raise Exception(f"Error al enviar el correo a {destino}")

    finally:

        servidor.quit()

@app.route(route="enviarCorreo", auth_level=func.AuthLevel.ANONYMOUS)
def enviarCorreo(req: func.HttpRequest) -> func.HttpResponse:

    logging.info('Python HTTP trigger function processed a request.')

    try:

        body=req.get_json()

    except Exception:

        return func.HttpResponse(
            json.dumps({
                "ok": False,
                "error": "Falta el body"
            }),
            status_code=500,
            mimetype="application/json"
            )

    nombre=body["nombre"]
    correo_destino=body["correo_destino"]

    if not correo_destino:

        return func.HttpResponse(
            json.dumps({
                "ok": False,
                "error": "Falta el correo destino"
            }),
            status_code=500,
            mimetype="application/json"
            )


    asunto="¡Bienvenido a nuestra familia!"

    html="""
            <!DOCTYPE html>
            <html lang="es">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Correo Aplicacion Futbol</title>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        background-color: #f4f4f4;
                        margin: 0;
                        padding: 0;
                    }}
                    .container {{
                        max-width: 600px;
                        margin: 0 auto;
                        background-color: #ffffff;
                        padding: 20px;
                        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                    }}
                    .header {{
                        text-align: center;
                        padding: 20px;
                        background-color: #333333;
                        color: #ffffff;
                    }}
                    .content {{
                        padding: 20px;
                        color: #333333;
                    }}
                    .content h1 {{
                        font-size: 24px;
                        color: #333333;
                    }}
                    .content p {{
                        font-size: 16px;
                        line-height: 1.5;
                        color: #666666;
                    }}
                    .content a {{
                        color: #333333;
                        text-decoration: none;
                    }}
                    .footer {{
                        text-align: center;
                        padding: 20px;
                        background-color: #f4f4f4;
                        color: #777777;
                        font-size: 12px;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>Porra App</h1>
                    </div>
                    <div class="content">
                        <h1>Hola, {nombre}:</h1>
                        <p>Te escribimos para confirmar que tu registro en nuestro aplicación ha sido exitoso.</p>
                        <p>Gracias por unirte a nosotros. Ahora puedes disfrutar de todas las funcionalidades de nuestra web.</p>
                        <p>Atentamente,<br>el equipo de Porra App<br></p>
                    </div>
                    <div class="footer">
                        <p>Este es un correo electrónico automatizado. Por favor, no respondas a este mensaje.</p>
                        <p>&copy; 2026 Porra App. Todos los derechos reservados.</p>
                    </div>
                </div>
            </body>
            </html>
            """

    try:

        nombre_usuario=nombre if nombre else "DESCONOCIDO"

        correo_origen=os.environ.get("EMAIL_ACCOUNT")
        contrasena=os.environ.get("CONTRASENA_LOGIN")
        servidor=os.environ.get("SERVIDOR_CORREO")
        puerto=int(os.environ.get("PUERTO_CORREO"))

        enviarCorreoBienvenida(correo_destino, asunto, html.format(nombre=nombre_usuario), correo_origen, contrasena, servidor, puerto)

        return func.HttpResponse(
                json.dumps({"ok": True}),
                status_code=200,
                mimetype="application/json"
                )

    except Exception as e:

        logging.error(str(e))

        return func.HttpResponse(
                json.dumps({
                    "ok": False,
                    "error": str(e)
                }),
                status_code=500,
                mimetype="application/json"
                )