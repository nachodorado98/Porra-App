import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def enviarCorreo(destino:str, asunto:str, template_correo:str, origen:str, contrasena:str, servidor_correo:str, puerto:int)->None:

    mensaje=MIMEMultipart()

    mensaje["From"]=origen
    mensaje["To"]=destino
    mensaje["Subject"]=asunto

    mensaje.attach(MIMEText(template_correo, "html"))

    try:

        servidor=smtplib.SMTP(servidor_correo, puerto)

        servidor.starttls()

        servidor.login(origen, contrasena)

        cuerpo=mensaje.as_string()

        servidor.sendmail(origen, destino, cuerpo)

    except Exception:

        raise Exception(f"Error al enviar el correo a {destino}")

    finally:

        servidor.quit()