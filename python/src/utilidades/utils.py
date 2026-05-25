import re
from datetime import datetime
from passlib.context import CryptContext
from typing import List, Dict

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

def obtenerGruposEquiposLimpios(grupos_equipos:List[tuple])->Dict:

    grupos={}

    for fila in grupos_equipos:

        grupo=fila[0]

        if grupo not in grupos:

            grupos[grupo]=[]

        grupos[grupo].append({"equipo_id": fila[1], "nombre": fila[2], "escudo": fila[3],  "bandera": fila[4]})

    return grupos

def validarEquiposGrupo(equipos_grupo_real:List[tuple], equipos_grupo_porra:List[tuple])->bool:

    equipos_grupo_real_limpio=[equipo[1] for equipo in equipos_grupo_real]

    if len(equipos_grupo_porra)!=4:

        return False

    for equipo_grupo_porra in equipos_grupo_porra:

        if equipo_grupo_porra not in equipos_grupo_real_limpio:

            return False

    return True

def gruposPorraCorrectos(equipos_grupos_real:List[tuple], equipos_grupos_porra:Dict)->bool:

    if len(equipos_grupos_porra)!=12:

        return False

    for grupo, equipos_grupo_porra in equipos_grupos_porra.items():

        equipos_grupo_real=list(filter(lambda equipo_grupo: equipo_grupo[0]==grupo, equipos_grupos_real))

        grupo_valido=validarEquiposGrupo(equipos_grupo_real, equipos_grupo_porra)

        if not grupo_valido:

            return False

    return True