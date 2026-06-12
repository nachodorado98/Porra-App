import re
from datetime import datetime
from passlib.context import CryptContext
from typing import List, Dict, Optional
import os
import pandas as pd

from .configutils import PARTIDOS_FIJOS, PARTIDOS_VARIABLES_EQUIPO_PRIMERO

from src.datalake.conexion_data_lake import ConexionDataLake

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

def obtenerEliminatoriasRealLimpias(eliminatorias:List[tuple])->Dict:

    partidos={}

    for fila in eliminatorias:

        partido=fila[1].strip()

        partidos[partido]={"ronda": fila[0], "partido": partido,
                            "equipo_1": {"equipo_id": fila[2], "nombre": fila[3], "escudo": fila[4], "bandera": fila[5]},
                            "equipo_2": {"equipo_id": fila[6], "nombre": fila[7], "escudo": fila[8], "bandera": fila[9]},
                            "ganador": None if fila[10] is None else {"equipo_id": fila[10], "nombre": fila[11], "escudo": fila[12], "bandera": fila[13]}}

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

def crearCarpetaDataLakePerfil(contenedor_dl:str)->bool:

    try:

        dl=ConexionDataLake()

        if not dl.existe_carpeta(contenedor_dl, "perfil"):

            dl.crearCarpeta(contenedor_dl, "perfil")

        dl.cerrarConexion()

        return True

    except Exception as e:

        print(f"Error en conexion con datalake: {e}")

        return False

def crearCarpetaDataLakePerfilUsuario(usuario:str, contenedor_dl:str)->bool:

    try:

        dl=ConexionDataLake()

        if not dl.existe_carpeta(contenedor_dl, f"perfil/{usuario}"):

            dl.crearCarpeta(contenedor_dl, f"perfil/{usuario}")

        dl.cerrarConexion()

        return True

    except Exception as e:

        print(f"Error en conexion con datalake: {e}")

        return False

def listarImagenesCarpetaDatalake(usuario:str, contenedor_dl:str)->list[str]:

    try:

        dl=ConexionDataLake()

        imagenes=dl.obtenerArchivosCarpeta(contenedor_dl, f"perfil/{usuario}") if dl.existe_carpeta(contenedor_dl, f"perfil/{usuario}") else []

        dl.cerrarConexion()

        return imagenes

    except Exception as e:

        print(f"Error en conexion con datalake: {e}")

        return []

def existe_imagen_datalake(usuario:str, imagen:str, contenedor_dl:str)->bool:

    imagenes=listarImagenesCarpetaDatalake(usuario, contenedor_dl)

    return True if imagen in imagenes else False

def eliminarImagenDatalake(usuario:str, imagen:str, contenedor_dl:str)->bool:

    if existe_imagen_datalake(usuario, imagen, contenedor_dl):

        try:

            dl=ConexionDataLake()

            dl.eliminarArchivo(contenedor_dl, f"perfil/{usuario}", imagen)

            return True

        except Exception:

            return False

    return False

def subirImagenPerfilUsuarioDataLake(usuario:str, imagen:str, ruta_carpeta_local:str, contenedor_dl:str)->bool:

    try:

        dl=ConexionDataLake()

        dl.subirArchivo(contenedor_dl, f"perfil/{usuario}", ruta_carpeta_local, imagen)

        dl.cerrarConexion()

        return True

    except Exception as e:

        print(f"Error al subir imagen de perfil a DataLake: {e}")

        return False

def calcularPuntos(fila:Dict, posiciones_reales:Dict)->int:

    posicion_real=posiciones_reales[fila["equipo_porra_id"]]

    diferencia=abs(posicion_real-fila["posicion"])

    if diferencia==0:

        return 3

    if diferencia==1:

        return 2

    if diferencia==2:

        return 1

    return 0

def calcularMotivo(fila:Dict, posiciones_reales:Dict)->str:

    equipo_porra=fila["equipo_porra_id"]

    posicion_porra=fila["posicion"]

    posicion_real=posiciones_reales[equipo_porra]

    diferencia=abs(posicion_real-posicion_porra)

    if diferencia == 0:

        return "Posición exacta"

    if diferencia == 1:

        return "Diferencia de 1 posición"

    if diferencia == 2:

        return "Diferencia de 2 posiciones"

    return "Diferencia de 3 posiciones"

