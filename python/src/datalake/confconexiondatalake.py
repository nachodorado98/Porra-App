import os

CUENTA_DL=os.environ.get("AZURE_NAME_ACCOUNT") # Nombre del Data Lake
CLAVE_DL=os.environ.get("AZURE_KEY_ACCOUNT") # Clave del Data Lake
CONTENEDOR_DL=(os.environ.get("ENTORNO") or "dev").lower() # Nombre del contenedor