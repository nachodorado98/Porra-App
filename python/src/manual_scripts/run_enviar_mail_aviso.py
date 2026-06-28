import os
import sys
sys.path.append("../..")
import time
import requests

from src.database.conexion import Conexion

if len(sys.argv)!=2:

    raise ValueError("Debes indicar el tipo de correo. Ejemplo: python run_enviar_mail_aviso.py inicio_mundial")

TIPO_CORREO=sys.argv[1]

tipos={"inicio_mundial":"INICIO MUNDIAL",
        "lanzamiento":"LANZAMIENTO",
        "recordatorio_porra_pendiente":"PORRA PENDIENTE",
        "cierre_porra":"PORRA CERRADA",
        "mitad_grupos":"MITAD GRUPOS",
        "fin_grupos":"FIN GRUPOS"}

if TIPO_CORREO not in list(tipos.keys()):

    raise ValueError(f"Debes indicar el tipo de correo correcto: \n{', '.join(list(tipos.keys()))}")

AZURE_FUNCTION=os.getenv("AZURE_FUNCTION", "nombre_azure_function")
        
ENDPOINT_AZURE_FUNCTION=os.getenv("ENDPOINT_AZURE_FUNCTION", "endpoint_azure_function")

URL_AZURE_FUNCTION=f"https://{AZURE_FUNCTION}.azurewebsites.net/api/{ENDPOINT_AZURE_FUNCTION}"

con=Conexion()

datos_usuarios=con.obtenerDatosUsuariosPorraPendiente() if TIPO_CORREO=="recordatorio_porra_pendiente" else con.obtenerDatosUsuarios()

con.cerrarConexion()

print("-"*50)
print(f"CORREO {tipos[TIPO_CORREO]}")
print("-"*50)

for usuario, nombre, correo, codigo_liga in datos_usuarios:

    payload={"correo_destino":correo, "nombre":nombre, "usuario":usuario, "codigo":codigo_liga, "tipo":TIPO_CORREO}

    print(f"Enviando correo a la direccion {correo}...")

    response=requests.post(URL_AZURE_FUNCTION, json=payload, timeout=120)

    time.sleep(5)