def compararGrupoDataFrameDetalle(grupos_real:List[Optional[tuple]], grupos_porra:List[Optional[tuple]])->pd.DataFrame:

    columnas=["grupo", "equipo_id", "nombre", "escudo", "bandera", "posicion"]

    df_real=pd.DataFrame(grupos_real, columns=columnas)

    df_porra=pd.DataFrame(grupos_porra, columns=columnas)

    columnas_salida=["grupo", "posicion", "equipo_real_id", "equipo_real_nombre", "equipo_real_escudo", "equipo_real_bandera",
                        "equipo_porra_id", "equipo_porra_nombre", "equipo_porra_escudo", "equipo_porra_bandera", "puntos", "motivo"]

    if df_real.empty:

        return pd.DataFrame(columns=columnas_salida)

    if df_porra.empty:

        df_real=df_real.rename(columns={"equipo_id": "equipo_real_id",
                                        "nombre": "equipo_real_nombre",
                                        "escudo": "equipo_real_escudo",
                                        "bandera": "equipo_real_bandera"})

        df_real["equipo_porra_id"]=None
        df_real["equipo_porra_nombre"]=None
        df_real["equipo_porra_escudo"]=None
        df_real["equipo_porra_bandera"]=None
        df_real["puntos"]=0
        df_real["motivo"]="Usuario sin porra para este grupo"

        return df_real[columnas_salida]

    grupo=df_real.iloc[0]["grupo"]

    df_real=df_real[df_real["grupo"]==grupo]

    df_porra=df_porra[df_porra["grupo"]==grupo]

    if len(df_real)!=4:

        raise Exception(f"Grupo real {grupo} incompleto: tiene {len(df_real)} equipos")

    if len(df_porra)!=4:

        raise Exception(f"Grupo porra {grupo} incompleto: tiene {len(df_porra)} equipos")

    df_comparacion=df_real.merge(df_porra, on=["grupo", "posicion"], how="left", suffixes=("_real", "_porra"))

    if len(df_comparacion)!=4:

        raise Exception(f"Error comparando grupo {grupo}: no coinciden las posiciones")

    df_comparacion=df_comparacion.rename(columns={"equipo_id_real": "equipo_real_id",
                                                    "nombre_real": "equipo_real_nombre",
                                                    "equipo_id_porra": "equipo_porra_id",
                                                    "nombre_porra": "equipo_porra_nombre"})

    posiciones_reales=dict(zip(df_real["equipo_id"], df_real["posicion"]))

    df_comparacion["puntos"]=df_comparacion.apply(calcularPuntos, axis=1, args=(posiciones_reales,))

    df_comparacion["motivo"]=df_comparacion.apply(calcularMotivo, axis=1, args=(posiciones_reales,))

    df_comparacion=df_comparacion.rename(columns={"equipo_id_real": "equipo_real_id",
                                                    "nombre_real": "equipo_real_nombre",
                                                    "escudo_real": "equipo_real_escudo",
                                                    "bandera_real": "equipo_real_bandera",
                                                    "equipo_id_porra": "equipo_porra_id",
                                                    "nombre_porra": "equipo_porra_nombre",
                                                    "escudo_porra": "equipo_porra_escudo",
                                                    "bandera_porra": "equipo_porra_bandera"})

    return df_comparacion[columnas_salida]

def compararGruposDisponiblesDataFrameDetalle(grupos_real:List[Optional[tuple]], grupos_porra:List[Optional[tuple]])->pd.DataFrame:

    columnas_salida=["grupo", "posicion", "equipo_real_id", "equipo_real_nombre", "equipo_real_escudo", "equipo_real_bandera",
                        "equipo_porra_id", "equipo_porra_nombre", "equipo_porra_escudo", "equipo_porra_bandera", "puntos", "motivo"]

    grupos_disponibles_real=sorted(list(set([grupo[0] for grupo in grupos_real])))

    dfs_detalle=[]

    for grupo_disponible_real in grupos_disponibles_real:

        grupo_real_grupo=list(filter(lambda grupo_real: grupo_real[0]==grupo_disponible_real, grupos_real))

        grupo_porra_grupo=list(filter(lambda grupo_porra: grupo_porra[0]==grupo_disponible_real, grupos_porra))

        df_detalle=compararGrupoDataFrameDetalle(grupo_real_grupo, grupo_porra_grupo)

        dfs_detalle.append(df_detalle)

    return pd.concat(dfs_detalle, ignore_index=True) if dfs_detalle else pd.DataFrame(columns=columnas_salida)

