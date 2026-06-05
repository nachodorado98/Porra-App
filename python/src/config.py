from .datalake.confconexiondatalake import CUENTA_DL, CLAVE_DL, CONTENEDOR_DL

URL_DATALAKE=f"https://{CUENTA_DL}.blob.core.windows.net/{CONTENEDOR_DL}"

PERFIL="perfil"

URL_DATALAKE_PERFIL=f"{URL_DATALAKE}/{PERFIL}/"