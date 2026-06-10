import os
import sys
sys.path.append("../..")
import time
import requests

from src.database.conexion import Conexion

AZURE_FUNCTION=os.getenv("AZURE_FUNCTION", "nombre_azure_function")
        
ENDPOINT_AZURE_FUNCTION=os.getenv("ENDPOINT_AZURE_FUNCTION", "endpoint_azure_function")

URL_AZURE_FUNCTION=f"https://{AZURE_FUNCTION}.azurewebsites.net/api/{ENDPOINT_AZURE_FUNCTION}"

con=Conexion()

datos_usuarios=con.obtenerDatosUsuarios()

con.cerrarConexion()

print("-"*50)
print("CORREO AVISO LANZAMIENTO")
print("-"*50)

for usuario, nombre, correo, codigo_liga in datos_usuarios:

    payload={"correo_destino":correo, "nombre":nombre, "usuario":usuario, "codigo":codigo_liga, "tipo":"lanzamiento"}

    print(f"Enviando correo a la direccion {correo}...")

    response=requests.post(URL_AZURE_FUNCTION, json=payload, timeout=120)

    time.sleep(5)