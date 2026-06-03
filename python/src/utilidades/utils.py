import re
from datetime import datetime
from passlib.context import CryptContext
from typing import List, Dict
import os

from .configutils import PARTIDOS_FIJOS, PARTIDOS_VARIABLES_EQUIPO_PRIMERO

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

    if len(set(equipos_grupo_porra))!=4:

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

def obtenerTercerosGruposEquiposLimpios(terceros_grupos:List[tuple])->List[Dict]:

    return [{"grupo": fila[0], "equipo_id": fila[1], "nombre": fila[2], "escudo": fila[3],  "bandera": fila[4]} for fila in terceros_grupos]

def mejoresTercerosPorraCorrectos(equipos_mejores_terceros_real:List[tuple], equipos_mejores_terceros_porra:List[Dict])->bool:

    if len(equipos_mejores_terceros_porra)!=8:

        return False

    if len(set(e['equipo_id'] for e in equipos_mejores_terceros_porra))!=8:
        
        return False

    if len(set(e['grupo'] for e in equipos_mejores_terceros_porra))!=8:
        
        return False

    for equipo_mejor_tercero_porra in equipos_mejores_terceros_porra:

        grupo_mejor_tercero=equipo_mejor_tercero_porra["grupo"]

        equipo_mejor_tercero=equipo_mejor_tercero_porra["equipo_id"]

        mejor_tercero_real_filtrado=list(filter(lambda equipo_mejor_tercero_real: equipo_mejor_tercero_real[0]==grupo_mejor_tercero and equipo_mejor_tercero_real[1]==equipo_mejor_tercero, equipos_mejores_terceros_real))

        if not mejor_tercero_real_filtrado:

            return False

    return True

def obtenerPasoEstado(estado:Dict)->int:

    PASOS=[("grupo_completo", 0), ("mejor_tercero_completo", 1), ("eliminatorias_completa", 2), ("porra_completa", 3)]

    for campo, paso in PASOS:

        if not estado[campo]:

            return paso

    return len(PASOS)

def obtenerPasosPorra(estado_porra:tuple):

    nombre_estados=["grupo_completo", "mejor_tercero_completo", "eliminatorias_completa", "porra_completa"]

    estado={nombre:estado for nombre, estado in zip(nombre_estados, estado_porra)}

    return obtenerPasoEstado(estado)

def obtenerCombinacionMejoresTerceros(mejores_terceros:List[tuple])->str:

    if not mejores_terceros:

        return ""

    grupos_mejores_terceros=[mejor_tercero[0] for mejor_tercero in mejores_terceros]

    return "".join(sorted(grupos_mejores_terceros))

def construirLookup(primeros_segundos:List[tuple], terceros:List[tuple])->Dict:

    lookup={}

    for grupo, slug, nombre, id_equipo, fifa, pos in primeros_segundos:

        lookup[f"{pos}{grupo}"]=(slug, nombre, id_equipo, fifa)

    for grupo, slug, nombre, id_equipo, fifa, pos in terceros:

        lookup[f"{pos}{grupo}"]=(slug, nombre, id_equipo, fifa)

    return lookup

def crearBracketDieciseisavos(partidos_variables_equipo_tercero:Dict, primeros_segundos:List[tuple], terceros:List[tuple])->Dict:

    lookup=construirLookup(primeros_segundos, terceros)

    bracket_final={}

    try:

        for partido, (slot1, slot2) in PARTIDOS_FIJOS.items():

            bracket_final[partido]=[lookup[slot1], lookup[slot2]]

        for partido, primero in PARTIDOS_VARIABLES_EQUIPO_PRIMERO.items():

            slot_tercero=partidos_variables_equipo_tercero[partido]

            bracket_final[partido]=[lookup[primero], lookup[slot_tercero]]

        return dict(sorted(bracket_final.items()))

    except Exception:

        return {}

