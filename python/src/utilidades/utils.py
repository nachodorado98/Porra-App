import re
from datetime import datetime
from passlib.context import CryptContext

def codigo_valido(codigo:str)->bool:

    if not codigo:

        return False

    codigo_upper=codigo.upper()

    return True if codigo_upper.isalnum() and codigo_upper.isupper() and len(codigo_upper)==6 else False

def usuario_correcto(usuario:str)->bool:

    return bool(usuario and re.match(r'^[\w.]+$', usuario))

def nombre_correcto(nombre:str)->bool:

    return bool(nombre and re.match(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$", nombre))

def apellido_correcto(apellido:str)->bool:

    return nombre_correcto(apellido)

def contrasena_correcta(contrasena:str)->bool:

    if not contrasena:

        return False

    patron=re.compile(r"^[^\s]{8,}$")

    return bool(re.fullmatch(patron, contrasena))

def correo_correcto(correo:str)->bool:

    if not correo:

        return False

    patron=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    return bool(re.match(patron, correo))

def datos_correctos(usuario:str, nombre:str, apellido:str, contrasena:str, correo:str)->bool:

    return (usuario_correcto(usuario) and
            nombre_correcto(nombre) and
            apellido_correcto(apellido) and
            contrasena_correcta(contrasena) and
            correo_correcto(correo))

def generarHash(contrasena:str)->str:

    objeto_hash=CryptContext(schemes=["bcrypt"], deprecated="auto")

    return objeto_hash.hash(contrasena)

def comprobarHash(contrasena:str, contrasena_hash:str)->bool:

    objeto_hash=CryptContext(schemes=["bcrypt"], deprecated="auto")

    return objeto_hash.verify(contrasena, contrasena_hash)