def calcularPuntosTotalesGrupos(grupos_real:List[Optional[tuple]], grupos_porra:List[Optional[tuple]])->int:

    df_detalle=compararGruposDisponiblesDataFrameDetalle(grupos_real, grupos_porra)

    return int(df_detalle["puntos"].sum())

def limpiarDataFrameDetalleGrupos(df_detalle_grupos:pd.DataFrame)->Dict:

    detalle_grupos={}

    for fila in df_detalle_grupos.to_dict("records"):

        grupo=fila["grupo"]

        if grupo not in detalle_grupos:

            detalle_grupos[grupo]={"puntos":0, "filas":[]}

        detalle_grupos[grupo]["filas"].append(fila)
        
        detalle_grupos[grupo]["puntos"]+=fila["puntos"]

    return detalle_grupos

def calcularPuntosMejoresTerceros(fila:Dict, equipos_reales:set)->int:

    if fila["equipo_porra_id"] in equipos_reales:

        return 4

    return 0

def calcularMotivoMejoresTerceros(fila:Dict, equipos_reales:set)->str:

    if fila["equipo_porra_id"] in equipos_reales:

        return "Mejor tercero acertado"

    return "No fue mejor tercero"

def compararMejoresTercerosDataFrameDetalle(mejores_terceros_real:List[Optional[tuple]], mejores_terceros_porra:List[Optional[tuple]])->pd.DataFrame:

    columnas=["grupo", "equipo_id", "nombre", "escudo", "bandera", "posicion"]

    df_real=pd.DataFrame(mejores_terceros_real, columns=columnas)

    df_porra=pd.DataFrame(mejores_terceros_porra, columns=columnas)

    columnas_salida=["posicion", "equipo_real_id", "equipo_real_nombre", "equipo_real_escudo", "equipo_real_bandera", "equipo_porra_id",
                    "equipo_porra_nombre", "equipo_porra_escudo", "equipo_porra_bandera", "puntos", "motivo"]

    if df_real.empty:

        return pd.DataFrame(columns=columnas_salida)

    if df_porra.empty:

        df_real=df_real.rename(columns={"equipo_id":"equipo_real_id",
                                        "nombre":"equipo_real_nombre",
                                        "escudo":"equipo_real_escudo",
                                        "bandera":"equipo_real_bandera"})

        df_real["equipo_porra_id"]=None
        df_real["equipo_porra_nombre"]=None
        df_real["equipo_porra_escudo"]=None
        df_real["equipo_porra_bandera"]=None
        df_real["puntos"]=0
        df_real["motivo"]="Usuario sin mejores terceros"

        return df_real[columnas_salida]

    if len(df_real)!=8:

        raise Exception(f"Mejores terceros reales incompletos: tiene {len(df_real)} equipos")

    if len(df_porra)!=8:

        raise Exception(f"Mejores terceros porra incompletos: tiene {len(df_porra)} equipos")

    df_comparacion=df_porra.rename(columns={"equipo_id":"equipo_porra_id",
                                            "nombre":"equipo_porra_nombre",
                                            "escudo":"equipo_porra_escudo",
                                            "bandera":"equipo_porra_bandera"})

    equipos_reales=set(df_real["equipo_id"])

    df_comparacion["puntos"]=df_comparacion.apply(calcularPuntosMejoresTerceros, axis=1, args=(equipos_reales,))

    df_comparacion["motivo"]=df_comparacion.apply(calcularMotivoMejoresTerceros, axis=1, args=(equipos_reales,))

    df_real_limpio=df_real.rename(columns={"equipo_id":"equipo_real_id",
                                            "nombre":"equipo_real_nombre",
                                            "escudo":"equipo_real_escudo",
                                            "bandera":"equipo_real_bandera"})

    df_comparacion["equipo_real_id"]=None
    df_comparacion["equipo_real_nombre"]=None
    df_comparacion["equipo_real_escudo"]=None
    df_comparacion["equipo_real_bandera"]=None

    return df_comparacion[columnas_salida]

def calcularPuntosTotalesMejoresTerceros(mejores_terceros_real:List[Optional[tuple]],  mejores_terceros_porra:List[Optional[tuple]])->int:

    df_detalle=compararMejoresTercerosDataFrameDetalle(mejores_terceros_real, mejores_terceros_porra)

    if df_detalle.empty:

        return 0

    return int(df_detalle["puntos"].sum())