def bracketEliminatoriasCorrecto(partidos_bracket:List[Dict], bracket_16avos:Dict)->bool:

    errores = []

    rondas_esperadas = {"dieciseisavos": 16,
                        "octavos": 8,
                        "cuartos": 4,
                        "semifinales": 2,
                        "tercer_puesto": 1,
                        "final": 1}

    ronda_por_partido = {**{f"M{i}": "dieciseisavos" for i in range(73, 89)},
                        **{f"M{i}": "octavos" for i in range(89, 97)},
                        **{f"M{i}": "cuartos" for i in range(97, 101)},
                        "M101": "semifinales",
                        "M102": "semifinales",
                        "M103": "tercer_puesto",
                        "M104": "final"}

    siguiente = {"M74": "M89", "M77": "M89",
                    "M73": "M90", "M75": "M90",
                    "M76": "M91", "M78": "M91",
                    "M79": "M92", "M80": "M92",
                    "M83": "M93", "M84": "M93",
                    "M81": "M94", "M82": "M94",
                    "M86": "M95", "M88": "M95",
                    "M85": "M96", "M87": "M96",

                    "M89": "M97", "M90": "M97",
                    "M93": "M98", "M94": "M98",
                    "M91": "M99", "M92": "M99",
                    "M95": "M100", "M96": "M100",

                    "M97": "M101", "M98": "M101",
                    "M99": "M102", "M100": "M102",

                    "M101": "M104",
                    "M102": "M104"}

    if not isinstance(partidos_bracket, list):
        return False

    if len(partidos_bracket) != 32:
        errores.append(f"El bracket debe tener 32 partidos y tiene {len(partidos_bracket)}")

    partidos = {}

    for p in partidos_bracket:
        partido = p.get("partido")

        if partido in partidos:
            errores.append(f"Partido duplicado: {partido}")

        partidos[partido] = p

    for partido_esperado in ronda_por_partido:
        if partido_esperado not in partidos:
            errores.append(f"Falta el partido {partido_esperado}")

    for match_id, p in partidos.items():
        if match_id not in ronda_por_partido:
            errores.append(f"Partido no válido: {match_id}")
            continue

        ronda_correcta = ronda_por_partido[match_id]

        if p.get("ronda") != ronda_correcta:
            errores.append(
                f"{match_id} debería ser ronda {ronda_correcta}, pero viene como {p.get('ronda')}"
            )

        equipo_1 = p.get("equipo_1_id")
        equipo_2 = p.get("equipo_2_id")
        ganador = p.get("ganador_id")

        if not equipo_1 or not equipo_2 or not ganador:
            errores.append(f"{match_id} tiene campos vacíos")

        if equipo_1 == equipo_2:
            errores.append(f"{match_id} tiene el mismo equipo dos veces")

        if ganador not in [equipo_1, equipo_2]:
            errores.append(f"El ganador de {match_id} no juega ese partido")

    for ronda, cantidad in rondas_esperadas.items():
        total = sum(1 for p in partidos.values() if p.get("ronda") == ronda)

        if total != cantidad:
            errores.append(f"La ronda {ronda} debe tener {cantidad} partidos y tiene {total}")

    for match_id, equipos in bracket_16avos.items():
        if match_id not in partidos:
            continue

        p = partidos[match_id]

        equipos_validos = {equipos[0][0], equipos[1][0]}
        equipos_recibidos = {p.get("equipo_1_id"), p.get("equipo_2_id")}

        if equipos_recibidos != equipos_validos:
            errores.append(
                f"{match_id} no coincide con los equipos reales de 16avos"
            )

    esperados_por_partido = {}

    for origen, destino in siguiente.items():
        if origen not in partidos:
            continue

        ganador_origen = partidos[origen].get("ganador_id")

        esperados_por_partido.setdefault(destino, []).append(ganador_origen)

    for destino, equipos_esperados in esperados_por_partido.items():
        if destino not in partidos:
            continue

        p = partidos[destino]
        equipos_recibidos = {p.get("equipo_1_id"), p.get("equipo_2_id")}

        if set(equipos_esperados) != equipos_recibidos:
            errores.append(
                f"{destino} debería tener {equipos_esperados}, pero tiene {list(equipos_recibidos)}"
            )

    if "M101" in partidos and "M102" in partidos and "M103" in partidos:
        perdedores_semis = []

        for semi in ["M101", "M102"]:
            p = partidos[semi]
            perdedor = p["equipo_1_id"] if p["ganador_id"] == p["equipo_2_id"] else p["equipo_2_id"]
            perdedores_semis.append(perdedor)

        equipos_m103 = {partidos["M103"]["equipo_1_id"], partidos["M103"]["equipo_2_id"]}

        if set(perdedores_semis) != equipos_m103:
            errores.append(
                f"M103 debería tener los perdedores de semifinales: {perdedores_semis}"
            )

    return len(errores)==0

def obtenerEliminatoriasPorraLimpias(eliminatorias:List[tuple])->Dict:

    partidos={}

    for fila in eliminatorias:

        partido=fila[1].strip()

        partidos[partido]={"ronda": fila[0], "partido": partido,
                            "equipo_1": {"equipo_id": fila[2], "nombre": fila[3], "escudo": fila[4], "bandera": fila[5]},
                            "equipo_2": {"equipo_id": fila[6], "nombre": fila[7], "escudo": fila[8], "bandera": fila[9]},
                            "ganador": {"equipo_id": fila[10], "nombre": fila[11], "escudo": fila[12], "bandera": fila[13]}}

    return partidos

def crearCarpeta(ruta:str)->None:

    if not os.path.exists(ruta):

        os.mkdir(ruta)

        print(f"Carpeta creada: {ruta}")

def borrarCarpeta(ruta:str)->None:

    if os.path.exists(ruta):

        os.rmdir(ruta)

        print(f"Carpeta borrada: {ruta}")

def vaciarCarpeta(ruta:str)->None:

    if os.path.exists(ruta):

        for archivo in os.listdir(ruta):

            try:

                if not os.path.isdir(os.path.join(ruta, archivo)):

                    os.remove(os.path.join(ruta, archivo))

                else:

                    os.rmdir(os.path.join(ruta, archivo))

            except Exception:
                
                pass
                
def extraerExtension(archivo:str, extension_alternativa:str="jpg")->str:

    return archivo.rsplit(".", 1)[1].lower() if "." in archivo else extension_alternativa