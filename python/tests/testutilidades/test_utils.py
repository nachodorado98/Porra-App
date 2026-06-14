import pytest
import os
import copy
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

from src.utilidades.utils import codigo_valido, usuario_correcto, nombre_correcto, apellido_correcto, contrasena_correcta
from src.utilidades.utils import correo_correcto, datos_correctos, generarHash, comprobarHash, obtenerGruposEquiposLimpios
from src.utilidades.utils import validarEquiposGrupo, gruposPorraCorrectos, obtenerTercerosGruposEquiposLimpios, mejoresTercerosPorraCorrectos
from src.utilidades.utils import obtenerPasoEstado, obtenerPasosPorra, obtenerCombinacionMejoresTerceros, construirLookup, crearBracketDieciseisavos
from src.utilidades.utils import bracketEliminatoriasCorrecto, obtenerEliminatoriasPorraLimpias, obtenerEliminatoriasRealLimpias
from src.utilidades.utils import crearCarpeta, borrarCarpeta, vaciarCarpeta, extraerExtension
from src.utilidades.utils import crearCarpetaDataLakePerfil, crearCarpetaDataLakePerfilUsuario, listarImagenesCarpetaDatalake
from src.utilidades.utils import existe_imagen_datalake, eliminarImagenDatalake, subirImagenPerfilUsuarioDataLake
from src.utilidades.utils import calcularPuntos, calcularMotivo, compararGrupoDataFrameDetalle, compararGruposDisponiblesDataFrameDetalle, calcularPuntosTotalesGrupos
from src.utilidades.utils import limpiarDataFrameDetalleGrupos, calcularPuntosMejoresTerceros, calcularMotivoMejoresTerceros, compararMejoresTercerosDataFrameDetalle
from src.utilidades.utils import calcularPuntosTotalesMejoresTerceros, obtenerEquiposRondaEliminatoria, calcularPuntosPresenciaEliminatoria, calcularMotivoPresenciaEliminatoria
from src.utilidades.utils import compararRondaEliminatoriaDataFrameDetalle, compararEliminatoriasDisponiblesDataFrameDetalle, calcularPuntosTotalesEliminatorias
from src.utilidades.utils import obtenerFinalEliminatoria, calcularBonusCampeonEliminatorias, calcularBonusFinalExactaEliminatorias


@pytest.mark.parametrize(["codigo"],
    [("123456",),("ABCDE",),("ABCDE&",),(None,),("ABCDEFG",),("A1BC2DEF",)]
)
def test_codigo_no_valido(codigo):

    assert not codigo_valido(codigo)

@pytest.mark.parametrize(["codigo"],
    [("ABCDEF",),("ABCDE1",),("ZK5Z1Q",),("3YYZKP",),("GTMRIJ",),("abcdef",)]
)
def test_codigo_valido(codigo):

    assert codigo_valido(codigo)

@pytest.mark.parametrize(["usuario"],
    [("ana-maria",),("carlos?456",),("",),(None,)]
)
def test_usuario_incorrecto(usuario):

    assert not usuario_correcto(usuario)

@pytest.mark.parametrize(["usuario"],
    [("juan123",),("usuario1",),("12345",),("ana_maria",),("carlos_456",)]
)
def test_usuario_correcto(usuario):

    assert usuario_correcto(usuario)

@pytest.mark.parametrize(["nombre"],
    [("123",),("Juan-Maria",),(None,),("",),("Nacho1998",)]
)
def test_nombre_incorrecto(nombre):

    assert not nombre_correcto(nombre)

@pytest.mark.parametrize(["nombre"],
    [("Nacho",),("Pérez",),("Ana",),("López",),("Carlos",),("González",),("Amanda",),("José",),("María del Carmen",)]
)
def test_nombre_correcto(nombre):

    assert nombre_correcto(nombre)

@pytest.mark.parametrize(["apellido"],
    [("123",),("Aranda.Gonzalez",),(None,),("",),("Dorado1998",)]
)
def test_apellido_incorrecto(apellido):

    assert not apellido_correcto(apellido)

@pytest.mark.parametrize(["apellido"],
    [("Nacho",),("Pérez",),("Ana",),("López",),("Carlos",),("González",),("Amanda",),("Aranda Gonzalez",)]
)
def test_apellido_correcto(apellido):

    assert apellido_correcto(apellido)

@pytest.mark.parametrize(["contrasena"],
    [("clave",),("PASSWD",),("1234567",),("Abcdefg",),("",),("A1b2C3d",),("abcd",),("1234",),
     ("Ab CdEfGhI",),("Ab!CdEfGhI ",),(" Ab!CdEfGhI",),("AIJKLMN",),("Ab@cdE2",),
     ("Ab@cdEf1 G",),("Abcd12 34!",),(None,)]
)
def test_contrasena_incorrecta(contrasena):

    assert not contrasena_correcta(contrasena)

@pytest.mark.parametrize(["contrasena"],
    [("Ab!CdEfGhIJK3LMN",),("Abcd1234!",),("22&NachoD&19",),("12345678",)]
)
def test_contrasena_correcta(contrasena):

    assert contrasena_correcta(contrasena)

@pytest.mark.parametrize(["correo"],
    [("correo_sin_arroba.com",),("usuario@sin_punto",),("correo@falta_punto_com",),("sin_local_part@.com",),("@falta_local_part.com",)]
)
def test_correo_incorrecto(correo):

    assert not correo_correcto(correo)

@pytest.mark.parametrize(["correo"],
    [("usuario@gmail.com",),("ejemplo123@yahoo.com",),("mi_correo-123@dominio.com",),
    ("usuario+etiqueta@dominio.com",), ("ejemplo.123@subdominio.dominio.co.uk",)]
)
def test_correo_correcto(correo):

    assert correo_correcto(correo)

@pytest.mark.parametrize(["usuario", "nombre", "apellido", "contrasena", "correo"],
    [
        (None, "nacho", "dorado", "Ab!CdEfGhIJK3LMN", "correo@correo.es"),
        ("golden98", None, "dorado", "Ab!CdEfGhIJK3LMN", "correo@correo.es"),
        ("golden98", "nacho", None, "Ab!CdEfGhIJK3LMN", "correo@correo.es"),
        ("golden98", "nacho", "dorado", None, "correo@correo.es"),
        ("carlos-456", "nacho", "dorado", "Ab!CdEfGhIJK3LMN", "correo@correo.es"),
        ("golden98", "nacho1", "dorado", "Ab!CdEfGhIJK3LMN", "correo@correo.es"),
        ("golden98", "nacho", "dorado2", "Ab!CdEfGhIJK3LMN", "correo@correo.es"),
        ("golden98", "nachogolden", "dorado", "12345678", "correo@.es"),
    ]
)
def test_datos_incorrectos(usuario, nombre, apellido, contrasena, correo):

    assert not datos_correctos(usuario, nombre, apellido, contrasena, correo)

@pytest.mark.parametrize(["usuario", "nombre", "apellido", "contrasena", "correo"],
    [
        ("nacho98", "nacho", "dorado", "Ab!CdEfGhIJK3LMN", "usuario@gmail.com"),
        ("golden98", "nachogolden", "dorado", "Abcd1234!","correo@correo.es"),
        ("carlos_456", "nachogolden", "dorado", "22&NachoD&19", "ejemplo123@yahoo.com"),
        ("carlos_456", "nachogolden", "dorado", "12345678", "ejemplo123@yahoo.com"),
    ]
)
def test_datos_correctos(usuario, nombre, apellido, contrasena, correo):

    assert datos_correctos(usuario, nombre, apellido, contrasena, correo)

@pytest.mark.parametrize(["contrasena"],
    [("contrasena1234",),("123456789",),("contrasena_secreta",)]
)
def test_generar_hash_contrasena(contrasena):

    contrasena_hash=generarHash(contrasena)

    assert len(contrasena_hash)==60
    assert contrasena not in contrasena_hash

@pytest.mark.parametrize(["contrasena", "contrasena_mal"],
    [
        ("contrasena1234","contrasena123"),
        ("123456789","1234567899"),
        ("contrasena_secreta","contrasenasecreta")
    ]
)
def test_comprobar_hash_contrasena_incorrecta(contrasena, contrasena_mal):

    contrasena_hash=generarHash(contrasena)

    assert not comprobarHash(contrasena_mal, contrasena_hash)

@pytest.mark.parametrize(["contrasena"],
    [("contrasena1234",),("123456789",),("contrasena_secreta",)]
)
def test_comprobar_hash_contrasena_correcta(contrasena):

    contrasena_hash=generarHash(contrasena)

    assert comprobarHash(contrasena, contrasena_hash)

def test_obtener_grupos_equipos_limpios_no_hay():

    assert not obtenerGruposEquiposLimpios([])

def test_obtener_grupos_equipos_limpios():

    grupos_equipos=[('A', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR'),
                    ('A', 'seleccion-mexico', 'México', 3811, 'MEX'),
                    ('A', 'republica-checa', 'República Checa', 6188, 'CZE'),
                    ('A', 'seleccion-sudafrica', 'Sudáfrica', 3815, 'ZAF')]

    grupos_equipos_limpios=obtenerGruposEquiposLimpios(grupos_equipos)

    assert len(grupos_equipos_limpios.keys())==1

    for grupo, equipos in grupos_equipos_limpios.items():

        assert len(grupos_equipos_limpios[grupo])==4

@pytest.mark.parametrize(["porra"],
    [
        (['seleccion-espanola', 'seleccion-uruguay', 'seleccion-arabia-saudi'],),
        (['seleccion-espanola', 'seleccion-uruguay', 'seleccion-arabia-saudi', 'cabo-verde', 'seleccion-suiza', 'canada'],),
        (['seleccion-espanola'],),
        ([],)
    ]
)
def test_validar_equipos_grupo_no_valido_dimension_error(porra):

    real=[('H', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'), ('H', 'cabo-verde', 'Cabo Verde', 9158, 'CPV'), ('H', 'seleccion-espanola', 'España', 3850, 'ESP'), ('H', 'seleccion-uruguay', 'Uruguay', 3768, 'URY')]

    assert not validarEquiposGrupo(real, porra)

@pytest.mark.parametrize(["porra"],
    [
        (['seleccion-espanola', 'seleccion-uruguay', 'seleccion-arabia-saudi', 'seleccion-suiza'],),
        (['seleccion-espanola', 'canada', 'seleccion-arabia-saudi', 'seleccion-suiza'],),
        (['seleccion-espanola', 'seleccion-uruguay', 'seleccion-arabia-saudi', 'equipo'],),
        (['equipo', 'seleccion-uruguay', 'seleccion-arabia-saudi', 'seleccion-suiza'],),
        (['seleccion-brasil', 'seleccion-marruecos', 'seleccion-escocia', 'haiti'],)
    ]
)
def test_validar_equipos_grupo_no_valido_equipos_error(porra):

    real=[('H', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'), ('H', 'cabo-verde', 'Cabo Verde', 9158, 'CPV'), ('H', 'seleccion-espanola', 'España', 3850, 'ESP'), ('H', 'seleccion-uruguay', 'Uruguay', 3768, 'URY')]

    assert not validarEquiposGrupo(real, porra)

def test_validar_equipos_grupo_valido():

    porra=['seleccion-espanola', 'seleccion-uruguay', 'seleccion-arabia-saudi', 'cabo-verde']

    real=[('H', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'), ('H', 'cabo-verde', 'Cabo Verde', 9158, 'CPV'), ('H', 'seleccion-espanola', 'España', 3850, 'ESP'), ('H', 'seleccion-uruguay', 'Uruguay', 3768, 'URY')]

    assert validarEquiposGrupo(real, porra)

def test_grupos_porra_correctos_grupo_faltante():

    porra={'A': ['seleccion-mexico', 'republica-checa', 'seleccion-republica-corea', 'seleccion-sudafrica'],
    'B': ['seleccion-suiza', 'canada', 'seleccion-bosnia-herzegovina', 'seleccion-qatar'],
    'C': ['seleccion-brasil', 'seleccion-marruecos', 'seleccion-escocia', 'haiti'],
    'D': ['seleccion-estados-unidos', 'seleccion-turquia', 'seleccion-paraguay', 'seleccion-australia'],
    'E': ['seleccion-alemania', 'seleccion-ecuador', 'seleccion-costa-marfil', 'curazao'],
    'F': ['seleccion-holanda', 'seleccion-japon', 'seleccion-suecia', 'seleccion-tunez'],
    'G': ['seleccion-belgica', 'seleccion-egipto', 'seleccion-iran', 'seleccion-nueva-zelanda'],
    'I': ['seleccion-francia', 'seleccion-noruega', 'senegal', 'seleccion-iraq'],
    'J': ['seleccion-argentina', 'seleccion-austria', 'seleccion-argelia', 'jordania'],
    'K': ['seleccion-portugal', 'seleccion-colombia', 'rd-congo', 'seleccion-uzbekistan'],
    'L': ['seleccion-inglaterra', 'seleccion-croacia', 'seleccion-ghana', 'panama-seleccion']}

    real=[('A', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR'), ('A', 'seleccion-mexico', 'México', 3811, 'MEX'), ('A', 'republica-checa', 'República Checa', 6188, 'CZE'), ('A', 'seleccion-sudafrica', 'Sudáfrica', 3815, 'ZAF'),
    ('B', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH'), ('B', 'canada', 'Canadá', 5577, 'CAN'), ('B', 'seleccion-qatar', 'Catar', 3799, 'QAT'), ('B', 'seleccion-suiza', 'Suiza', 3723, 'CHE'),
    ('C', 'seleccion-brasil', 'Brasil', 3775, 'BRA'), ('C', 'seleccion-escocia', 'Escocia', 3758, 'SCO'), ('C', 'haiti', 'Haití', 5582, 'HTI'), ('C', 'seleccion-marruecos', 'Marruecos', 3780, 'MAR'),
    ('D', 'seleccion-australia', 'Australia', 3801, 'AUS'), ('D', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'), ('D', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY'), ('D', 'seleccion-turquia', 'Turquía', 3737, 'TUR'),
    ('E', 'seleccion-alemania', 'Alemania', 3734, 'DEU'), ('E', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV'), ('E', 'curazao', 'Curazao', 61757, 'CUR'), ('E', 'seleccion-ecuador', 'Ecuador', 3771, 'ECU'),
    ('F', 'seleccion-japon', 'Japón', 3798, 'JPN'), ('F', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD'), ('F', 'seleccion-suecia', 'Suecia', 3074, 'SWE'), ('F', 'seleccion-tunez', 'Túnez', 3783, 'TUN'),
    ('G', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'), ('G', 'seleccion-egipto', 'Egipto', 3788, 'EGY'), ('G', 'seleccion-iran', 'Irán', 3806, 'IRN'), ('G', 'seleccion-nueva-zelanda', 'Nueva Zelanda', 3808, 'NZL'),
    ('H', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'), ('H', 'cabo-verde', 'Cabo Verde', 9158, 'CPV'), ('H', 'seleccion-espanola', 'España', 3850, 'ESP'), ('H', 'seleccion-uruguay', 'Uruguay', 3768, 'URY'),
    ('I', 'seleccion-francia', 'Francia', 3750, 'FRA'), ('I', 'seleccion-iraq', 'Iraq', 3816, 'IRQ'), ('I', 'seleccion-noruega', 'Noruega', 3759, 'NOR'), ('I', 'senegal', 'Senegal', 5658, 'SEN'),
    ('J', 'seleccion-argelia', 'Argelia', 3787, 'DZA'), ('J', 'seleccion-argentina', 'Argentina', 3770, 'ARG'), ('J', 'seleccion-austria', 'Austria', 3767, 'AUT'), ('J', 'jordania', 'Jordania', 5480, 'JOR'),
    ('K', 'seleccion-colombia', 'Colombia', 3774, 'COL'), ('K', 'seleccion-portugal', 'Portugal', 3762, 'PRT'), ('K', 'rd-congo', 'RD Congo', 11591, 'COD'), ('K', 'seleccion-uzbekistan', 'Uzbekistán', 3800, 'UZB'),
    ('L', 'seleccion-croacia', 'Croacia', 3766, 'HRV'), ('L', 'seleccion-ghana', 'Ghana', 3791, 'GHA'), ('L', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG'), ('L', 'panama-seleccion', 'Panamá', 17581, 'PAN')]
    
    assert not gruposPorraCorrectos(real, porra)

@pytest.mark.parametrize(["porra_grupo"],
    [
        (['seleccion-espanola', 'seleccion-uruguay', 'seleccion-arabia-saudi'],),
        (['seleccion-espanola', 'seleccion-uruguay', 'seleccion-arabia-saudi', 'cabo-verde', 'seleccion-suiza', 'canada'],),
        (['seleccion-espanola'],),
        ([],)
    ]
)
def test_grupos_porra_correctos_dimension_error(porra_grupo):

    porra={'A': ['seleccion-mexico', 'republica-checa', 'seleccion-republica-corea', 'seleccion-sudafrica'],
    'B': ['seleccion-suiza', 'canada', 'seleccion-bosnia-herzegovina', 'seleccion-qatar'],
    'C': ['seleccion-brasil', 'seleccion-marruecos', 'seleccion-escocia', 'haiti'],
    'D': ['seleccion-estados-unidos', 'seleccion-turquia', 'seleccion-paraguay', 'seleccion-australia'],
    'E': ['seleccion-alemania', 'seleccion-ecuador', 'seleccion-costa-marfil', 'curazao'],
    'F': ['seleccion-holanda', 'seleccion-japon', 'seleccion-suecia', 'seleccion-tunez'],
    'G': ['seleccion-belgica', 'seleccion-egipto', 'seleccion-iran', 'seleccion-nueva-zelanda'],
    'H': porra_grupo,
    'I': ['seleccion-francia', 'seleccion-noruega', 'senegal', 'seleccion-iraq'],
    'J': ['seleccion-argentina', 'seleccion-austria', 'seleccion-argelia', 'jordania'],
    'K': ['seleccion-portugal', 'seleccion-colombia', 'rd-congo', 'seleccion-uzbekistan'],
    'L': ['seleccion-inglaterra', 'seleccion-croacia', 'seleccion-ghana', 'panama-seleccion']}

    real=[('A', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR'), ('A', 'seleccion-mexico', 'México', 3811, 'MEX'), ('A', 'republica-checa', 'República Checa', 6188, 'CZE'), ('A', 'seleccion-sudafrica', 'Sudáfrica', 3815, 'ZAF'),
    ('B', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH'), ('B', 'canada', 'Canadá', 5577, 'CAN'), ('B', 'seleccion-qatar', 'Catar', 3799, 'QAT'), ('B', 'seleccion-suiza', 'Suiza', 3723, 'CHE'),
    ('C', 'seleccion-brasil', 'Brasil', 3775, 'BRA'), ('C', 'seleccion-escocia', 'Escocia', 3758, 'SCO'), ('C', 'haiti', 'Haití', 5582, 'HTI'), ('C', 'seleccion-marruecos', 'Marruecos', 3780, 'MAR'),
    ('D', 'seleccion-australia', 'Australia', 3801, 'AUS'), ('D', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'), ('D', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY'), ('D', 'seleccion-turquia', 'Turquía', 3737, 'TUR'),
    ('E', 'seleccion-alemania', 'Alemania', 3734, 'DEU'), ('E', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV'), ('E', 'curazao', 'Curazao', 61757, 'CUR'), ('E', 'seleccion-ecuador', 'Ecuador', 3771, 'ECU'),
    ('F', 'seleccion-japon', 'Japón', 3798, 'JPN'), ('F', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD'), ('F', 'seleccion-suecia', 'Suecia', 3074, 'SWE'), ('F', 'seleccion-tunez', 'Túnez', 3783, 'TUN'),
    ('G', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'), ('G', 'seleccion-egipto', 'Egipto', 3788, 'EGY'), ('G', 'seleccion-iran', 'Irán', 3806, 'IRN'), ('G', 'seleccion-nueva-zelanda', 'Nueva Zelanda', 3808, 'NZL'),
    ('H', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'), ('H', 'cabo-verde', 'Cabo Verde', 9158, 'CPV'), ('H', 'seleccion-espanola', 'España', 3850, 'ESP'), ('H', 'seleccion-uruguay', 'Uruguay', 3768, 'URY'),
    ('I', 'seleccion-francia', 'Francia', 3750, 'FRA'), ('I', 'seleccion-iraq', 'Iraq', 3816, 'IRQ'), ('I', 'seleccion-noruega', 'Noruega', 3759, 'NOR'), ('I', 'senegal', 'Senegal', 5658, 'SEN'),
    ('J', 'seleccion-argelia', 'Argelia', 3787, 'DZA'), ('J', 'seleccion-argentina', 'Argentina', 3770, 'ARG'), ('J', 'seleccion-austria', 'Austria', 3767, 'AUT'), ('J', 'jordania', 'Jordania', 5480, 'JOR'),
    ('K', 'seleccion-colombia', 'Colombia', 3774, 'COL'), ('K', 'seleccion-portugal', 'Portugal', 3762, 'PRT'), ('K', 'rd-congo', 'RD Congo', 11591, 'COD'), ('K', 'seleccion-uzbekistan', 'Uzbekistán', 3800, 'UZB'),
    ('L', 'seleccion-croacia', 'Croacia', 3766, 'HRV'), ('L', 'seleccion-ghana', 'Ghana', 3791, 'GHA'), ('L', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG'), ('L', 'panama-seleccion', 'Panamá', 17581, 'PAN')]
    
    assert not gruposPorraCorrectos(real, porra)

@pytest.mark.parametrize(["porra_grupo"],
    [
        (['seleccion-espanola', 'seleccion-uruguay', 'seleccion-arabia-saudi', 'seleccion-suiza'],),
        (['seleccion-espanola', 'canada', 'seleccion-arabia-saudi', 'seleccion-suiza'],),
        (['seleccion-espanola', 'seleccion-uruguay', 'seleccion-arabia-saudi', 'equipo'],),
        (['equipo', 'seleccion-uruguay', 'seleccion-arabia-saudi', 'seleccion-suiza'],),
        (['seleccion-brasil', 'seleccion-marruecos', 'seleccion-escocia', 'haiti'],),
        (['seleccion-espanola', 'seleccion-espanola', 'seleccion-espanola', 'seleccion-espanola'],),
        (['seleccion-espanola', 'seleccion-uruguay', 'seleccion-arabia-saudi', 'seleccion-espanola'],)
    ]
)
def test_grupos_porra_correctos_equipos_error(porra_grupo):

    porra={'A': ['seleccion-mexico', 'republica-checa', 'seleccion-republica-corea', 'seleccion-sudafrica'],
    'B': ['seleccion-suiza', 'canada', 'seleccion-bosnia-herzegovina', 'seleccion-qatar'],
    'C': ['seleccion-brasil', 'seleccion-marruecos', 'seleccion-escocia', 'haiti'],
    'D': ['seleccion-estados-unidos', 'seleccion-turquia', 'seleccion-paraguay', 'seleccion-australia'],
    'E': ['seleccion-alemania', 'seleccion-ecuador', 'seleccion-costa-marfil', 'curazao'],
    'F': ['seleccion-holanda', 'seleccion-japon', 'seleccion-suecia', 'seleccion-tunez'],
    'G': ['seleccion-belgica', 'seleccion-egipto', 'seleccion-iran', 'seleccion-nueva-zelanda'],
    'H': porra_grupo,
    'I': ['seleccion-francia', 'seleccion-noruega', 'senegal', 'seleccion-iraq'],
    'J': ['seleccion-argentina', 'seleccion-austria', 'seleccion-argelia', 'jordania'],
    'K': ['seleccion-portugal', 'seleccion-colombia', 'rd-congo', 'seleccion-uzbekistan'],
    'L': ['seleccion-inglaterra', 'seleccion-croacia', 'seleccion-ghana', 'panama-seleccion']}

    real=[('A', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR'), ('A', 'seleccion-mexico', 'México', 3811, 'MEX'), ('A', 'republica-checa', 'República Checa', 6188, 'CZE'), ('A', 'seleccion-sudafrica', 'Sudáfrica', 3815, 'ZAF'),
    ('B', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH'), ('B', 'canada', 'Canadá', 5577, 'CAN'), ('B', 'seleccion-qatar', 'Catar', 3799, 'QAT'), ('B', 'seleccion-suiza', 'Suiza', 3723, 'CHE'),
    ('C', 'seleccion-brasil', 'Brasil', 3775, 'BRA'), ('C', 'seleccion-escocia', 'Escocia', 3758, 'SCO'), ('C', 'haiti', 'Haití', 5582, 'HTI'), ('C', 'seleccion-marruecos', 'Marruecos', 3780, 'MAR'),
    ('D', 'seleccion-australia', 'Australia', 3801, 'AUS'), ('D', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'), ('D', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY'), ('D', 'seleccion-turquia', 'Turquía', 3737, 'TUR'),
    ('E', 'seleccion-alemania', 'Alemania', 3734, 'DEU'), ('E', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV'), ('E', 'curazao', 'Curazao', 61757, 'CUR'), ('E', 'seleccion-ecuador', 'Ecuador', 3771, 'ECU'),
    ('F', 'seleccion-japon', 'Japón', 3798, 'JPN'), ('F', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD'), ('F', 'seleccion-suecia', 'Suecia', 3074, 'SWE'), ('F', 'seleccion-tunez', 'Túnez', 3783, 'TUN'),
    ('G', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'), ('G', 'seleccion-egipto', 'Egipto', 3788, 'EGY'), ('G', 'seleccion-iran', 'Irán', 3806, 'IRN'), ('G', 'seleccion-nueva-zelanda', 'Nueva Zelanda', 3808, 'NZL'),
    ('H', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'), ('H', 'cabo-verde', 'Cabo Verde', 9158, 'CPV'), ('H', 'seleccion-espanola', 'España', 3850, 'ESP'), ('H', 'seleccion-uruguay', 'Uruguay', 3768, 'URY'),
    ('I', 'seleccion-francia', 'Francia', 3750, 'FRA'), ('I', 'seleccion-iraq', 'Iraq', 3816, 'IRQ'), ('I', 'seleccion-noruega', 'Noruega', 3759, 'NOR'), ('I', 'senegal', 'Senegal', 5658, 'SEN'),
    ('J', 'seleccion-argelia', 'Argelia', 3787, 'DZA'), ('J', 'seleccion-argentina', 'Argentina', 3770, 'ARG'), ('J', 'seleccion-austria', 'Austria', 3767, 'AUT'), ('J', 'jordania', 'Jordania', 5480, 'JOR'),
    ('K', 'seleccion-colombia', 'Colombia', 3774, 'COL'), ('K', 'seleccion-portugal', 'Portugal', 3762, 'PRT'), ('K', 'rd-congo', 'RD Congo', 11591, 'COD'), ('K', 'seleccion-uzbekistan', 'Uzbekistán', 3800, 'UZB'),
    ('L', 'seleccion-croacia', 'Croacia', 3766, 'HRV'), ('L', 'seleccion-ghana', 'Ghana', 3791, 'GHA'), ('L', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG'), ('L', 'panama-seleccion', 'Panamá', 17581, 'PAN')]
    
    assert not gruposPorraCorrectos(real, porra)

def test_grupos_porra_correctos():

    porra={'A': ['seleccion-mexico', 'republica-checa', 'seleccion-republica-corea', 'seleccion-sudafrica'],
    'B': ['seleccion-suiza', 'canada', 'seleccion-bosnia-herzegovina', 'seleccion-qatar'],
    'C': ['seleccion-brasil', 'seleccion-marruecos', 'seleccion-escocia', 'haiti'],
    'D': ['seleccion-estados-unidos', 'seleccion-turquia', 'seleccion-paraguay', 'seleccion-australia'],
    'E': ['seleccion-alemania', 'seleccion-ecuador', 'seleccion-costa-marfil', 'curazao'],
    'F': ['seleccion-holanda', 'seleccion-japon', 'seleccion-suecia', 'seleccion-tunez'],
    'G': ['seleccion-belgica', 'seleccion-egipto', 'seleccion-iran', 'seleccion-nueva-zelanda'],
    'H': ['seleccion-espanola', 'seleccion-uruguay', 'seleccion-arabia-saudi', 'cabo-verde'],
    'I': ['seleccion-francia', 'seleccion-noruega', 'senegal', 'seleccion-iraq'],
    'J': ['seleccion-argentina', 'seleccion-austria', 'seleccion-argelia', 'jordania'],
    'K': ['seleccion-portugal', 'seleccion-colombia', 'rd-congo', 'seleccion-uzbekistan'],
    'L': ['seleccion-inglaterra', 'seleccion-croacia', 'seleccion-ghana', 'panama-seleccion']}

    real=[('A', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR'), ('A', 'seleccion-mexico', 'México', 3811, 'MEX'), ('A', 'republica-checa', 'República Checa', 6188, 'CZE'), ('A', 'seleccion-sudafrica', 'Sudáfrica', 3815, 'ZAF'),
    ('B', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH'), ('B', 'canada', 'Canadá', 5577, 'CAN'), ('B', 'seleccion-qatar', 'Catar', 3799, 'QAT'), ('B', 'seleccion-suiza', 'Suiza', 3723, 'CHE'),
    ('C', 'seleccion-brasil', 'Brasil', 3775, 'BRA'), ('C', 'seleccion-escocia', 'Escocia', 3758, 'SCO'), ('C', 'haiti', 'Haití', 5582, 'HTI'), ('C', 'seleccion-marruecos', 'Marruecos', 3780, 'MAR'),
    ('D', 'seleccion-australia', 'Australia', 3801, 'AUS'), ('D', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'), ('D', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY'), ('D', 'seleccion-turquia', 'Turquía', 3737, 'TUR'),
    ('E', 'seleccion-alemania', 'Alemania', 3734, 'DEU'), ('E', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV'), ('E', 'curazao', 'Curazao', 61757, 'CUR'), ('E', 'seleccion-ecuador', 'Ecuador', 3771, 'ECU'),
    ('F', 'seleccion-japon', 'Japón', 3798, 'JPN'), ('F', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD'), ('F', 'seleccion-suecia', 'Suecia', 3074, 'SWE'), ('F', 'seleccion-tunez', 'Túnez', 3783, 'TUN'),
    ('G', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'), ('G', 'seleccion-egipto', 'Egipto', 3788, 'EGY'), ('G', 'seleccion-iran', 'Irán', 3806, 'IRN'), ('G', 'seleccion-nueva-zelanda', 'Nueva Zelanda', 3808, 'NZL'),
    ('H', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'), ('H', 'cabo-verde', 'Cabo Verde', 9158, 'CPV'), ('H', 'seleccion-espanola', 'España', 3850, 'ESP'), ('H', 'seleccion-uruguay', 'Uruguay', 3768, 'URY'),
    ('I', 'seleccion-francia', 'Francia', 3750, 'FRA'), ('I', 'seleccion-iraq', 'Iraq', 3816, 'IRQ'), ('I', 'seleccion-noruega', 'Noruega', 3759, 'NOR'), ('I', 'senegal', 'Senegal', 5658, 'SEN'),
    ('J', 'seleccion-argelia', 'Argelia', 3787, 'DZA'), ('J', 'seleccion-argentina', 'Argentina', 3770, 'ARG'), ('J', 'seleccion-austria', 'Austria', 3767, 'AUT'), ('J', 'jordania', 'Jordania', 5480, 'JOR'),
    ('K', 'seleccion-colombia', 'Colombia', 3774, 'COL'), ('K', 'seleccion-portugal', 'Portugal', 3762, 'PRT'), ('K', 'rd-congo', 'RD Congo', 11591, 'COD'), ('K', 'seleccion-uzbekistan', 'Uzbekistán', 3800, 'UZB'),
    ('L', 'seleccion-croacia', 'Croacia', 3766, 'HRV'), ('L', 'seleccion-ghana', 'Ghana', 3791, 'GHA'), ('L', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG'), ('L', 'panama-seleccion', 'Panamá', 17581, 'PAN')]
    
    assert gruposPorraCorrectos(real, porra)

def test_obtener_terceros_grupos_equipos_limpios_no_hay():

    assert not obtenerTercerosGruposEquiposLimpios([])

def test_obtener_terceros_grupos_equipos_limpios():

    terceros_grupos=[('A', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR'),
                    ('B', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH'),
                    ('C', 'seleccion-escocia', 'Escocia', 3758, 'SCO'),
                    ('D', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY'),
                    ('E', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV'),
                    ('F', 'seleccion-suecia', 'Suecia', 3074, 'SWE'),
                    ('G', 'seleccion-iran', 'Irán', 3806, 'IRN'),
                    ('H', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'),
                    ('I', 'senegal', 'Senegal', 5658, 'SEN'),
                    ('J', 'seleccion-argelia', 'Argelia', 3787, 'DZA'),
                    ('K', 'rd-congo', 'RD Congo', 11591, 'COD'),
                    ('L', 'seleccion-ghana', 'Ghana', 3791, 'GHA')]

    terceros_grupos_limpios=obtenerTercerosGruposEquiposLimpios(terceros_grupos)

    assert len(terceros_grupos_limpios)==12

@pytest.mark.parametrize(["porra_mejores_terceros"],
    [
        ([{'equipo_id': 'seleccion-brasil', 'grupo': 'C'},
            {'equipo_id': 'seleccion-espanola', 'grupo': 'H'},
            {'equipo_id': 'seleccion-alemania', 'grupo': 'E'},
            {'equipo_id': 'seleccion-holanda', 'grupo': 'F'},
            {'equipo_id': 'seleccion-francia', 'grupo': 'I'},
            {'equipo_id': 'seleccion-argentina', 'grupo': 'J'},
            {'equipo_id': 'seleccion-inglaterra', 'grupo': 'L'}],),
        ([{'equipo_id': 'seleccion-brasil', 'grupo': 'C'},
            {'equipo_id': 'seleccion-espanola', 'grupo': 'H'},
            {'equipo_id': 'seleccion-inglaterra', 'grupo': 'L'}],),
        ([{'equipo_id': 'seleccion-brasil', 'grupo': 'C'}],),
        ([],),
        ([{'equipo_id': 'seleccion-brasil', 'grupo': 'C'},
            {'equipo_id': 'seleccion-espanola', 'grupo': 'H'},
            {'equipo_id': 'seleccion-alemania', 'grupo': 'E'},
            {'equipo_id': 'seleccion-holanda', 'grupo': 'F'},
            {'equipo_id': 'seleccion-francia', 'grupo': 'I'},
            {'equipo_id': 'seleccion-argentina', 'grupo': 'J'},
            {'equipo_id': 'seleccion-portugal', 'grupo': 'K'},
            {'equipo_id': 'seleccion-inglaterra', 'grupo': 'L'},
            {'equipo_id': 'seleccion-belgica', 'grupo': 'G'}],),
        ([{'equipo_id': 'seleccion-brasil', 'grupo': 'C'},
            {'equipo_id': 'seleccion-brasil', 'grupo': 'C'},
            {'equipo_id': 'seleccion-brasil', 'grupo': 'C'},
            {'equipo_id': 'seleccion-brasil', 'grupo': 'C'},
            {'equipo_id': 'seleccion-brasil', 'grupo': 'C'},
            {'equipo_id': 'seleccion-brasil', 'grupo': 'C'},
            {'equipo_id': 'seleccion-brasil', 'grupo': 'C'},
            {'equipo_id': 'seleccion-brasil', 'grupo': 'C'}],),
        ([{'equipo_id': 'seleccion-brasil', 'grupo': 'C'},
            {'equipo_id': 'seleccion-espanola', 'grupo': 'H'},
            {'equipo_id': 'seleccion-alemania', 'grupo': 'E'},
            {'equipo_id': 'seleccion-holanda', 'grupo': 'F'},
            {'equipo_id': 'seleccion-francia', 'grupo': 'I'},
            {'equipo_id': 'seleccion-argentina', 'grupo': 'J'},
            {'equipo_id': 'seleccion-portugal', 'grupo': 'K'},
            {'equipo_id': 'seleccion-brasil', 'grupo': 'C'}],),
        ([{'equipo_id': 'seleccion-brasil', 'grupo': 'C'},
            {'equipo_id': 'seleccion-espanola', 'grupo': 'H'},
            {'equipo_id': 'seleccion-alemania', 'grupo': 'E'},
            {'equipo_id': 'seleccion-holanda', 'grupo': 'F'},
            {'equipo_id': 'seleccion-francia', 'grupo': 'I'},
            {'equipo_id': 'seleccion-argentina', 'grupo': 'J'},
            {'equipo_id': 'seleccion-portugal', 'grupo': 'K'},
            {'equipo_id': 'seleccion-brasil', 'grupo': 'L'}],),
        ([{'equipo_id': 'seleccion-brasil', 'grupo': 'C'},
            {'equipo_id': 'seleccion-espanola', 'grupo': 'H'},
            {'equipo_id': 'seleccion-alemania', 'grupo': 'E'},
            {'equipo_id': 'seleccion-holanda', 'grupo': 'F'},
            {'equipo_id': 'seleccion-francia', 'grupo': 'I'},
            {'equipo_id': 'seleccion-argentina', 'grupo': 'J'},
            {'equipo_id': 'seleccion-portugal', 'grupo': 'K'},
            {'equipo_id': 'seleccion-inglaterra', 'grupo': 'C'}],)
    ]
)
def test_mejores_terceros_porra_correctos_dimension_error(porra_mejores_terceros):

    real_usuario=[('A', 'seleccion-mexico', 'México', 3811, 'MEX'),
                    ('B', 'seleccion-suiza', 'Suiza', 3723, 'CHE'),
                    ('C', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                    ('D', 'seleccion-turquia', 'Turquía', 3737, 'TUR'),
                    ('E', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                    ('F', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD'),
                    ('G', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                    ('H', 'seleccion-espanola', 'España', 3850, 'ESP'),
                    ('I', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                    ('J', 'seleccion-argentina', 'Argentina', 3770, 'ARG'),
                    ('K', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                    ('L', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG')]
    
    assert not mejoresTercerosPorraCorrectos(real_usuario, porra_mejores_terceros)

@pytest.mark.parametrize(["porra_mejores_terceros"],
    [
        ([{'equipo_id': 'seleccion-brasil', 'grupo': 'A'},
            {'equipo_id': 'seleccion-espanola', 'grupo': 'H'},
            {'equipo_id': 'seleccion-alemania', 'grupo': 'E'},
            {'equipo_id': 'seleccion-holanda', 'grupo': 'F'},
            {'equipo_id': 'seleccion-francia', 'grupo': 'I'},
            {'equipo_id': 'seleccion-argentina', 'grupo': 'J'},
            {'equipo_id': 'seleccion-portugal', 'grupo': 'K'},
            {'equipo_id': 'seleccion-inglaterra', 'grupo': 'L'}],),
        ([{'equipo_id': 'seleccion-marruecos', 'grupo': 'C'},
            {'equipo_id': 'seleccion-espanola', 'grupo': 'H'},
            {'equipo_id': 'seleccion-alemania', 'grupo': 'E'},
            {'equipo_id': 'seleccion-holanda', 'grupo': 'F'},
            {'equipo_id': 'seleccion-francia', 'grupo': 'I'},
            {'equipo_id': 'seleccion-argentina', 'grupo': 'J'},
            {'equipo_id': 'seleccion-portugal', 'grupo': 'K'},
            {'equipo_id': 'seleccion-inglaterra', 'grupo': 'L'}],),
        ([{'equipo_id': 'seleccion-marruecos', 'grupo': 'C'},
            {'equipo_id': 'seleccion-espanola', 'grupo': 'H'},
            {'equipo_id': 'seleccion-alemania', 'grupo': 'E'},
            {'equipo_id': 'seleccion-holanda', 'grupo': 'F'},
            {'equipo_id': 'seleccion-francia', 'grupo': 'I'},
            {'equipo_id': 'seleccion-argentina', 'grupo': 'J'},
            {'equipo_id': 'seleccion-portugal', 'grupo': 'K'},
            {'equipo_id': 'seleccion-inglaterra', 'grupo': 'Z'}],)
    ]
)
def test_mejores_terceros_porra_correctos_equipos_error(porra_mejores_terceros):

    real_usuario=[('A', 'seleccion-mexico', 'México', 3811, 'MEX'),
                    ('B', 'seleccion-suiza', 'Suiza', 3723, 'CHE'),
                    ('C', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                    ('D', 'seleccion-turquia', 'Turquía', 3737, 'TUR'),
                    ('E', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                    ('F', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD'),
                    ('G', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                    ('H', 'seleccion-espanola', 'España', 3850, 'ESP'),
                    ('I', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                    ('J', 'seleccion-argentina', 'Argentina', 3770, 'ARG'),
                    ('K', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                    ('L', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG')]
    
    assert not mejoresTercerosPorraCorrectos(real_usuario, porra_mejores_terceros)

@pytest.mark.parametrize(["porra_mejores_terceros"],
    [
        ([{'equipo_id': 'seleccion-brasil', 'grupo': 'C'},
            {'equipo_id': 'seleccion-espanola', 'grupo': 'H'},
            {'equipo_id': 'seleccion-alemania', 'grupo': 'E'},
            {'equipo_id': 'seleccion-holanda', 'grupo': 'F'},
            {'equipo_id': 'seleccion-francia', 'grupo': 'I'},
            {'equipo_id': 'seleccion-argentina', 'grupo': 'J'},
            {'equipo_id': 'seleccion-portugal', 'grupo': 'K'},
            {'equipo_id': 'seleccion-inglaterra', 'grupo': 'L'}],),
        ([{'equipo_id': 'seleccion-mexico', 'grupo': 'A'},
            {'equipo_id': 'seleccion-espanola', 'grupo': 'H'},
            {'equipo_id': 'seleccion-alemania', 'grupo': 'E'},
            {'equipo_id': 'seleccion-holanda', 'grupo': 'F'},
            {'equipo_id': 'seleccion-francia', 'grupo': 'I'},
            {'equipo_id': 'seleccion-argentina', 'grupo': 'J'},
            {'equipo_id': 'seleccion-portugal', 'grupo': 'K'},
            {'equipo_id': 'seleccion-inglaterra', 'grupo': 'L'}],),
        ([{'equipo_id': 'seleccion-mexico', 'grupo': 'A'},
            {'equipo_id': 'seleccion-espanola', 'grupo': 'H'},
            {'equipo_id': 'seleccion-turquia', 'grupo': 'D'},
            {'equipo_id': 'seleccion-holanda', 'grupo': 'F'},
            {'equipo_id': 'seleccion-francia', 'grupo': 'I'},
            {'equipo_id': 'seleccion-argentina', 'grupo': 'J'},
            {'equipo_id': 'seleccion-portugal', 'grupo': 'K'},
            {'equipo_id': 'seleccion-inglaterra', 'grupo': 'L'}],),
        ([{'equipo_id': 'seleccion-mexico', 'grupo': 'A'},
            {'equipo_id': 'seleccion-espanola', 'grupo': 'H'},
            {'equipo_id': 'seleccion-turquia', 'grupo': 'D'},
            {'equipo_id': 'seleccion-holanda', 'grupo': 'F'},
            {'equipo_id': 'seleccion-francia', 'grupo': 'I'},
            {'equipo_id': 'seleccion-argentina', 'grupo': 'J'},
            {'equipo_id': 'seleccion-suiza', 'grupo': 'B'},
            {'equipo_id': 'seleccion-belgica', 'grupo': 'G'}],),
    ]
)
def test_mejores_terceros_porra_correctos(porra_mejores_terceros):

    real_usuario=[('A', 'seleccion-mexico', 'México', 3811, 'MEX'),
                    ('B', 'seleccion-suiza', 'Suiza', 3723, 'CHE'),
                    ('C', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                    ('D', 'seleccion-turquia', 'Turquía', 3737, 'TUR'),
                    ('E', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                    ('F', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD'),
                    ('G', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                    ('H', 'seleccion-espanola', 'España', 3850, 'ESP'),
                    ('I', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                    ('J', 'seleccion-argentina', 'Argentina', 3770, 'ARG'),
                    ('K', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                    ('L', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG')]
    
    assert mejoresTercerosPorraCorrectos(real_usuario, porra_mejores_terceros)

@pytest.mark.parametrize(["estado", "paso"],
    [
        ({'grupo_completo': False, 'mejor_tercero_completo': False, "eliminatorias_completa": False, "porra_completa": False}, 0),
        ({'grupo_completo': True, 'mejor_tercero_completo': False, "eliminatorias_completa": False, "porra_completa": False}, 1),
        ({'grupo_completo': True, 'mejor_tercero_completo': True, "eliminatorias_completa": False, "porra_completa": False}, 2),
        ({'grupo_completo': True, 'mejor_tercero_completo': True, "eliminatorias_completa": True, "porra_completa": False}, 3),
        ({'grupo_completo': True, 'mejor_tercero_completo': True, "eliminatorias_completa": True, "porra_completa": True}, 4)
    ]
)
def test_obtener_paso_estado(estado, paso):

    assert obtenerPasoEstado(estado)==paso

@pytest.mark.parametrize(["estado_porra", "paso"],
    [((False, False, False, False), 0), ((True, False, False, False), 1), ((True, True, False, False), 2), ((True, True, True, False), 3), ((True, True, True, True), 4)]
)
def test_obtener_pasos_porra(estado_porra, paso):

    assert obtenerPasosPorra(estado_porra)==paso

def test_obtener_combinacion_mejores_terceros_no_hay():

    assert not obtenerCombinacionMejoresTerceros([])

def test_obtener_combinacion_mejores_terceros():

    mejores_terceros=[('A', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 3),
                        ('B', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 3),
                        ('C', 'seleccion-escocia', 'Escocia', 3758, 'SCO', 3), ('D', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 3),
                        ('F', 'seleccion-suecia', 'Suecia', 3074, 'SWE', 3),
                        ('H', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 3), ('I', 'senegal', 'Senegal', 5658, 'SEN', 3),
                        ('L', 'seleccion-ghana', 'Ghana', 3791, 'GHA', 3)]

    combinacion_mejores_terceros=obtenerCombinacionMejoresTerceros(mejores_terceros)

    assert len(combinacion_mejores_terceros)==8

def test_construir_lookup_no_hay():

    assert not construirLookup([], [])

def test_construir_lookup():

    primero_segundos=[('A', 'seleccion-mexico', 'México', 3811, 'MEX', 1),
                        ('B', 'seleccion-suiza', 'Suiza', 3723, 'CHE', 1),
                        ('C', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 1),
                        ('D', 'seleccion-turquia', 'Turquía', 3737, 'TUR', 1),
                        ('E', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 1),
                        ('F', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 1),
                        ('G', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 1),
                        ('H', 'seleccion-espanola', 'España', 3850, 'ESP', 1),
                        ('I', 'seleccion-francia', 'Francia', 3750, 'FRA', 1),
                        ('J', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 1),
                        ('K', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 1),
                        ('L', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG', 1),
                        ('A', 'republica-checa', 'República Checa', 6188, 'CZE', 2),
                        ('B', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 2),
                        ('C', 'seleccion-marruecos', 'Marruecos', 3780, 'MAR', 2),
                        ('D', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 2),
                        ('E', 'seleccion-ecuador', 'Ecuador', 3771, 'ECU', 2),
                        ('F', 'seleccion-japon', 'Japón', 3798, 'JPN', 2),
                        ('G', 'seleccion-egipto', 'Egipto', 3788, 'EGY', 2),
                        ('H', 'seleccion-uruguay', 'Uruguay', 3768, 'URY', 2),
                        ('I', 'seleccion-noruega', 'Noruega', 3759, 'NOR', 2),
                        ('J', 'seleccion-austria', 'Austria', 3767, 'AUT', 2),
                        ('K', 'seleccion-colombia', 'Colombia', 3774, 'COL', 2),
                        ('L', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 2)]

    terceros=[('A', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 3),
                ('C', 'seleccion-escocia', 'Escocia', 3758, 'SCO', 3),
                ('D', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 3),
                ('E', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV', 3),
                ('F', 'seleccion-tunez', 'Túnez', 3783, 'TUN', 3),
                ('H', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 3),
                ('I', 'senegal', 'Senegal', 5658, 'SEN', 3),
                ('L', 'seleccion-ghana', 'Ghana', 3791, 'GHA', 3)]

    lookup=construirLookup(primero_segundos, terceros)

    assert len(lookup)==32
    assert len(lookup) == len(set(lookup.keys()))

    for g in "ABCDEFGHIJKL":

        assert f"1{g}" in lookup
        assert f"2{g}" in lookup

    for g in "ACDEFHIL":

        assert f"3{g}" in lookup

def test_crear_bracket_dieciseisavos_no_hay():

    partidos_variables_equipo_tercero={'M74': '3C', 'M77': '3D', 'M79': '3H', 'M80': '3I', 'M81': '3F', 'M82': '3A', 'M85': '3E', 'M87': '3L'}

    assert not crearBracketDieciseisavos(partidos_variables_equipo_tercero, [], [])

def test_crear_bracket_dieciseisavos():

    primero_segundos=[('A', 'seleccion-mexico', 'México', 3811, 'MEX', 1),
                        ('B', 'seleccion-suiza', 'Suiza', 3723, 'CHE', 1),
                        ('C', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 1),
                        ('D', 'seleccion-turquia', 'Turquía', 3737, 'TUR', 1),
                        ('E', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 1),
                        ('F', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 1),
                        ('G', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 1),
                        ('H', 'seleccion-espanola', 'España', 3850, 'ESP', 1),
                        ('I', 'seleccion-francia', 'Francia', 3750, 'FRA', 1),
                        ('J', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 1),
                        ('K', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 1),
                        ('L', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG', 1),
                        ('A', 'republica-checa', 'República Checa', 6188, 'CZE', 2),
                        ('B', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 2),
                        ('C', 'seleccion-marruecos', 'Marruecos', 3780, 'MAR', 2),
                        ('D', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 2),
                        ('E', 'seleccion-ecuador', 'Ecuador', 3771, 'ECU', 2),
                        ('F', 'seleccion-japon', 'Japón', 3798, 'JPN', 2),
                        ('G', 'seleccion-egipto', 'Egipto', 3788, 'EGY', 2),
                        ('H', 'seleccion-uruguay', 'Uruguay', 3768, 'URY', 2),
                        ('I', 'seleccion-noruega', 'Noruega', 3759, 'NOR', 2),
                        ('J', 'seleccion-austria', 'Austria', 3767, 'AUT', 2),
                        ('K', 'seleccion-colombia', 'Colombia', 3774, 'COL', 2),
                        ('L', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 2)]

    terceros=[('A', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 3),
                ('C', 'seleccion-escocia', 'Escocia', 3758, 'SCO', 3),
                ('D', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 3),
                ('E', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV', 3),
                ('F', 'seleccion-tunez', 'Túnez', 3783, 'TUN', 3),
                ('H', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 3),
                ('I', 'senegal', 'Senegal', 5658, 'SEN', 3),
                ('L', 'seleccion-ghana', 'Ghana', 3791, 'GHA', 3)]

    partidos_variables_equipo_tercero={'M74': '3C', 'M77': '3D', 'M79': '3H', 'M80': '3I', 'M81': '3F', 'M82': '3A', 'M85': '3E', 'M87': '3L'}

    bracket_16avos=crearBracketDieciseisavos(partidos_variables_equipo_tercero, primero_segundos, terceros)

    assert len(bracket_16avos)==16

    partidos=["M73","M74","M75","M76","M77","M78","M79","M80", "M81","M82","M83","M84","M85","M86","M87","M88"]

    for partido in partidos:

        assert partido in bracket_16avos

    for equipos in bracket_16avos.values():

        assert len(equipos)==2
        assert all(isinstance(e, tuple) for e in equipos)
        assert all(len(e)==4 for e in equipos)

def test_test_bracket_eliminatorias_correcto_no_es_lista():

    assert not bracketEliminatoriasCorrecto("no soy una lista", {})
    
@pytest.mark.parametrize(["partido"],
    [("M104",), ("M102",), ("M99",), ("M88",)]
)
def test_bracket_eliminatorias_correcto_falta_un_partido(partidos_bracket, bracket_16avos_real, partido):

    bracket=copy.deepcopy(partidos_bracket)

    bracket=[p for p in partidos_bracket if p["partido"]!=partido]

    assert not bracketEliminatoriasCorrecto(bracket, bracket_16avos_real)

def test_bracket_eliminatorias_correcto_partido_duplicado(partidos_bracket, bracket_16avos_real):

    bracket=copy.deepcopy(partidos_bracket)

    bracket.append(copy.deepcopy(bracket[0]))

    assert not bracketEliminatoriasCorrecto(bracket, bracket_16avos_real)

def test_bracket_eliminatorias_correcto_partido_no_valido(partidos_bracket, bracket_16avos_real):

    bracket=copy.deepcopy(partidos_bracket)

    bracket[0]["partido"]="M999"

    assert not bracketEliminatoriasCorrecto(bracket, bracket_16avos_real)

def test_bracket_eliminatorias_correcto_ronda_incorrecta(partidos_bracket, bracket_16avos_real):

    bracket=copy.deepcopy(partidos_bracket)

    partido=next(p for p in bracket if p["partido"]=="M89")

    partido["ronda"]="cuartos"

    assert not bracketEliminatoriasCorrecto(bracket, bracket_16avos_real)

def test_bracket_eliminatorias_correcto_ganador_no_juega_el_partido(partidos_bracket, bracket_16avos_real):

    bracket=copy.deepcopy(partidos_bracket)

    partido=next(p for p in bracket if p["partido"]=="M73")

    partido["ganador_id"]="seleccion-falsa"

    assert not bracketEliminatoriasCorrecto(bracket, bracket_16avos_real)

def test_bracket_eliminatorias_correcto_equipo_repetido_en_mismo_partido(partidos_bracket, bracket_16avos_real):

    bracket=copy.deepcopy(partidos_bracket)

    partido=next(p for p in bracket if p["partido"]=="M73")

    partido["equipo_2_id"]=partido["equipo_1_id"]

    assert not bracketEliminatoriasCorrecto(bracket, bracket_16avos_real)

def test_bracket_eliminatorias_correcto_campo_vacio(partidos_bracket, bracket_16avos_real):

    bracket=copy.deepcopy(partidos_bracket)

    partido=next(p for p in bracket if p["partido"]=="M73")

    partido["ganador_id"]=""

    assert not bracketEliminatoriasCorrecto(bracket, bracket_16avos_real)

def test_bracket_eliminatorias_correcto_16avos_no_coinciden_con_backend(partidos_bracket, bracket_16avos_real):

    bracket=copy.deepcopy(partidos_bracket)

    partido=next(p for p in bracket if p["partido"]=="M73")

    partido["equipo_1_id"]="seleccion-falsa"

    assert not bracketEliminatoriasCorrecto(bracket, bracket_16avos_real)

def test_bracket_eliminatorias_correcto_octavos_no_salen_de_los_ganadores_de_16avos(partidos_bracket, bracket_16avos_real):

    bracket=copy.deepcopy(partidos_bracket)

    partido=next(p for p in bracket if p["partido"]=="M89")

    partido["equipo_1_id"]="seleccion-falsa"

    assert not bracketEliminatoriasCorrecto(bracket, bracket_16avos_real)

def test_bracket_eliminatorias_correcto_cuartos_no_salen_de_los_ganadores_de_octavos(partidos_bracket, bracket_16avos_real):

    bracket=copy.deepcopy(partidos_bracket)

    partido=next(p for p in bracket if p["partido"]=="M97")

    partido["equipo_2_id"]="seleccion-falsa"

    assert not bracketEliminatoriasCorrecto(bracket, bracket_16avos_real)

def test_bracket_eliminatorias_correcto_semis_no_salen_de_los_ganadores_de_cuartos(partidos_bracket, bracket_16avos_real):

    bracket=copy.deepcopy(partidos_bracket)

    partido=next(p for p in bracket if p["partido"]=="M101")

    partido["equipo_1_id"]="seleccion-falsa"

    assert not bracketEliminatoriasCorrecto(bracket, bracket_16avos_real)

def test_bracket_eliminatorias_correcto_final_no_tiene_ganadores_de_semis(partidos_bracket, bracket_16avos_real):

    bracket=copy.deepcopy(partidos_bracket)

    partido=next(p for p in bracket if p["partido"]=="M104")

    partido["equipo_1_id"]="seleccion-falsa"

    assert not bracketEliminatoriasCorrecto(bracket, bracket_16avos_real)

def test_bracket_eliminatorias_correcto_tercer_puesto_no_tiene_perdedores_de_semis(partidos_bracket, bracket_16avos_real):

    bracket=copy.deepcopy(partidos_bracket)

    partido=next(p for p in bracket if p["partido"]=="M103")

    partido["equipo_1_id"]="seleccion-falsa"

    assert not bracketEliminatoriasCorrecto(bracket, bracket_16avos_real)

def test_bracket_eliminatorias_correcto_ganador_de_tercer_puesto_no_juega(partidos_bracket, bracket_16avos_real):

    bracket=copy.deepcopy(partidos_bracket)

    partido=next(p for p in bracket if p["partido"]=="M103")

    partido["ganador_id"]="seleccion-falsa"

    assert not bracketEliminatoriasCorrecto(bracket, bracket_16avos_real)

def test_bracket_eliminatorias_correcto_ganador_de_final_no_juega(partidos_bracket, bracket_16avos_real):

    bracket=copy.deepcopy(partidos_bracket)

    partido=next(p for p in bracket if p["partido"]=="M104")

    partido["ganador_id"]="seleccion-falsa"

    assert not bracketEliminatoriasCorrecto(bracket, bracket_16avos_real)

def test_bracket_eliminatorias_correcto(partidos_bracket, bracket_16avos_real):

    assert bracketEliminatoriasCorrecto(partidos_bracket, bracket_16avos_real)

def test_obtener_eliminatorias_porra_limpios_no_hay():

    assert not obtenerEliminatoriasPorraLimpias([])

def test_obtener_eliminatorias_porra_limpios():

    eliminatorias_porra=[('dieciseisavos', 'M73', 'seleccion-mexico', 'México', 3811, 'MEX', 'canada', 'Canadá', 5577, 'CAN', 'seleccion-mexico', 'México', 3811, 'MEX'),
                        ('dieciseisavos', 'M74', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'haiti', 'Haití', 5582, 'HTI', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('dieciseisavos', 'M75', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-escocia', 'Escocia', 3758, 'SCO', 'seleccion-japon', 'Japón', 3798, 'JPN'),
                        ('dieciseisavos', 'M76', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('dieciseisavos', 'M77', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-suecia', 'Suecia', 3074, 'SWE', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('dieciseisavos', 'M78', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV', 'seleccion-iraq', 'Iraq', 3816, 'IRQ', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV'),
                        ('dieciseisavos', 'M79', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-espanola', 'España', 3850, 'ESP'),
                        ('dieciseisavos', 'M80', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'curazao', 'Curazao', 61757, 'CUR', 'seleccion-croacia', 'Croacia', 3766, 'HRV'),
                        ('dieciseisavos', 'M81', 'seleccion-australia', 'Australia', 3801, 'AUS', 'seleccion-qatar', 'Catar', 3799, 'QAT', 'seleccion-australia', 'Australia', 3801, 'AUS'),
                        ('dieciseisavos', 'M82', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'republica-checa', 'República Checa', 6188, 'CZE', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('dieciseisavos', 'M83', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-ghana', 'Ghana', 3791, 'GHA', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('dieciseisavos', 'M84', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'),
                        ('dieciseisavos', 'M85', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-iran', 'Irán', 3806, 'IRN', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH'),
                        ('dieciseisavos', 'M86', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'cabo-verde', 'Cabo Verde', 9158, 'CPV', 'seleccion-argelia', 'Argelia', 3787, 'DZA'),
                        ('dieciseisavos', 'M87', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-colombia', 'Colombia', 3774, 'COL'),
                        ('dieciseisavos', 'M88', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-egipto', 'Egipto', 3788, 'EGY', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('octavos', 'M89', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('octavos', 'M90', 'seleccion-mexico', 'México', 3811, 'MEX', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-japon', 'Japón', 3798, 'JPN'),
                        ('octavos', 'M91', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('octavos', 'M92', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'seleccion-espanola', 'España', 3850, 'ESP'),
                        ('octavos', 'M93', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('octavos', 'M94', 'seleccion-australia', 'Australia', 3801, 'AUS', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('octavos', 'M95', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('octavos', 'M96', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-colombia', 'Colombia', 3774, 'COL'),
                        ('cuartos', 'M97', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('cuartos', 'M98', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('cuartos', 'M99', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-espanola', 'España', 3850, 'ESP'),
                        ('cuartos', 'M100', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-colombia', 'Colombia', 3774, 'COL'),
                        ('semifinales', 'M101', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('semifinales', 'M102', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-espanola', 'España', 3850, 'ESP'),
                        ('tercer_puesto', 'M103', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('final', 'M104', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-espanola', 'España', 3850, 'ESP')]

    eliminatorias_porra_limpios=obtenerEliminatoriasPorraLimpias(eliminatorias_porra)

    assert len(eliminatorias_porra_limpios)==32

def test_obtener_eliminatorias_real_limpios_no_hay():

    assert not obtenerEliminatoriasRealLimpias([])

def test_obtener_eliminatorias_real_limpios_sin_ganadores():

    eliminatorias_real=[('dieciseisavos', 'M73', 'seleccion-mexico', 'México', 3811, 'MEX', 'canada', 'Canadá', 5577, 'CAN', None, None, None, None),
                        ('dieciseisavos', 'M74', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'haiti', 'Haití', 5582, 'HTI', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('dieciseisavos', 'M75', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-escocia', 'Escocia', 3758, 'SCO', 'seleccion-japon', 'Japón', 3798, 'JPN'),
                        ('dieciseisavos', 'M76', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('dieciseisavos', 'M77', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-suecia', 'Suecia', 3074, 'SWE', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('dieciseisavos', 'M78', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV', 'seleccion-iraq', 'Iraq', 3816, 'IRQ', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV'),
                        ('dieciseisavos', 'M79', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-espanola', 'España', 3850, 'ESP', None, None, None, None),
                        ('dieciseisavos', 'M80', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'curazao', 'Curazao', 61757, 'CUR', 'seleccion-croacia', 'Croacia', 3766, 'HRV'),
                        ('dieciseisavos', 'M81', 'seleccion-australia', 'Australia', 3801, 'AUS', 'seleccion-qatar', 'Catar', 3799, 'QAT', 'seleccion-australia', 'Australia', 3801, 'AUS'),
                        ('dieciseisavos', 'M82', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'republica-checa', 'República Checa', 6188, 'CZE', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('dieciseisavos', 'M83', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-ghana', 'Ghana', 3791, 'GHA', None, None, None, None),
                        ('dieciseisavos', 'M84', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'),
                        ('dieciseisavos', 'M85', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-iran', 'Irán', 3806, 'IRN', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH'),
                        ('dieciseisavos', 'M86', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'cabo-verde', 'Cabo Verde', 9158, 'CPV', 'seleccion-argelia', 'Argelia', 3787, 'DZA'),
                        ('dieciseisavos', 'M87', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-colombia', 'Colombia', 3774, 'COL'),
                        ('dieciseisavos', 'M88', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-egipto', 'Egipto', 3788, 'EGY', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('octavos', 'M89', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('octavos', 'M90', 'seleccion-mexico', 'México', 3811, 'MEX', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-japon', 'Japón', 3798, 'JPN'),
                        ('octavos', 'M91', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('octavos', 'M92', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'seleccion-espanola', 'España', 3850, 'ESP'),
                        ('octavos', 'M93', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('octavos', 'M94', 'seleccion-australia', 'Australia', 3801, 'AUS', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('octavos', 'M95', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('octavos', 'M96', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-colombia', 'Colombia', 3774, 'COL'),
                        ('cuartos', 'M97', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('cuartos', 'M98', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('cuartos', 'M99', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-espanola', 'España', 3850, 'ESP'),
                        ('cuartos', 'M100', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-colombia', 'Colombia', 3774, 'COL'),
                        ('semifinales', 'M101', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('semifinales', 'M102', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-espanola', 'España', 3850, 'ESP'),
                        ('tercer_puesto', 'M103', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('final', 'M104', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-espanola', 'España', 3850, 'ESP')]

    eliminatorias_real_limpios=obtenerEliminatoriasRealLimpias(eliminatorias_real)

    assert len(eliminatorias_real_limpios)==32

    eliminatorias_sin_ganador=[eliminatoria for eliminatoria in eliminatorias_real_limpios.values() if eliminatoria["ganador"] is None]

    assert len(eliminatorias_sin_ganador)==3

def test_obtener_eliminatorias_real_limpios():

    eliminatorias_real=[('dieciseisavos', 'M73', 'seleccion-mexico', 'México', 3811, 'MEX', 'canada', 'Canadá', 5577, 'CAN', 'seleccion-mexico', 'México', 3811, 'MEX'),
                        ('dieciseisavos', 'M74', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'haiti', 'Haití', 5582, 'HTI', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('dieciseisavos', 'M75', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-escocia', 'Escocia', 3758, 'SCO', 'seleccion-japon', 'Japón', 3798, 'JPN'),
                        ('dieciseisavos', 'M76', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('dieciseisavos', 'M77', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-suecia', 'Suecia', 3074, 'SWE', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('dieciseisavos', 'M78', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV', 'seleccion-iraq', 'Iraq', 3816, 'IRQ', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV'),
                        ('dieciseisavos', 'M79', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-espanola', 'España', 3850, 'ESP'),
                        ('dieciseisavos', 'M80', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'curazao', 'Curazao', 61757, 'CUR', 'seleccion-croacia', 'Croacia', 3766, 'HRV'),
                        ('dieciseisavos', 'M81', 'seleccion-australia', 'Australia', 3801, 'AUS', 'seleccion-qatar', 'Catar', 3799, 'QAT', 'seleccion-australia', 'Australia', 3801, 'AUS'),
                        ('dieciseisavos', 'M82', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'republica-checa', 'República Checa', 6188, 'CZE', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('dieciseisavos', 'M83', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-ghana', 'Ghana', 3791, 'GHA', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('dieciseisavos', 'M84', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'),
                        ('dieciseisavos', 'M85', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-iran', 'Irán', 3806, 'IRN', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH'),
                        ('dieciseisavos', 'M86', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'cabo-verde', 'Cabo Verde', 9158, 'CPV', 'seleccion-argelia', 'Argelia', 3787, 'DZA'),
                        ('dieciseisavos', 'M87', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-colombia', 'Colombia', 3774, 'COL'),
                        ('dieciseisavos', 'M88', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-egipto', 'Egipto', 3788, 'EGY', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('octavos', 'M89', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('octavos', 'M90', 'seleccion-mexico', 'México', 3811, 'MEX', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-japon', 'Japón', 3798, 'JPN'),
                        ('octavos', 'M91', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('octavos', 'M92', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'seleccion-espanola', 'España', 3850, 'ESP'),
                        ('octavos', 'M93', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('octavos', 'M94', 'seleccion-australia', 'Australia', 3801, 'AUS', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('octavos', 'M95', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('octavos', 'M96', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-colombia', 'Colombia', 3774, 'COL'),
                        ('cuartos', 'M97', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('cuartos', 'M98', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('cuartos', 'M99', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-espanola', 'España', 3850, 'ESP'),
                        ('cuartos', 'M100', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-colombia', 'Colombia', 3774, 'COL'),
                        ('semifinales', 'M101', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('semifinales', 'M102', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-espanola', 'España', 3850, 'ESP'),
                        ('tercer_puesto', 'M103', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('final', 'M104', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-espanola', 'España', 3850, 'ESP')]

    eliminatorias_real_limpios=obtenerEliminatoriasRealLimpias(eliminatorias_real)

    assert len(eliminatorias_real_limpios)==32

    eliminatorias_sin_ganador=[eliminatoria for eliminatoria in eliminatorias_real_limpios.values() if eliminatoria["ganador"] is None]

    assert len(eliminatorias_sin_ganador)==0

def test_crear_carpeta_no_existe():

    ruta_carpeta=os.path.join(os.getcwd(), "testutilidades", "Prueba")

    assert not os.path.exists(ruta_carpeta)

    crearCarpeta(ruta_carpeta)

    assert os.path.exists(ruta_carpeta)

def test_crear_carpeta_existe():

    ruta_carpeta=os.path.join(os.getcwd(), "testutilidades", "Prueba")

    assert os.path.exists(ruta_carpeta)

    crearCarpeta(ruta_carpeta)

    assert os.path.exists(ruta_carpeta)

    os.rmdir(ruta_carpeta)

def test_borrar_carpeta_no_existe():

    ruta_carpeta=os.path.join(os.getcwd(), "testutilidades", "Prueba")

    assert not os.path.exists(ruta_carpeta)

    borrarCarpeta(ruta_carpeta)

    assert not os.path.exists(ruta_carpeta)

def test_borrar_carpeta_existe():

    ruta_carpeta=os.path.join(os.getcwd(), "testutilidades", "Prueba")

    crearCarpeta(ruta_carpeta)

    assert os.path.exists(ruta_carpeta)

    borrarCarpeta(ruta_carpeta)

    assert not os.path.exists(ruta_carpeta)

def test_vaciar_carpeta_vacia():

    ruta_carpeta=os.path.join(os.getcwd(), "testutilidades", "Prueba")

    crearCarpeta(ruta_carpeta)

    assert not os.listdir(ruta_carpeta)

    vaciarCarpeta(ruta_carpeta)

    assert not os.listdir(ruta_carpeta)

def crearHTML(ruta:str)->None:

    contenido="""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Mi Archivo HTML</title>
            </head>
            <body>
                <h1>Hola, este es mi archivo HTML creado con Python</h1>
            </body>
            </html>
            """

    with open(ruta, "w") as html:

        html.write(contenido)

def test_vaciar_carpeta_llena():

    ruta_carpeta=os.path.join(os.getcwd(), "testutilidades", "Prueba")

    assert not os.listdir(ruta_carpeta)

    ruta_html=os.path.join(ruta_carpeta, "html.html")

    crearHTML(ruta_html)

    assert os.listdir(ruta_carpeta)

    vaciarCarpeta(ruta_carpeta)

    assert not os.listdir(ruta_carpeta)

    borrarCarpeta(ruta_carpeta)

@pytest.mark.parametrize(["numero_archivos"],
    [(1,),(3,),(7,),(4,),(13,)]
)
def test_vaciar_carpeta_llena_varios(numero_archivos):

    ruta_carpeta=os.path.join(os.getcwd(), "testutilidades", "Prueba")

    crearCarpeta(ruta_carpeta)

    assert not os.listdir(ruta_carpeta)

    for numero in range(numero_archivos):

        ruta_html=os.path.join(ruta_carpeta, f"html{numero}.html")

        crearHTML(ruta_html)

    assert len(os.listdir(ruta_carpeta))==numero_archivos

    vaciarCarpeta(ruta_carpeta)

    assert not os.listdir(ruta_carpeta)

    borrarCarpeta(ruta_carpeta)

@pytest.mark.parametrize(["archivo", "extension"],
    [
        ("mipdf.pdf", "pdf"),
        ("miimagen.jpeg", "jpeg"),
        ("imagen", "jpg"),
        ("mitxt.txt", "txt"),
    ]
)
def test_extraer_extension(archivo, extension):

    assert extraerExtension(archivo)==extension

def test_crear_carpeta_data_lake_perfil_no_existe(datalake, contenedor_dl):

    datalake.eliminarCarpeta(contenedor_dl, "perfil")

    assert not datalake.existe_carpeta(contenedor_dl, "perfil")

    crearCarpetaDataLakePerfil(contenedor_dl)

    assert datalake.existe_carpeta(contenedor_dl, "perfil")

    datalake.cerrarConexion()

def test_crear_carpeta_data_lake_perfil_existe(datalake, contenedor_dl):

    assert datalake.existe_carpeta(contenedor_dl, "perfil")

    crearCarpetaDataLakePerfil(contenedor_dl)

    assert datalake.existe_carpeta(contenedor_dl, "perfil")

    datalake.cerrarConexion()

def test_crear_carpeta_data_lake_perfil_usuario_no_existe(datalake, contenedor_dl):

    datalake.eliminarCarpeta(contenedor_dl, "perfil")

    crearCarpetaDataLakePerfil(contenedor_dl)

    assert datalake.existe_carpeta(contenedor_dl, "perfil")
    assert not datalake.existe_carpeta(contenedor_dl, "perfil/nacho")

    crearCarpetaDataLakePerfilUsuario("nacho", contenedor_dl)

    assert datalake.existe_carpeta(contenedor_dl, "perfil/nacho")

    datalake.cerrarConexion()

def test_crear_carpeta_data_lake_perfil_usuario_existe(datalake, contenedor_dl):

    assert datalake.existe_carpeta(contenedor_dl, "perfil")
    assert datalake.existe_carpeta(contenedor_dl, "perfil/nacho")

    crearCarpetaDataLakePerfilUsuario("nacho", contenedor_dl)

    assert datalake.existe_carpeta(contenedor_dl, "perfil/nacho")

    datalake.cerrarConexion()

def test_listar_imagenes_carpeta_datalake_carpeta_no_existe(datalake, contenedor_dl):

    assert not datalake.existe_carpeta(contenedor_dl, "perfil/no_existo")

    assert not listarImagenesCarpetaDatalake("no_existo", contenedor_dl)

    datalake.cerrarConexion()

def test_listar_imagenes_carpeta_datalake_imagenes_no_existen(datalake, contenedor_dl):

    assert datalake.existe_carpeta(contenedor_dl, "perfil/nacho")

    assert not listarImagenesCarpetaDatalake("nacho", contenedor_dl)

    datalake.cerrarConexion()

def crearArchivoTXT(ruta:str, nombre:str)->None:

    ruta_archivo=os.path.join(ruta, nombre)

    with open(ruta_archivo, "w") as file:

        file.write("Nacho")

def test_listar_imagenes_carpeta_datalake(datalake, contenedor_dl):

    ruta_carpeta=os.path.join(os.getcwd(), "Archivos_Tests_Data_Lake")

    nombre_archivo="archivo.txt"

    crearCarpeta(ruta_carpeta)

    vaciarCarpeta(ruta_carpeta)

    crearArchivoTXT(ruta_carpeta, nombre_archivo)

    assert datalake.existe_carpeta(contenedor_dl, "perfil/nacho")

    datalake.subirArchivo(contenedor_dl, "perfil/nacho", ruta_carpeta, nombre_archivo)

    archivos=listarImagenesCarpetaDatalake("nacho", contenedor_dl)

    assert nombre_archivo in archivos

    vaciarCarpeta(ruta_carpeta)

    borrarCarpeta(ruta_carpeta)

    datalake.cerrarConexion()

def test_existe_imagen_datalake_carpeta_no_existe(datalake, contenedor_dl):

    assert not datalake.existe_carpeta(contenedor_dl, "perfil/no_existo")

    assert not existe_imagen_datalake("no_existo", "archivo.txt", contenedor_dl)

    datalake.cerrarConexion()

def test_existe_imagen_datalake_imagen_no_existe(datalake, contenedor_dl):

    assert datalake.existe_carpeta(contenedor_dl, "perfil/nacho")

    assert not existe_imagen_datalake("nacho", "nacho.txt", contenedor_dl)

    datalake.cerrarConexion()

def test_existe_imagen_datalake(datalake, contenedor_dl):

    assert datalake.existe_carpeta(contenedor_dl, "perfil/nacho")

    assert existe_imagen_datalake("nacho", "archivo.txt", contenedor_dl)

    datalake.cerrarConexion()

def test_eliminar_imagen_datalake_carpeta_no_existe(datalake, contenedor_dl):

    assert not datalake.existe_carpeta(contenedor_dl, "perfil/no_existo")

    assert not eliminarImagenDatalake("no_existo", "archivo.txt", contenedor_dl)

    datalake.cerrarConexion()

def test_eliminar_imagen_datalake_imagen_no_existe(datalake, contenedor_dl):

    assert datalake.existe_carpeta(contenedor_dl, "perfil/nacho")

    assert not existe_imagen_datalake("nacho", "nacho.txt", contenedor_dl)

    assert not eliminarImagenDatalake("nacho", "nacho.txt", contenedor_dl)

    datalake.cerrarConexion()

def test_existe_imagen_datalake(datalake, contenedor_dl):

    assert datalake.existe_carpeta(contenedor_dl, "perfil/nacho")

    assert existe_imagen_datalake("nacho", "archivo.txt", contenedor_dl)

    assert eliminarImagenDatalake("nacho", "archivo.txt", contenedor_dl)

    assert not existe_imagen_datalake("nacho", "archivo.txt", contenedor_dl)

    datalake.cerrarConexion()

def test_subir_imagen_perfil_usuario_datalake_no_existe_carpeta(datalake, contenedor_dl):

    ruta_carpeta=os.path.join(os.getcwd(), "Archivos_Tests_Data_Lake")

    datalake.eliminarCarpeta(contenedor_dl, "perfil")

    crearCarpetaDataLakePerfil(contenedor_dl)

    assert datalake.existe_carpeta(contenedor_dl, "perfil")

    assert not datalake.existe_carpeta(contenedor_dl, "perfil/nacho")

    assert not existe_imagen_datalake("nacho", "archivo.txt", contenedor_dl)

    subirImagenPerfilUsuarioDataLake("nacho", "archivo.txt", ruta_carpeta, contenedor_dl)

    assert not existe_imagen_datalake("nacho", "archivo.txt", contenedor_dl)

    datalake.cerrarConexion()

def test_subir_imagen_perfil_usuario_datalake_no_existe_archivo(datalake, contenedor_dl):

    ruta_carpeta=os.path.join(os.getcwd(), "Archivos_Tests_Data_Lake")

    crearCarpeta(ruta_carpeta)

    datalake.eliminarCarpeta(contenedor_dl, "perfil")

    crearCarpetaDataLakePerfil(contenedor_dl)

    crearCarpetaDataLakePerfilUsuario("nacho", contenedor_dl)

    assert datalake.existe_carpeta(contenedor_dl, "perfil")
    
    assert datalake.existe_carpeta(contenedor_dl, "perfil/nacho")

    assert not existe_imagen_datalake("nacho", "archivo.txt", contenedor_dl)

    subirImagenPerfilUsuarioDataLake("nacho", "archivo.txt", ruta_carpeta, contenedor_dl)

    assert not existe_imagen_datalake("nacho", "archivo.txt", contenedor_dl)

    datalake.cerrarConexion()

def test_subir_imagen_perfil_usuario_datalake(datalake, contenedor_dl):

    ruta_carpeta=os.path.join(os.getcwd(), "Archivos_Tests_Data_Lake")

    nombre_archivo="archivo.txt"

    vaciarCarpeta(ruta_carpeta)

    crearArchivoTXT(ruta_carpeta, nombre_archivo)

    datalake.eliminarCarpeta(contenedor_dl, "perfil")

    crearCarpetaDataLakePerfil(contenedor_dl)

    crearCarpetaDataLakePerfilUsuario("nacho", contenedor_dl)

    assert datalake.existe_carpeta(contenedor_dl, "perfil")

    assert datalake.existe_carpeta(contenedor_dl, "perfil/nacho")

    assert not existe_imagen_datalake("nacho", nombre_archivo, contenedor_dl)

    subirImagenPerfilUsuarioDataLake("nacho", nombre_archivo, ruta_carpeta, contenedor_dl)

    assert existe_imagen_datalake("nacho", nombre_archivo, contenedor_dl)

    vaciarCarpeta(ruta_carpeta)

    borrarCarpeta(ruta_carpeta)

    datalake.cerrarConexion()

@pytest.mark.parametrize(["real", "posicon_porra", "puntos"],
    [   
        ({'seleccion-republica-corea': 1, 'seleccion-mexico': 2, 'republica-checa': 3, 'seleccion-sudafrica': 4}, 1, 3),
        ({'seleccion-republica-corea': 1, 'seleccion-mexico': 2, 'republica-checa': 3, 'seleccion-sudafrica': 4}, 2, 2),
        ({'seleccion-republica-corea': 1, 'seleccion-mexico': 2, 'republica-checa': 3, 'seleccion-sudafrica': 4}, 3, 1),
        ({'seleccion-republica-corea': 1, 'seleccion-mexico': 2, 'republica-checa': 3, 'seleccion-sudafrica': 4}, 4, 0),
        ({'seleccion-mexico': 1, 'seleccion-republica-corea': 2, 'republica-checa': 3, 'seleccion-sudafrica': 4}, 4, 1),
        ({'seleccion-mexico': 1, 'seleccion-republica-corea': 2, 'republica-checa': 3, 'seleccion-sudafrica': 4}, 3, 2),
        ({'seleccion-mexico': 1, 'seleccion-republica-corea': 2, 'republica-checa': 3, 'seleccion-sudafrica': 4}, 2, 3),
        ({'seleccion-mexico': 1, 'seleccion-republica-corea': 2, 'republica-checa': 3, 'seleccion-sudafrica': 4}, 1, 2)
    ]
)
def test_calcular_puntos(real, posicon_porra, puntos):

    fila={"equipo_porra_id": "seleccion-republica-corea", "posicion": posicon_porra}

    assert calcularPuntos(fila, real)==puntos

@pytest.mark.parametrize(["real", "posicon_porra", "motivo"],
    [   
        ({'seleccion-republica-corea': 1, 'seleccion-mexico': 2, 'republica-checa': 3, 'seleccion-sudafrica': 4}, 1, "Posición exacta"),
        ({'seleccion-republica-corea': 1, 'seleccion-mexico': 2, 'republica-checa': 3, 'seleccion-sudafrica': 4}, 2, "Diferencia de 1 posición"),
        ({'seleccion-republica-corea': 1, 'seleccion-mexico': 2, 'republica-checa': 3, 'seleccion-sudafrica': 4}, 3, "Diferencia de 2 posiciones"),
        ({'seleccion-republica-corea': 1, 'seleccion-mexico': 2, 'republica-checa': 3, 'seleccion-sudafrica': 4}, 4, "Diferencia de 3 posiciones"),
        ({'seleccion-mexico': 1, 'seleccion-republica-corea': 2, 'republica-checa': 3, 'seleccion-sudafrica': 4}, 4, "Diferencia de 2 posiciones"),
        ({'seleccion-mexico': 1, 'seleccion-republica-corea': 2, 'republica-checa': 3, 'seleccion-sudafrica': 4}, 3, "Diferencia de 1 posición"),
        ({'seleccion-mexico': 1, 'seleccion-republica-corea': 2, 'republica-checa': 3, 'seleccion-sudafrica': 4}, 2, "Posición exacta"),
        ({'seleccion-mexico': 1, 'seleccion-republica-corea': 2, 'republica-checa': 3, 'seleccion-sudafrica': 4}, 1, "Diferencia de 1 posición")
    ]
)
def test_calcular_motivo(real, posicon_porra, motivo):

    fila={"equipo_porra_id": "seleccion-republica-corea", "posicion": posicon_porra}

    assert calcularMotivo(fila, real)==motivo

def test_comparar_grupo_dataframe_detalle_grupo_real_sin_datos():

    grupos_real=[]

    grupos_porra=[('A', 'seleccion-mexico', 'México', 3811, 'MEX', 1),
                ('A', 'republica-checa', 'República Checa', 6188, 'CZE', 2),
                ('A', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 3),
                ('A', 'seleccion-sudafrica', 'Sudáfrica', 3815, 'ZAF', 4)]

    df=compararGrupoDataFrameDetalle(grupos_real, grupos_porra)

    assert df.empty

def test_comparar_grupo_dataframe_detalle_grupo_porra_sin_datos():

    grupos_real=[('A', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 1),
                ('A', 'seleccion-mexico', 'México', 3811, 'MEX', 2),
                ('A', 'republica-checa', 'República Checa', 6188, 'CZE', 3),
                ('A', 'seleccion-sudafrica', 'Sudáfrica', 3815, 'ZAF', 4)]

    grupos_porra=[]

    df=compararGrupoDataFrameDetalle(grupos_real, grupos_porra)

    assert not df.empty
    assert len(df)==4
    assert df["equipo_porra_id"].isnull().all()
    assert df["equipo_porra_nombre"].isnull().all()
    assert (df["puntos"]==0).all()
    assert (df["motivo"]=="Usuario sin porra para este grupo").all()

def test_comparar_grupo_dataframe_detalle_grupos_porra_menos_4_registros():

    grupos_real=[('A', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 1),
                ('A', 'seleccion-mexico', 'México', 3811, 'MEX', 2),
                ('A', 'republica-checa', 'República Checa', 6188, 'CZE', 3),
                ('A', 'seleccion-sudafrica', 'Sudáfrica', 3815, 'ZAF', 4)]

    grupos_porra=[('A', 'seleccion-mexico', 'México', 3811, 'MEX', 1),
                ('A', 'republica-checa', 'República Checa', 6188, 'CZE', 2),
                ('A', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 3)]

    with pytest.raises(Exception):

        compararGrupoDataFrameDetalle(grupos_real, grupos_porra)

def test_comparar_grupo_dataframe_detalle_grupos_real_menos_4_registros():

    grupos_real=[('A', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 1),
                ('A', 'republica-checa', 'República Checa', 6188, 'CZE', 3),
                ('A', 'seleccion-sudafrica', 'Sudáfrica', 3815, 'ZAF', 4)]

    grupos_porra=[('A', 'seleccion-mexico', 'México', 3811, 'MEX', 1),
                ('A', 'republica-checa', 'República Checa', 6188, 'CZE', 2),
                ('A', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 3),
                ('A', 'seleccion-sudafrica', 'Sudáfrica', 3815, 'ZAF', 4)]

    with pytest.raises(Exception):

        compararGrupoDataFrameDetalle(grupos_real, grupos_porra)

def test_comparar_grupo_dataframe_detalle_merge_erroneo():

    grupos_real=[('A', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 1),
                ('A', 'seleccion-mexico', 'México', 3811, 'MEX', 2),
                ('A', 'republica-checa', 'República Checa', 6188, 'CZE', 3),
                ('A', 'seleccion-sudafrica', 'Sudáfrica', 3815, 'ZAF', 4)]

    grupos_porra=[('A', 'seleccion-mexico', 'México', 3811, 'MEX', 1),
                ('A', 'republica-checa', 'República Checa', 6188, 'CZE', 1),
                ('A', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 1),
                ('A', 'seleccion-sudafrica', 'Sudáfrica', 3815, 'ZAF', 4)]

    with pytest.raises(Exception):

        compararGrupoDataFrameDetalle(grupos_real, grupos_porra)

@pytest.mark.parametrize(["grupos_porra", "puntos_totales"],
    [   
        ([('A', 'seleccion-mexico', 'México', 3811, 'MEX', 1),
            ('A', 'republica-checa', 'República Checa', 6188, 'CZE', 2),
            ('A', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 3),
            ('A', 'seleccion-sudafrica', 'Sudáfrica', 3815, 'ZAF', 4)], 8),
        ([('A', 'seleccion-sudafrica', 'Sudáfrica', 3815, 'ZAF', 1),
            ('A', 'seleccion-mexico', 'México', 3811, 'MEX', 2),
            ('A', 'republica-checa', 'República Checa', 6188, 'CZE', 3),
            ('A', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 4)], 6),
        ([('A', 'seleccion-sudafrica', 'Sudáfrica', 3815, 'ZAF', 1),
            ('A', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 2),
            ('A', 'seleccion-mexico', 'México', 3811, 'MEX', 3),
            ('A', 'republica-checa', 'República Checa', 6188, 'CZE', 4)], 6)
    ]
)
def test_comparar_grupo_dataframe_detalle(grupos_porra, puntos_totales):

    grupos_real=[('A', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 1),
                ('A', 'seleccion-mexico', 'México', 3811, 'MEX', 2),
                ('A', 'republica-checa', 'República Checa', 6188, 'CZE', 3),
                ('A', 'seleccion-sudafrica', 'Sudáfrica', 3815, 'ZAF', 4)]

    df=compararGrupoDataFrameDetalle(grupos_real, grupos_porra)

    assert not df.empty
    assert len(df)==4
    assert df["puntos"].sum()==puntos_totales

def test_comparar_grupos_disponibles_dataframe_detalle_sin_grupo_real_sin_grupo_porra():

    grupos_real=[]

    grupos_porra=[]

    df=compararGruposDisponiblesDataFrameDetalle(grupos_real, grupos_porra)

    assert df.empty

def test_comparar_grupos_disponibles_dataframe_detalle_sin_grupo_real():

    grupos_real=[]

    grupos_porra=[('A', 'seleccion-mexico', 'México', 3811, 'MEX', 1),
                ('A', 'republica-checa', 'República Checa', 6188, 'CZE', 2),
                ('A', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 3),
                ('A', 'seleccion-sudafrica', 'Sudáfrica', 3815, 'ZAF', 4)]

    df=compararGruposDisponiblesDataFrameDetalle(grupos_real, grupos_porra)

    assert df.empty

def test_comparar_grupos_disponibles_dataframe_detalle_un_grupo_real_un_grupo_porra():

    grupos_real=[('A', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 1),
                ('A', 'seleccion-mexico', 'México', 3811, 'MEX', 2),
                ('A', 'republica-checa', 'República Checa', 6188, 'CZE', 3),
                ('A', 'seleccion-sudafrica', 'Sudáfrica', 3815, 'ZAF', 4)]

    grupos_porra=[('A', 'seleccion-mexico', 'México', 3811, 'MEX', 1),
                ('A', 'republica-checa', 'República Checa', 6188, 'CZE', 2),
                ('A', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 3),
                ('A', 'seleccion-sudafrica', 'Sudáfrica', 3815, 'ZAF', 4)]

    df=compararGruposDisponiblesDataFrameDetalle(grupos_real, grupos_porra)

    assert not df.empty
    assert len(df)==4
    assert df["grupo"].unique().tolist()==["A"]

def test_comparar_grupos_disponibles_dataframe_detalle_un_grupo_real_dos_grupos_porra():

    grupos_real=[('A', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 1),
                ('A', 'seleccion-mexico', 'México', 3811, 'MEX', 2),
                ('A', 'republica-checa', 'República Checa', 6188, 'CZE', 3),
                ('A', 'seleccion-sudafrica', 'Sudáfrica', 3815, 'ZAF', 4)]

    grupos_porra=[('A', 'seleccion-mexico', 'México', 3811, 'MEX', 1),
                ('A', 'republica-checa', 'República Checa', 6188, 'CZE', 2),
                ('A', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 3),
                ('A', 'seleccion-sudafrica', 'Sudáfrica', 3815, 'ZAF', 4),
                ('B', 'seleccion-suiza', 'Suiza', 3723, 'CHE', 1),
                ('B', 'canada', 'Canadá', 5577, 'CAN', 2),
                ('B', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 3),
                ('B', 'seleccion-qatar', 'Catar', 3799, 'QAT', 4)]

    df=compararGruposDisponiblesDataFrameDetalle(grupos_real, grupos_porra)

    assert not df.empty
    assert len(df)==4
    assert df["grupo"].unique().tolist()==["A"]

def test_comparar_grupos_disponibles_dataframe_detalle_dos_grupos_real_dos_grupos_porra():

    grupos_real=[('A', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 1),
                ('A', 'seleccion-mexico', 'México', 3811, 'MEX', 2),
                ('A', 'republica-checa', 'República Checa', 6188, 'CZE', 3),
                ('A', 'seleccion-sudafrica', 'Sudáfrica', 3815, 'ZAF', 4),
                ('B', 'canada', 'Canadá', 5577, 'CAN', 1),
                ('B', 'seleccion-suiza', 'Suiza', 3723, 'CHE', 2),
                ('B', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 3),
                ('B', 'seleccion-qatar', 'Catar', 3799, 'QAT', 4)]

    grupos_porra=[('A', 'seleccion-mexico', 'México', 3811, 'MEX', 1),
                ('A', 'republica-checa', 'República Checa', 6188, 'CZE', 2),
                ('A', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 3),
                ('A', 'seleccion-sudafrica', 'Sudáfrica', 3815, 'ZAF', 4),
                ('B', 'seleccion-suiza', 'Suiza', 3723, 'CHE', 1),
                ('B', 'canada', 'Canadá', 5577, 'CAN', 2),
                ('B', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 3),
                ('B', 'seleccion-qatar', 'Catar', 3799, 'QAT', 4)]

    df=compararGruposDisponiblesDataFrameDetalle(grupos_real, grupos_porra)

    assert not df.empty
    assert len(df)==8
    assert sorted(df["grupo"].unique().tolist())==["A", "B"]

def test_comparar_grupos_disponibles_dataframe_detalle_dos_grupos_real_tres_grupos_porra():

    grupos_real=[('A', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 1),
                ('A', 'seleccion-mexico', 'México', 3811, 'MEX', 2),
                ('A', 'republica-checa', 'República Checa', 6188, 'CZE', 3),
                ('A', 'seleccion-sudafrica', 'Sudáfrica', 3815, 'ZAF', 4),
                ('B', 'canada', 'Canadá', 5577, 'CAN', 1),
                ('B', 'seleccion-suiza', 'Suiza', 3723, 'CHE', 2),
                ('B', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 3),
                ('B', 'seleccion-qatar', 'Catar', 3799, 'QAT', 4)]

    grupos_porra=[('A', 'seleccion-mexico', 'México', 3811, 'MEX', 1),
                ('A', 'republica-checa', 'República Checa', 6188, 'CZE', 2),
                ('A', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 3),
                ('A', 'seleccion-sudafrica', 'Sudáfrica', 3815, 'ZAF', 4),
                ('B', 'seleccion-suiza', 'Suiza', 3723, 'CHE', 1),
                ('B', 'canada', 'Canadá', 5577, 'CAN', 2),
                ('B', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 3),
                ('B', 'seleccion-qatar', 'Catar', 3799, 'QAT', 4),
                ('C', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 1),
                ('C', 'seleccion-marruecos', 'Marruecos', 3780, 'MAR', 2),
                ('C', 'seleccion-escocia', 'Escocia', 3758, 'SCO', 3),
                ('C', 'haiti', 'Haití', 5582, 'HTI', 4)]

    df=compararGruposDisponiblesDataFrameDetalle(grupos_real, grupos_porra)

    assert not df.empty
    assert len(df)==8
    assert sorted(df["grupo"].unique().tolist())==["A", "B"]

def test_comparar_grupos_disponibles_dataframe_detalle_tres_grupos_real_tres_grupos_porra():

    grupos_real=[('A', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 1),
                ('A', 'seleccion-mexico', 'México', 3811, 'MEX', 2),
                ('A', 'republica-checa', 'República Checa', 6188, 'CZE', 3),
                ('A', 'seleccion-sudafrica', 'Sudáfrica', 3815, 'ZAF', 4),
                ('B', 'canada', 'Canadá', 5577, 'CAN', 1),
                ('B', 'seleccion-suiza', 'Suiza', 3723, 'CHE', 2),
                ('B', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 3),
                ('B', 'seleccion-qatar', 'Catar', 3799, 'QAT', 4),
                ('C', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 1),
                ('C', 'seleccion-marruecos', 'Marruecos', 3780, 'MAR', 2),
                ('C', 'seleccion-escocia', 'Escocia', 3758, 'SCO', 3),
                ('C', 'haiti', 'Haití', 5582, 'HTI', 4)]

    grupos_porra=[('A', 'seleccion-mexico', 'México', 3811, 'MEX', 1),
                ('A', 'republica-checa', 'República Checa', 6188, 'CZE', 2),
                ('A', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 3),
                ('A', 'seleccion-sudafrica', 'Sudáfrica', 3815, 'ZAF', 4),
                ('B', 'seleccion-suiza', 'Suiza', 3723, 'CHE', 1),
                ('B', 'canada', 'Canadá', 5577, 'CAN', 2),
                ('B', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 3),
                ('B', 'seleccion-qatar', 'Catar', 3799, 'QAT', 4),
                ('C', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 1),
                ('C', 'seleccion-marruecos', 'Marruecos', 3780, 'MAR', 2),
                ('C', 'seleccion-escocia', 'Escocia', 3758, 'SCO', 3),
                ('C', 'haiti', 'Haití', 5582, 'HTI', 4)]

    df=compararGruposDisponiblesDataFrameDetalle(grupos_real, grupos_porra)

    assert not df.empty
    assert len(df)==12
    assert sorted(df["grupo"].unique().tolist())==["A", "B", "C"]

def test_comparar_grupos_disponibles_dataframe_detalle_todos():

    grupos_real=[('A', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 1),
                ('A', 'seleccion-mexico', 'México', 3811, 'MEX', 2),
                ('A', 'republica-checa', 'República Checa', 6188, 'CZE', 3),
                ('A', 'seleccion-sudafrica', 'Sudáfrica', 3815, 'ZAF', 4),
                ('B', 'canada', 'Canadá', 5577, 'CAN', 1),
                ('B', 'seleccion-suiza', 'Suiza', 3723, 'CHE', 2),
                ('B', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 3),
                ('B', 'seleccion-qatar', 'Catar', 3799, 'QAT', 4),
                ('C', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 1),
                ('C', 'seleccion-marruecos', 'Marruecos', 3780, 'MAR', 2),
                ('C', 'seleccion-escocia', 'Escocia', 3758, 'SCO', 3),
                ('C', 'haiti', 'Haití', 5582, 'HTI', 4),
                ('D', 'seleccion-turquia', 'Turquía', 3737, 'TUR', 1),
                ('D', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 2),
                ('D', 'seleccion-australia', 'Australia', 3801, 'AUS', 3),
                ('D', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 4),
                ('E', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 1),
                ('E', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV', 2),
                ('E', 'seleccion-ecuador', 'Ecuador', 3771, 'ECU', 3),
                ('E', 'curazao', 'Curazao', 61757, 'CUR', 4),
                ('F', 'seleccion-japon', 'Japón', 3798, 'JPN', 1),
                ('F', 'seleccion-suecia', 'Suecia', 3074, 'SWE', 2),
                ('F', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 3),
                ('F', 'seleccion-tunez', 'Túnez', 3783, 'TUN', 4),
                ('G', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 1),
                ('G', 'seleccion-egipto', 'Egipto', 3788, 'EGY', 2),
                ('G', 'seleccion-nueva-zelanda', 'Nueva Zelanda', 3808, 'NZL', 3),
                ('G', 'seleccion-iran', 'Irán', 3806, 'IRN', 4),
                ('H', 'seleccion-espanola', 'España', 3850, 'ESP', 1),
                ('H', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 2),
                ('H', 'cabo-verde', 'Cabo Verde', 9158, 'CPV', 3),
                ('H', 'seleccion-uruguay', 'Uruguay', 3768, 'URY', 4),
                ('I', 'seleccion-francia', 'Francia', 3750, 'FRA', 1),
                ('I', 'senegal', 'Senegal', 5658, 'SEN', 2),
                ('I', 'seleccion-noruega', 'Noruega', 3759, 'NOR', 3),
                ('I', 'seleccion-iraq', 'Iraq', 3816, 'IRQ', 4),
                ('J', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 1),
                ('J', 'seleccion-austria', 'Austria', 3767, 'AUT', 2),
                ('J', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 3),
                ('J', 'jordania', 'Jordania', 5480, 'JOR', 4),
                ('K', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 1),
                ('K', 'seleccion-colombia', 'Colombia', 3774, 'COL', 2),
                ('K', 'seleccion-uzbekistan', 'Uzbekistán', 3800, 'UZB', 3),
                ('K', 'rd-congo', 'RD Congo', 11591, 'COD', 4),
                ('L', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG', 1),
                ('L', 'seleccion-ghana', 'Ghana', 3791, 'GHA', 2),
                ('L', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 3),
                ('L', 'panama-seleccion', 'Panamá', 17581, 'PAN', 4)]

    grupos_porra=[('A', 'seleccion-mexico', 'México', 3811, 'MEX', 1),
                ('A', 'republica-checa', 'República Checa', 6188, 'CZE', 2),
                ('A', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 3),
                ('A', 'seleccion-sudafrica', 'Sudáfrica', 3815, 'ZAF', 4),
                ('B', 'seleccion-suiza', 'Suiza', 3723, 'CHE', 1),
                ('B', 'canada', 'Canadá', 5577, 'CAN', 2),
                ('B', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 3),
                ('B', 'seleccion-qatar', 'Catar', 3799, 'QAT', 4),
                ('C', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 1),
                ('C', 'seleccion-marruecos', 'Marruecos', 3780, 'MAR', 2),
                ('C', 'seleccion-escocia', 'Escocia', 3758, 'SCO', 3),
                ('C', 'haiti', 'Haití', 5582, 'HTI', 4),
                ('D', 'seleccion-turquia', 'Turquía', 3737, 'TUR', 1),
                ('D', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 2),
                ('D', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 3),
                ('D', 'seleccion-australia', 'Australia', 3801, 'AUS', 4),
                ('E', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 1),
                ('E', 'seleccion-ecuador', 'Ecuador', 3771, 'ECU', 2),
                ('E', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV', 3),
                ('E', 'curazao', 'Curazao', 61757, 'CUR', 4),
                ('F', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 1),
                ('F', 'seleccion-japon', 'Japón', 3798, 'JPN', 2),
                ('F', 'seleccion-suecia', 'Suecia', 3074, 'SWE', 3),
                ('F', 'seleccion-tunez', 'Túnez', 3783, 'TUN', 4),
                ('G', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 1),
                ('G', 'seleccion-egipto', 'Egipto', 3788, 'EGY', 2),
                ('G', 'seleccion-iran', 'Irán', 3806, 'IRN', 3),
                ('G', 'seleccion-nueva-zelanda', 'Nueva Zelanda', 3808, 'NZL', 4),
                ('H', 'seleccion-espanola', 'España', 3850, 'ESP', 1),
                ('H', 'seleccion-uruguay', 'Uruguay', 3768, 'URY', 2),
                ('H', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 3),
                ('H', 'cabo-verde', 'Cabo Verde', 9158, 'CPV', 4),
                ('I', 'seleccion-francia', 'Francia', 3750, 'FRA', 1),
                ('I', 'seleccion-noruega', 'Noruega', 3759, 'NOR', 2),
                ('I', 'senegal', 'Senegal', 5658, 'SEN', 3),
                ('I', 'seleccion-iraq', 'Iraq', 3816, 'IRQ', 4),
                ('J', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 1),
                ('J', 'seleccion-austria', 'Austria', 3767, 'AUT', 2),
                ('J', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 3),
                ('J', 'jordania', 'Jordania', 5480, 'JOR', 4),
                ('K', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 1),
                ('K', 'seleccion-colombia', 'Colombia', 3774, 'COL', 2),
                ('K', 'rd-congo', 'RD Congo', 11591, 'COD', 3),
                ('K', 'seleccion-uzbekistan', 'Uzbekistán', 3800, 'UZB', 4),
                ('L', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG', 1),
                ('L', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 2),
                ('L', 'seleccion-ghana', 'Ghana', 3791, 'GHA', 3),
                ('L', 'panama-seleccion', 'Panamá', 17581, 'PAN', 4)]

    df=compararGruposDisponiblesDataFrameDetalle(grupos_real, grupos_porra)

    assert not df.empty
    assert len(df)==48
    assert sorted(df["grupo"].unique().tolist())==["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]

def test_calcular_puntos_totales_grupos_sin_grupo_real_sin_grupo_porra():

    grupos_real=[]

    grupos_porra=[]

    assert calcularPuntosTotalesGrupos(grupos_real, grupos_porra)==0

def test_calcular_puntos_totales_grupos_sin_grupo_real():

    grupos_real=[]

    grupos_porra=[('A', 'seleccion-mexico', 'México', 3811, 'MEX', 1),
                ('A', 'republica-checa', 'República Checa', 6188, 'CZE', 2),
                ('A', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 3),
                ('A', 'seleccion-sudafrica', 'Sudáfrica', 3815, 'ZAF', 4)]

    assert calcularPuntosTotalesGrupos(grupos_real, grupos_porra)==0

def test_calcular_puntos_totales_grupos_un_grupo_real_un_grupo_porra():

    grupos_real=[('A', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 1),
                ('A', 'seleccion-mexico', 'México', 3811, 'MEX', 2),
                ('A', 'republica-checa', 'República Checa', 6188, 'CZE', 3),
                ('A', 'seleccion-sudafrica', 'Sudáfrica', 3815, 'ZAF', 4)]

    grupos_porra=[('A', 'seleccion-mexico', 'México', 3811, 'MEX', 1),
                ('A', 'republica-checa', 'República Checa', 6188, 'CZE', 2),
                ('A', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 3),
                ('A', 'seleccion-sudafrica', 'Sudáfrica', 3815, 'ZAF', 4)]

    assert calcularPuntosTotalesGrupos(grupos_real, grupos_porra)==8

def test_calcular_puntos_totales_grupos_un_grupo_real_dos_grupos_porra():

    grupos_real=[('A', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 1),
                ('A', 'seleccion-mexico', 'México', 3811, 'MEX', 2),
                ('A', 'republica-checa', 'República Checa', 6188, 'CZE', 3),
                ('A', 'seleccion-sudafrica', 'Sudáfrica', 3815, 'ZAF', 4)]

    grupos_porra=[('A', 'seleccion-mexico', 'México', 3811, 'MEX', 1),
                ('A', 'republica-checa', 'República Checa', 6188, 'CZE', 2),
                ('A', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 3),
                ('A', 'seleccion-sudafrica', 'Sudáfrica', 3815, 'ZAF', 4),
                ('B', 'seleccion-suiza', 'Suiza', 3723, 'CHE', 1),
                ('B', 'canada', 'Canadá', 5577, 'CAN', 2),
                ('B', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 3),
                ('B', 'seleccion-qatar', 'Catar', 3799, 'QAT', 4)]

    assert calcularPuntosTotalesGrupos(grupos_real, grupos_porra)==8

def test_calcular_puntos_totales_grupos_dos_grupos_real_dos_grupos_porra():

    grupos_real=[('A', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 1),
                ('A', 'seleccion-mexico', 'México', 3811, 'MEX', 2),
                ('A', 'republica-checa', 'República Checa', 6188, 'CZE', 3),
                ('A', 'seleccion-sudafrica', 'Sudáfrica', 3815, 'ZAF', 4),
                ('B', 'canada', 'Canadá', 5577, 'CAN', 1),
                ('B', 'seleccion-suiza', 'Suiza', 3723, 'CHE', 2),
                ('B', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 3),
                ('B', 'seleccion-qatar', 'Catar', 3799, 'QAT', 4)]

    grupos_porra=[('A', 'seleccion-mexico', 'México', 3811, 'MEX', 1),
                ('A', 'republica-checa', 'República Checa', 6188, 'CZE', 2),
                ('A', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 3),
                ('A', 'seleccion-sudafrica', 'Sudáfrica', 3815, 'ZAF', 4),
                ('B', 'seleccion-suiza', 'Suiza', 3723, 'CHE', 1),
                ('B', 'canada', 'Canadá', 5577, 'CAN', 2),
                ('B', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 3),
                ('B', 'seleccion-qatar', 'Catar', 3799, 'QAT', 4)]

    assert calcularPuntosTotalesGrupos(grupos_real, grupos_porra)==18

def test_calcular_puntos_totales_grupos_dos_grupos_real_tres_grupos_porra():

    grupos_real=[('A', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 1),
                ('A', 'seleccion-mexico', 'México', 3811, 'MEX', 2),
                ('A', 'republica-checa', 'República Checa', 6188, 'CZE', 3),
                ('A', 'seleccion-sudafrica', 'Sudáfrica', 3815, 'ZAF', 4),
                ('B', 'canada', 'Canadá', 5577, 'CAN', 1),
                ('B', 'seleccion-suiza', 'Suiza', 3723, 'CHE', 2),
                ('B', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 3),
                ('B', 'seleccion-qatar', 'Catar', 3799, 'QAT', 4)]

    grupos_porra=[('A', 'seleccion-mexico', 'México', 3811, 'MEX', 1),
                ('A', 'republica-checa', 'República Checa', 6188, 'CZE', 2),
                ('A', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 3),
                ('A', 'seleccion-sudafrica', 'Sudáfrica', 3815, 'ZAF', 4),
                ('B', 'seleccion-suiza', 'Suiza', 3723, 'CHE', 1),
                ('B', 'canada', 'Canadá', 5577, 'CAN', 2),
                ('B', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 3),
                ('B', 'seleccion-qatar', 'Catar', 3799, 'QAT', 4),
                ('C', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 1),
                ('C', 'seleccion-marruecos', 'Marruecos', 3780, 'MAR', 2),
                ('C', 'seleccion-escocia', 'Escocia', 3758, 'SCO', 3),
                ('C', 'haiti', 'Haití', 5582, 'HTI', 4)]

    assert calcularPuntosTotalesGrupos(grupos_real, grupos_porra)==18

def test_calcular_puntos_totales_grupos_tres_grupos_real_tres_grupos_porra():

    grupos_real=[('A', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 1),
                ('A', 'seleccion-mexico', 'México', 3811, 'MEX', 2),
                ('A', 'republica-checa', 'República Checa', 6188, 'CZE', 3),
                ('A', 'seleccion-sudafrica', 'Sudáfrica', 3815, 'ZAF', 4),
                ('B', 'canada', 'Canadá', 5577, 'CAN', 1),
                ('B', 'seleccion-suiza', 'Suiza', 3723, 'CHE', 2),
                ('B', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 3),
                ('B', 'seleccion-qatar', 'Catar', 3799, 'QAT', 4),
                ('C', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 1),
                ('C', 'seleccion-marruecos', 'Marruecos', 3780, 'MAR', 2),
                ('C', 'seleccion-escocia', 'Escocia', 3758, 'SCO', 3),
                ('C', 'haiti', 'Haití', 5582, 'HTI', 4)]

    grupos_porra=[('A', 'seleccion-mexico', 'México', 3811, 'MEX', 1),
                ('A', 'republica-checa', 'República Checa', 6188, 'CZE', 2),
                ('A', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 3),
                ('A', 'seleccion-sudafrica', 'Sudáfrica', 3815, 'ZAF', 4),
                ('B', 'seleccion-suiza', 'Suiza', 3723, 'CHE', 1),
                ('B', 'canada', 'Canadá', 5577, 'CAN', 2),
                ('B', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 3),
                ('B', 'seleccion-qatar', 'Catar', 3799, 'QAT', 4),
                ('C', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 1),
                ('C', 'seleccion-marruecos', 'Marruecos', 3780, 'MAR', 2),
                ('C', 'seleccion-escocia', 'Escocia', 3758, 'SCO', 3),
                ('C', 'haiti', 'Haití', 5582, 'HTI', 4)]

    assert calcularPuntosTotalesGrupos(grupos_real, grupos_porra)==30

def test_calcular_puntos_totales_grupos_todos():

    grupos_real=[('A', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 1),
                ('A', 'seleccion-mexico', 'México', 3811, 'MEX', 2),
                ('A', 'republica-checa', 'República Checa', 6188, 'CZE', 3),
                ('A', 'seleccion-sudafrica', 'Sudáfrica', 3815, 'ZAF', 4),
                ('B', 'canada', 'Canadá', 5577, 'CAN', 1),
                ('B', 'seleccion-suiza', 'Suiza', 3723, 'CHE', 2),
                ('B', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 3),
                ('B', 'seleccion-qatar', 'Catar', 3799, 'QAT', 4),
                ('C', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 1),
                ('C', 'seleccion-marruecos', 'Marruecos', 3780, 'MAR', 2),
                ('C', 'seleccion-escocia', 'Escocia', 3758, 'SCO', 3),
                ('C', 'haiti', 'Haití', 5582, 'HTI', 4),
                ('D', 'seleccion-turquia', 'Turquía', 3737, 'TUR', 1),
                ('D', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 2),
                ('D', 'seleccion-australia', 'Australia', 3801, 'AUS', 3),
                ('D', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 4),
                ('E', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 1),
                ('E', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV', 2),
                ('E', 'seleccion-ecuador', 'Ecuador', 3771, 'ECU', 3),
                ('E', 'curazao', 'Curazao', 61757, 'CUR', 4),
                ('F', 'seleccion-japon', 'Japón', 3798, 'JPN', 1),
                ('F', 'seleccion-suecia', 'Suecia', 3074, 'SWE', 2),
                ('F', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 3),
                ('F', 'seleccion-tunez', 'Túnez', 3783, 'TUN', 4),
                ('G', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 1),
                ('G', 'seleccion-egipto', 'Egipto', 3788, 'EGY', 2),
                ('G', 'seleccion-nueva-zelanda', 'Nueva Zelanda', 3808, 'NZL', 3),
                ('G', 'seleccion-iran', 'Irán', 3806, 'IRN', 4),
                ('H', 'seleccion-espanola', 'España', 3850, 'ESP', 1),
                ('H', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 2),
                ('H', 'cabo-verde', 'Cabo Verde', 9158, 'CPV', 3),
                ('H', 'seleccion-uruguay', 'Uruguay', 3768, 'URY', 4),
                ('I', 'seleccion-francia', 'Francia', 3750, 'FRA', 1),
                ('I', 'senegal', 'Senegal', 5658, 'SEN', 2),
                ('I', 'seleccion-noruega', 'Noruega', 3759, 'NOR', 3),
                ('I', 'seleccion-iraq', 'Iraq', 3816, 'IRQ', 4),
                ('J', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 1),
                ('J', 'seleccion-austria', 'Austria', 3767, 'AUT', 2),
                ('J', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 3),
                ('J', 'jordania', 'Jordania', 5480, 'JOR', 4),
                ('K', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 1),
                ('K', 'seleccion-colombia', 'Colombia', 3774, 'COL', 2),
                ('K', 'seleccion-uzbekistan', 'Uzbekistán', 3800, 'UZB', 3),
                ('K', 'rd-congo', 'RD Congo', 11591, 'COD', 4),
                ('L', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG', 1),
                ('L', 'seleccion-ghana', 'Ghana', 3791, 'GHA', 2),
                ('L', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 3),
                ('L', 'panama-seleccion', 'Panamá', 17581, 'PAN', 4)]

    grupos_porra=[('A', 'seleccion-mexico', 'México', 3811, 'MEX', 1),
                ('A', 'republica-checa', 'República Checa', 6188, 'CZE', 2),
                ('A', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 3),
                ('A', 'seleccion-sudafrica', 'Sudáfrica', 3815, 'ZAF', 4),
                ('B', 'seleccion-suiza', 'Suiza', 3723, 'CHE', 1),
                ('B', 'canada', 'Canadá', 5577, 'CAN', 2),
                ('B', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 3),
                ('B', 'seleccion-qatar', 'Catar', 3799, 'QAT', 4),
                ('C', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 1),
                ('C', 'seleccion-marruecos', 'Marruecos', 3780, 'MAR', 2),
                ('C', 'seleccion-escocia', 'Escocia', 3758, 'SCO', 3),
                ('C', 'haiti', 'Haití', 5582, 'HTI', 4),
                ('D', 'seleccion-turquia', 'Turquía', 3737, 'TUR', 1),
                ('D', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 2),
                ('D', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 3),
                ('D', 'seleccion-australia', 'Australia', 3801, 'AUS', 4),
                ('E', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 1),
                ('E', 'seleccion-ecuador', 'Ecuador', 3771, 'ECU', 2),
                ('E', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV', 3),
                ('E', 'curazao', 'Curazao', 61757, 'CUR', 4),
                ('F', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 1),
                ('F', 'seleccion-japon', 'Japón', 3798, 'JPN', 2),
                ('F', 'seleccion-suecia', 'Suecia', 3074, 'SWE', 3),
                ('F', 'seleccion-tunez', 'Túnez', 3783, 'TUN', 4),
                ('G', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 1),
                ('G', 'seleccion-egipto', 'Egipto', 3788, 'EGY', 2),
                ('G', 'seleccion-iran', 'Irán', 3806, 'IRN', 3),
                ('G', 'seleccion-nueva-zelanda', 'Nueva Zelanda', 3808, 'NZL', 4),
                ('H', 'seleccion-espanola', 'España', 3850, 'ESP', 1),
                ('H', 'seleccion-uruguay', 'Uruguay', 3768, 'URY', 2),
                ('H', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 3),
                ('H', 'cabo-verde', 'Cabo Verde', 9158, 'CPV', 4),
                ('I', 'seleccion-francia', 'Francia', 3750, 'FRA', 1),
                ('I', 'seleccion-noruega', 'Noruega', 3759, 'NOR', 2),
                ('I', 'senegal', 'Senegal', 5658, 'SEN', 3),
                ('I', 'seleccion-iraq', 'Iraq', 3816, 'IRQ', 4),
                ('J', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 1),
                ('J', 'seleccion-austria', 'Austria', 3767, 'AUT', 2),
                ('J', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 3),
                ('J', 'jordania', 'Jordania', 5480, 'JOR', 4),
                ('K', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 1),
                ('K', 'seleccion-colombia', 'Colombia', 3774, 'COL', 2),
                ('K', 'rd-congo', 'RD Congo', 11591, 'COD', 3),
                ('K', 'seleccion-uzbekistan', 'Uzbekistán', 3800, 'UZB', 4),
                ('L', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG', 1),
                ('L', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 2),
                ('L', 'seleccion-ghana', 'Ghana', 3791, 'GHA', 3),
                ('L', 'panama-seleccion', 'Panamá', 17581, 'PAN', 4)]

    assert calcularPuntosTotalesGrupos(grupos_real, grupos_porra)==118

def test_limpiar_dataframe_detalle_grupos_sin_grupo_real_sin_grupo_porra():

    grupos_real=[]

    grupos_porra=[]

    df=compararGruposDisponiblesDataFrameDetalle(grupos_real, grupos_porra)

    assert not limpiarDataFrameDetalleGrupos(df)

def test_limpiar_dataframe_detalle_grupos_sin_grupo_real():

    grupos_real=[]

    grupos_porra=[('A', 'seleccion-mexico', 'México', 3811, 'MEX', 1),
                ('A', 'republica-checa', 'República Checa', 6188, 'CZE', 2),
                ('A', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 3),
                ('A', 'seleccion-sudafrica', 'Sudáfrica', 3815, 'ZAF', 4)]

    df=compararGruposDisponiblesDataFrameDetalle(grupos_real, grupos_porra)

    assert not limpiarDataFrameDetalleGrupos(df)

def test_limpiar_dataframe_detalle_grupos_un_grupo_real_un_grupo_porra():

    grupos_real=[('A', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 1),
                ('A', 'seleccion-mexico', 'México', 3811, 'MEX', 2),
                ('A', 'republica-checa', 'República Checa', 6188, 'CZE', 3),
                ('A', 'seleccion-sudafrica', 'Sudáfrica', 3815, 'ZAF', 4)]

    grupos_porra=[('A', 'seleccion-mexico', 'México', 3811, 'MEX', 1),
                ('A', 'republica-checa', 'República Checa', 6188, 'CZE', 2),
                ('A', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 3),
                ('A', 'seleccion-sudafrica', 'Sudáfrica', 3815, 'ZAF', 4)]

    df=compararGruposDisponiblesDataFrameDetalle(grupos_real, grupos_porra)

    diccionario_detalle_grupos=limpiarDataFrameDetalleGrupos(df)

    assert sorted(list(diccionario_detalle_grupos.keys()))==["A"]

    for grupo in list(diccionario_detalle_grupos.keys()):

        assert len(diccionario_detalle_grupos[grupo]["filas"])==4

def test_limpiar_dataframe_detalle_grupos_un_grupo_real_dos_grupos_porra():

    grupos_real=[('A', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 1),
                ('A', 'seleccion-mexico', 'México', 3811, 'MEX', 2),
                ('A', 'republica-checa', 'República Checa', 6188, 'CZE', 3),
                ('A', 'seleccion-sudafrica', 'Sudáfrica', 3815, 'ZAF', 4)]

    grupos_porra=[('A', 'seleccion-mexico', 'México', 3811, 'MEX', 1),
                ('A', 'republica-checa', 'República Checa', 6188, 'CZE', 2),
                ('A', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 3),
                ('A', 'seleccion-sudafrica', 'Sudáfrica', 3815, 'ZAF', 4),
                ('B', 'seleccion-suiza', 'Suiza', 3723, 'CHE', 1),
                ('B', 'canada', 'Canadá', 5577, 'CAN', 2),
                ('B', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 3),
                ('B', 'seleccion-qatar', 'Catar', 3799, 'QAT', 4)]

    df=compararGruposDisponiblesDataFrameDetalle(grupos_real, grupos_porra)

    diccionario_detalle_grupos=limpiarDataFrameDetalleGrupos(df)

    assert sorted(list(diccionario_detalle_grupos.keys()))==["A"]

    for grupo in list(diccionario_detalle_grupos.keys()):

        assert len(diccionario_detalle_grupos[grupo]["filas"])==4

def test_limpiar_dataframe_detalle_grupos_dos_grupos_real_dos_grupos_porra():

    grupos_real=[('A', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 1),
                ('A', 'seleccion-mexico', 'México', 3811, 'MEX', 2),
                ('A', 'republica-checa', 'República Checa', 6188, 'CZE', 3),
                ('A', 'seleccion-sudafrica', 'Sudáfrica', 3815, 'ZAF', 4),
                ('B', 'canada', 'Canadá', 5577, 'CAN', 1),
                ('B', 'seleccion-suiza', 'Suiza', 3723, 'CHE', 2),
                ('B', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 3),
                ('B', 'seleccion-qatar', 'Catar', 3799, 'QAT', 4)]

    grupos_porra=[('A', 'seleccion-mexico', 'México', 3811, 'MEX', 1),
                ('A', 'republica-checa', 'República Checa', 6188, 'CZE', 2),
                ('A', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 3),
                ('A', 'seleccion-sudafrica', 'Sudáfrica', 3815, 'ZAF', 4),
                ('B', 'seleccion-suiza', 'Suiza', 3723, 'CHE', 1),
                ('B', 'canada', 'Canadá', 5577, 'CAN', 2),
                ('B', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 3),
                ('B', 'seleccion-qatar', 'Catar', 3799, 'QAT', 4)]

    df=compararGruposDisponiblesDataFrameDetalle(grupos_real, grupos_porra)

    diccionario_detalle_grupos=limpiarDataFrameDetalleGrupos(df)

    assert sorted(list(diccionario_detalle_grupos.keys()))==["A", "B"]

    for grupo in list(diccionario_detalle_grupos.keys()):

        assert len(diccionario_detalle_grupos[grupo]["filas"])==4

def test_limpiar_dataframe_detalle_grupos_dos_grupos_real_tres_grupos_porra():

    grupos_real=[('A', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 1),
                ('A', 'seleccion-mexico', 'México', 3811, 'MEX', 2),
                ('A', 'republica-checa', 'República Checa', 6188, 'CZE', 3),
                ('A', 'seleccion-sudafrica', 'Sudáfrica', 3815, 'ZAF', 4),
                ('B', 'canada', 'Canadá', 5577, 'CAN', 1),
                ('B', 'seleccion-suiza', 'Suiza', 3723, 'CHE', 2),
                ('B', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 3),
                ('B', 'seleccion-qatar', 'Catar', 3799, 'QAT', 4)]

    grupos_porra=[('A', 'seleccion-mexico', 'México', 3811, 'MEX', 1),
                ('A', 'republica-checa', 'República Checa', 6188, 'CZE', 2),
                ('A', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 3),
                ('A', 'seleccion-sudafrica', 'Sudáfrica', 3815, 'ZAF', 4),
                ('B', 'seleccion-suiza', 'Suiza', 3723, 'CHE', 1),
                ('B', 'canada', 'Canadá', 5577, 'CAN', 2),
                ('B', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 3),
                ('B', 'seleccion-qatar', 'Catar', 3799, 'QAT', 4),
                ('C', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 1),
                ('C', 'seleccion-marruecos', 'Marruecos', 3780, 'MAR', 2),
                ('C', 'seleccion-escocia', 'Escocia', 3758, 'SCO', 3),
                ('C', 'haiti', 'Haití', 5582, 'HTI', 4)]

    df=compararGruposDisponiblesDataFrameDetalle(grupos_real, grupos_porra)

    diccionario_detalle_grupos=limpiarDataFrameDetalleGrupos(df)

    assert sorted(list(diccionario_detalle_grupos.keys()))==["A", "B"]

    for grupo in list(diccionario_detalle_grupos.keys()):

        assert len(diccionario_detalle_grupos[grupo]["filas"])==4

def test_limpiar_dataframe_detalle_grupos_tres_grupos_real_tres_grupos_porra():

    grupos_real=[('A', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 1),
                ('A', 'seleccion-mexico', 'México', 3811, 'MEX', 2),
                ('A', 'republica-checa', 'República Checa', 6188, 'CZE', 3),
                ('A', 'seleccion-sudafrica', 'Sudáfrica', 3815, 'ZAF', 4),
                ('B', 'canada', 'Canadá', 5577, 'CAN', 1),
                ('B', 'seleccion-suiza', 'Suiza', 3723, 'CHE', 2),
                ('B', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 3),
                ('B', 'seleccion-qatar', 'Catar', 3799, 'QAT', 4),
                ('C', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 1),
                ('C', 'seleccion-marruecos', 'Marruecos', 3780, 'MAR', 2),
                ('C', 'seleccion-escocia', 'Escocia', 3758, 'SCO', 3),
                ('C', 'haiti', 'Haití', 5582, 'HTI', 4)]

    grupos_porra=[('A', 'seleccion-mexico', 'México', 3811, 'MEX', 1),
                ('A', 'republica-checa', 'República Checa', 6188, 'CZE', 2),
                ('A', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 3),
                ('A', 'seleccion-sudafrica', 'Sudáfrica', 3815, 'ZAF', 4),
                ('B', 'seleccion-suiza', 'Suiza', 3723, 'CHE', 1),
                ('B', 'canada', 'Canadá', 5577, 'CAN', 2),
                ('B', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 3),
                ('B', 'seleccion-qatar', 'Catar', 3799, 'QAT', 4),
                ('C', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 1),
                ('C', 'seleccion-marruecos', 'Marruecos', 3780, 'MAR', 2),
                ('C', 'seleccion-escocia', 'Escocia', 3758, 'SCO', 3),
                ('C', 'haiti', 'Haití', 5582, 'HTI', 4)]

    df=compararGruposDisponiblesDataFrameDetalle(grupos_real, grupos_porra)

    diccionario_detalle_grupos=limpiarDataFrameDetalleGrupos(df)

    assert sorted(list(diccionario_detalle_grupos.keys()))==["A", "B", "C"]

    for grupo in list(diccionario_detalle_grupos.keys()):

        assert len(diccionario_detalle_grupos[grupo]["filas"])==4

def test_limpiar_dataframe_detalle_grupos_todos():

    grupos_real=[('A', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 1),
                ('A', 'seleccion-mexico', 'México', 3811, 'MEX', 2),
                ('A', 'republica-checa', 'República Checa', 6188, 'CZE', 3),
                ('A', 'seleccion-sudafrica', 'Sudáfrica', 3815, 'ZAF', 4),
                ('B', 'canada', 'Canadá', 5577, 'CAN', 1),
                ('B', 'seleccion-suiza', 'Suiza', 3723, 'CHE', 2),
                ('B', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 3),
                ('B', 'seleccion-qatar', 'Catar', 3799, 'QAT', 4),
                ('C', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 1),
                ('C', 'seleccion-marruecos', 'Marruecos', 3780, 'MAR', 2),
                ('C', 'seleccion-escocia', 'Escocia', 3758, 'SCO', 3),
                ('C', 'haiti', 'Haití', 5582, 'HTI', 4),
                ('D', 'seleccion-turquia', 'Turquía', 3737, 'TUR', 1),
                ('D', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 2),
                ('D', 'seleccion-australia', 'Australia', 3801, 'AUS', 3),
                ('D', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 4),
                ('E', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 1),
                ('E', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV', 2),
                ('E', 'seleccion-ecuador', 'Ecuador', 3771, 'ECU', 3),
                ('E', 'curazao', 'Curazao', 61757, 'CUR', 4),
                ('F', 'seleccion-japon', 'Japón', 3798, 'JPN', 1),
                ('F', 'seleccion-suecia', 'Suecia', 3074, 'SWE', 2),
                ('F', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 3),
                ('F', 'seleccion-tunez', 'Túnez', 3783, 'TUN', 4),
                ('G', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 1),
                ('G', 'seleccion-egipto', 'Egipto', 3788, 'EGY', 2),
                ('G', 'seleccion-nueva-zelanda', 'Nueva Zelanda', 3808, 'NZL', 3),
                ('G', 'seleccion-iran', 'Irán', 3806, 'IRN', 4),
                ('H', 'seleccion-espanola', 'España', 3850, 'ESP', 1),
                ('H', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 2),
                ('H', 'cabo-verde', 'Cabo Verde', 9158, 'CPV', 3),
                ('H', 'seleccion-uruguay', 'Uruguay', 3768, 'URY', 4),
                ('I', 'seleccion-francia', 'Francia', 3750, 'FRA', 1),
                ('I', 'senegal', 'Senegal', 5658, 'SEN', 2),
                ('I', 'seleccion-noruega', 'Noruega', 3759, 'NOR', 3),
                ('I', 'seleccion-iraq', 'Iraq', 3816, 'IRQ', 4),
                ('J', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 1),
                ('J', 'seleccion-austria', 'Austria', 3767, 'AUT', 2),
                ('J', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 3),
                ('J', 'jordania', 'Jordania', 5480, 'JOR', 4),
                ('K', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 1),
                ('K', 'seleccion-colombia', 'Colombia', 3774, 'COL', 2),
                ('K', 'seleccion-uzbekistan', 'Uzbekistán', 3800, 'UZB', 3),
                ('K', 'rd-congo', 'RD Congo', 11591, 'COD', 4),
                ('L', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG', 1),
                ('L', 'seleccion-ghana', 'Ghana', 3791, 'GHA', 2),
                ('L', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 3),
                ('L', 'panama-seleccion', 'Panamá', 17581, 'PAN', 4)]

    grupos_porra=[('A', 'seleccion-mexico', 'México', 3811, 'MEX', 1),
                ('A', 'republica-checa', 'República Checa', 6188, 'CZE', 2),
                ('A', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 3),
                ('A', 'seleccion-sudafrica', 'Sudáfrica', 3815, 'ZAF', 4),
                ('B', 'seleccion-suiza', 'Suiza', 3723, 'CHE', 1),
                ('B', 'canada', 'Canadá', 5577, 'CAN', 2),
                ('B', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 3),
                ('B', 'seleccion-qatar', 'Catar', 3799, 'QAT', 4),
                ('C', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 1),
                ('C', 'seleccion-marruecos', 'Marruecos', 3780, 'MAR', 2),
                ('C', 'seleccion-escocia', 'Escocia', 3758, 'SCO', 3),
                ('C', 'haiti', 'Haití', 5582, 'HTI', 4),
                ('D', 'seleccion-turquia', 'Turquía', 3737, 'TUR', 1),
                ('D', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 2),
                ('D', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 3),
                ('D', 'seleccion-australia', 'Australia', 3801, 'AUS', 4),
                ('E', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 1),
                ('E', 'seleccion-ecuador', 'Ecuador', 3771, 'ECU', 2),
                ('E', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV', 3),
                ('E', 'curazao', 'Curazao', 61757, 'CUR', 4),
                ('F', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 1),
                ('F', 'seleccion-japon', 'Japón', 3798, 'JPN', 2),
                ('F', 'seleccion-suecia', 'Suecia', 3074, 'SWE', 3),
                ('F', 'seleccion-tunez', 'Túnez', 3783, 'TUN', 4),
                ('G', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 1),
                ('G', 'seleccion-egipto', 'Egipto', 3788, 'EGY', 2),
                ('G', 'seleccion-iran', 'Irán', 3806, 'IRN', 3),
                ('G', 'seleccion-nueva-zelanda', 'Nueva Zelanda', 3808, 'NZL', 4),
                ('H', 'seleccion-espanola', 'España', 3850, 'ESP', 1),
                ('H', 'seleccion-uruguay', 'Uruguay', 3768, 'URY', 2),
                ('H', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 3),
                ('H', 'cabo-verde', 'Cabo Verde', 9158, 'CPV', 4),
                ('I', 'seleccion-francia', 'Francia', 3750, 'FRA', 1),
                ('I', 'seleccion-noruega', 'Noruega', 3759, 'NOR', 2),
                ('I', 'senegal', 'Senegal', 5658, 'SEN', 3),
                ('I', 'seleccion-iraq', 'Iraq', 3816, 'IRQ', 4),
                ('J', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 1),
                ('J', 'seleccion-austria', 'Austria', 3767, 'AUT', 2),
                ('J', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 3),
                ('J', 'jordania', 'Jordania', 5480, 'JOR', 4),
                ('K', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 1),
                ('K', 'seleccion-colombia', 'Colombia', 3774, 'COL', 2),
                ('K', 'rd-congo', 'RD Congo', 11591, 'COD', 3),
                ('K', 'seleccion-uzbekistan', 'Uzbekistán', 3800, 'UZB', 4),
                ('L', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG', 1),
                ('L', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 2),
                ('L', 'seleccion-ghana', 'Ghana', 3791, 'GHA', 3),
                ('L', 'panama-seleccion', 'Panamá', 17581, 'PAN', 4)]

    df=compararGruposDisponiblesDataFrameDetalle(grupos_real, grupos_porra)

    diccionario_detalle_grupos=limpiarDataFrameDetalleGrupos(df)

    assert sorted(list(diccionario_detalle_grupos.keys()))==["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]

    for grupo in list(diccionario_detalle_grupos.keys()):

        assert len(diccionario_detalle_grupos[grupo]["filas"])==4

@pytest.mark.parametrize(["real", "puntos"],
    [   
        ({'seleccion-escocia', 'seleccion-paraguay', 'seleccion-ghana', 'rd-congo', 'seleccion-republica-corea', 'seleccion-bosnia-herzegovina', 'seleccion-arabia-saudi', 'seleccion-iran'}, 0),
        ({'seleccion-escocia', 'seleccion-paraguay', 'seleccion-ghana', 'seleccion-espanola', 'seleccion-republica-corea', 'seleccion-bosnia-herzegovina', 'seleccion-arabia-saudi', 'seleccion-iran'}, 4)
    ]
)
def test_calcular_puntos_mejores_terceros(real, puntos):

    fila=pd.Series({"grupo": "A", "equipo_porra_id": "seleccion-espanola", "equipo_porra_nombre": "España", "equipo_porra_escudo": 3850, "equipo_porra_bandera": "ESP", "posicion": 1})

    assert calcularPuntosMejoresTerceros(fila, real)==puntos

@pytest.mark.parametrize(["real", "motivo"],
    [   
        ({'seleccion-escocia', 'seleccion-paraguay', 'seleccion-ghana', 'rd-congo', 'seleccion-republica-corea', 'seleccion-bosnia-herzegovina', 'seleccion-arabia-saudi', 'seleccion-iran'}, "No fue mejor tercero"),
        ({'seleccion-escocia', 'seleccion-paraguay', 'seleccion-ghana', 'seleccion-espanola', 'seleccion-republica-corea', 'seleccion-bosnia-herzegovina', 'seleccion-arabia-saudi', 'seleccion-iran'}, "Mejor tercero acertado")
    ]
)
def test_calcular_motivo_mejores_terceros(real, motivo):

    fila=pd.Series({"grupo": "A", "equipo_porra_id": "seleccion-espanola", "equipo_porra_nombre": "España", "equipo_porra_escudo": 3850, "equipo_porra_bandera": "ESP", "posicion": 1})

    assert calcularMotivoMejoresTerceros(fila, real)==motivo

def test_comparar_mejores_terceros_dataframe_detalle_mejores_terceros_real_sin_datos():

    mejores_terceros_real=[]

    mejores_terceros_porra=[('A', 'republica-checa', 'República Checa', 6188, 'CZE', 3),
                            ('F', 'seleccion-suecia', 'Suecia', 3074, 'SWE', 3),
                            ('G', 'seleccion-iran', 'Irán', 3806, 'IRN', 3),
                            ('H', 'seleccion-espanola', 'España', 3850, 'ESP', 3),
                            ('I', 'seleccion-noruega', 'Noruega', 3759, 'NOR', 3),
                            ('J', 'seleccion-austria', 'Austria', 3767, 'AUT', 3),
                            ('K', 'rd-congo', 'RD Congo', 11591, 'COD', 3),
                            ('L', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG', 3)]

    df=compararMejoresTercerosDataFrameDetalle(mejores_terceros_real, mejores_terceros_porra)

    assert df.empty

def test_comparar_mejores_terceros_dataframe_detalle_mejores_terceros_porra_sin_datos():

    mejores_terceros_real=[('A', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 3),
                            ('B', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 3),
                            ('C', 'seleccion-escocia', 'Escocia', 3758, 'SCO', 3),
                            ('D', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 3),
                            ('G', 'seleccion-iran', 'Irán', 3806, 'IRN', 3),
                            ('H', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 3),
                            ('K', 'rd-congo', 'RD Congo', 11591, 'COD', 3),
                            ('L', 'seleccion-ghana', 'Ghana', 3791, 'GHA', 3)]

    mejores_terceros_porra=[]

    df=compararMejoresTercerosDataFrameDetalle(mejores_terceros_real, mejores_terceros_porra)

    assert not df.empty
    assert len(df)==8
    assert df["equipo_porra_id"].isnull().all()
    assert df["equipo_porra_nombre"].isnull().all()
    assert (df["puntos"]==0).all()
    assert (df["motivo"]=="Usuario sin mejores terceros").all()

def test_comparar_mejores_terceros_dataframe_detalle_mejores_terceros_porra_menos_8_registros():

    mejores_terceros_real=[('A', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 3),
                            ('B', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 3),
                            ('C', 'seleccion-escocia', 'Escocia', 3758, 'SCO', 3),
                            ('D', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 3),
                            ('G', 'seleccion-iran', 'Irán', 3806, 'IRN', 3),
                            ('H', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 3),
                            ('K', 'rd-congo', 'RD Congo', 11591, 'COD', 3),
                            ('L', 'seleccion-ghana', 'Ghana', 3791, 'GHA', 3)]

    mejores_terceros_porra=[('A', 'republica-checa', 'República Checa', 6188, 'CZE', 3),
                            ('F', 'seleccion-suecia', 'Suecia', 3074, 'SWE', 3),
                            ('G', 'seleccion-iran', 'Irán', 3806, 'IRN', 3),
                            ('H', 'seleccion-espanola', 'España', 3850, 'ESP', 3),
                            ('I', 'seleccion-noruega', 'Noruega', 3759, 'NOR', 3),
                            ('J', 'seleccion-austria', 'Austria', 3767, 'AUT', 3),
                            ('K', 'rd-congo', 'RD Congo', 11591, 'COD', 3)]

    with pytest.raises(Exception):

        compararMejoresTercerosDataFrameDetalle(mejores_terceros_real, mejores_terceros_porra)

def test_comparar_mejores_terceros_dataframe_detalle_mejores_terceros_real_menos_8_registros():

    mejores_terceros_real=[('A', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 3),
                            ('B', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 3),
                            ('C', 'seleccion-escocia', 'Escocia', 3758, 'SCO', 3),
                            ('G', 'seleccion-iran', 'Irán', 3806, 'IRN', 3),
                            ('H', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 3),
                            ('K', 'rd-congo', 'RD Congo', 11591, 'COD', 3),
                            ('L', 'seleccion-ghana', 'Ghana', 3791, 'GHA', 3)]

    mejores_terceros_porra=[('A', 'republica-checa', 'República Checa', 6188, 'CZE', 3),
                            ('F', 'seleccion-suecia', 'Suecia', 3074, 'SWE', 3),
                            ('G', 'seleccion-iran', 'Irán', 3806, 'IRN', 3),
                            ('H', 'seleccion-espanola', 'España', 3850, 'ESP', 3),
                            ('I', 'seleccion-noruega', 'Noruega', 3759, 'NOR', 3),
                            ('J', 'seleccion-austria', 'Austria', 3767, 'AUT', 3),
                            ('K', 'rd-congo', 'RD Congo', 11591, 'COD', 3),
                            ('L', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG', 3)]

    with pytest.raises(Exception):

        compararMejoresTercerosDataFrameDetalle(mejores_terceros_real, mejores_terceros_porra)

@pytest.mark.parametrize(["mejores_terceros_porra", "puntos_totales"],
    [   
        ([('A', 'republica-checa', 'República Checa', 6188, 'CZE', 3),
            ('F', 'seleccion-suecia', 'Suecia', 3074, 'SWE', 3),
            ('G', 'seleccion-iran', 'Irán', 3806, 'IRN', 3),
            ('H', 'seleccion-espanola', 'España', 3850, 'ESP', 3),
            ('I', 'seleccion-noruega', 'Noruega', 3759, 'NOR', 3),
            ('J', 'seleccion-austria', 'Austria', 3767, 'AUT', 3),
            ('K', 'rd-congo', 'RD Congo', 11591, 'COD', 3),
            ('L', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG', 3)], 8),
        ([('A', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 3),
            ('F', 'seleccion-suecia', 'Suecia', 3074, 'SWE', 3),
            ('G', 'seleccion-iran', 'Irán', 3806, 'IRN', 3),
            ('H', 'seleccion-espanola', 'España', 3850, 'ESP', 3),
            ('I', 'seleccion-noruega', 'Noruega', 3759, 'NOR', 3),
            ('J', 'seleccion-austria', 'Austria', 3767, 'AUT', 3),
            ('K', 'rd-congo', 'RD Congo', 11591, 'COD', 3),
            ('L', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG', 3)], 12),
        ([('A', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 3),
            ('F', 'seleccion-suecia', 'Suecia', 3074, 'SWE', 3),
            ('G', 'seleccion-iran', 'Irán', 3806, 'IRN', 3),
            ('H', 'seleccion-espanola', 'España', 3850, 'ESP', 3),
            ('I', 'seleccion-noruega', 'Noruega', 3759, 'NOR', 3),
            ('J', 'seleccion-austria', 'Austria', 3767, 'AUT', 3),
            ('K', 'rd-congo', 'RD Congo', 11591, 'COD', 3),
            ('L', 'seleccion-ghana', 'Ghana', 3791, 'GHA', 3)], 16)
    ]
)
def test_comparar_mejores_terceros_dataframe_detalle(mejores_terceros_porra, puntos_totales):

    mejores_terceros_real=[('A', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 3),
                            ('B', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 3),
                            ('C', 'seleccion-escocia', 'Escocia', 3758, 'SCO', 3),
                            ('D', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 3),
                            ('G', 'seleccion-iran', 'Irán', 3806, 'IRN', 3),
                            ('H', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 3),
                            ('K', 'rd-congo', 'RD Congo', 11591, 'COD', 3),
                            ('L', 'seleccion-ghana', 'Ghana', 3791, 'GHA', 3)]

    df=compararMejoresTercerosDataFrameDetalle(mejores_terceros_real, mejores_terceros_porra)

    assert not df.empty
    assert len(df)==8
    assert df["puntos"].sum()==puntos_totales

def test_calcular_puntos_totales_mejores_terceros_sin_mejores_terceros_real_sin_mejores_terceros_porra():

    mejores_terceros_real=[]

    mejores_terceros_porra=[]

    assert calcularPuntosTotalesMejoresTerceros(mejores_terceros_real, mejores_terceros_porra)==0

def test_calcular_puntos_totales_mejores_terceros_sin_mejores_terceros_real():

    mejores_terceros_real=[]

    mejores_terceros_porra=[('A', 'republica-checa', 'República Checa', 6188, 'CZE', 3),
                            ('F', 'seleccion-suecia', 'Suecia', 3074, 'SWE', 3),
                            ('G', 'seleccion-iran', 'Irán', 3806, 'IRN', 3),
                            ('H', 'seleccion-espanola', 'España', 3850, 'ESP', 3),
                            ('I', 'seleccion-noruega', 'Noruega', 3759, 'NOR', 3),
                            ('J', 'seleccion-austria', 'Austria', 3767, 'AUT', 3),
                            ('K', 'rd-congo', 'RD Congo', 11591, 'COD', 3),
                            ('L', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG', 3)]

    assert calcularPuntosTotalesMejoresTerceros(mejores_terceros_real, mejores_terceros_porra)==0

def test_calcular_puntos_totales_mejores_terceros():

    mejores_terceros_real=[('A', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 3),
                            ('B', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 3),
                            ('C', 'seleccion-escocia', 'Escocia', 3758, 'SCO', 3),
                            ('D', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 3),
                            ('G', 'seleccion-iran', 'Irán', 3806, 'IRN', 3),
                            ('H', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 3),
                            ('K', 'rd-congo', 'RD Congo', 11591, 'COD', 3),
                            ('L', 'seleccion-ghana', 'Ghana', 3791, 'GHA', 3)]

    mejores_terceros_porra=[('A', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 3),
                            ('F', 'seleccion-suecia', 'Suecia', 3074, 'SWE', 3),
                            ('G', 'seleccion-iran', 'Irán', 3806, 'IRN', 3),
                            ('H', 'seleccion-espanola', 'España', 3850, 'ESP', 3),
                            ('I', 'seleccion-noruega', 'Noruega', 3759, 'NOR', 3),
                            ('J', 'seleccion-austria', 'Austria', 3767, 'AUT', 3),
                            ('K', 'rd-congo', 'RD Congo', 11591, 'COD', 3),
                            ('L', 'seleccion-ghana', 'Ghana', 3791, 'GHA', 3)]

    assert calcularPuntosTotalesMejoresTerceros(mejores_terceros_real, mejores_terceros_porra)==16

def test_obtener_equipo_ronda_eliminatoria_sin_equipos():

    equipos_ronda_eliminatoria=obtenerEquiposRondaEliminatoria([])

@pytest.mark.parametrize(["eliminatorias_ronda"],
    [   
        ([('cuartos', 'M97', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-francia', 'Francia', 3750, 'FRA'),
        ('cuartos', 'M98', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-espanola', 'España', 3850, 'ESP')],),
        ([('final', 'M104', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-espanola', 'España', 3850, 'ESP')],),
        ([('cuartos', 'M97', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-francia', 'Francia', 3750, 'FRA'),
        ('cuartos', 'M98', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-espanola', 'España', 3850, 'ESP'),
        ('cuartos', 'M99', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
        ('cuartos', 'M100', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-argentina', 'Argentina', 3770, 'ARG')],)
    ]
)
def test_obtener_equipo_ronda_eliminatoria(eliminatorias_ronda):

    equipos_ronda_eliminatoria=obtenerEquiposRondaEliminatoria(eliminatorias_ronda)

    assert len(equipos_ronda_eliminatoria)==len(eliminatorias_ronda)*2

@pytest.mark.parametrize(["real", "puntos_ronda", "puntos_totales"],
    [   
        ({"seleccion-francia", "seleccion-espanola", "seleccion-belgica", "seleccion-holanda"}, 10, 0),
        ({"seleccion-francia", "seleccion-arabia-saudi", "seleccion-belgica", "seleccion-holanda"}, 10, 10),
        ({"seleccion-francia", "seleccion-espanola", "seleccion-belgica", "seleccion-holanda"}, 20, 0),
        ({"seleccion-francia", "seleccion-espanola", "seleccion-belgica", "seleccion-arabia-saudi"}, 20, 20),
    ]
)
def test_calcular_puntos_presencia_eliminatoria(real, puntos_ronda, puntos_totales):

    fila={"ronda":"semifinales", "equipo_porra_id":"seleccion-arabia-saudi"}

    assert calcularPuntosPresenciaEliminatoria(fila, real, puntos_ronda)==puntos_totales

@pytest.mark.parametrize(["real", "motivo"],
    [   
        ({"seleccion-francia", "seleccion-espanola", "seleccion-belgica", "seleccion-holanda"}, "No llegó a Semifinales"),
        ({"seleccion-francia", "seleccion-arabia-saudi", "seleccion-belgica", "seleccion-holanda"}, "Clasificado para Semifinales"),
        ({"seleccion-francia", "seleccion-espanola", "seleccion-belgica", "seleccion-holanda"}, "No llegó a Semifinales"),
        ({"seleccion-francia", "seleccion-espanola", "seleccion-belgica", "seleccion-arabia-saudi"}, "Clasificado para Semifinales"),
    ]
)
def test_calcular_motivo_presencia_eliminatoria(real, motivo):

    fila={"ronda":"semifinales", "equipo_porra_id":"seleccion-arabia-saudi"}

    assert calcularMotivoPresenciaEliminatoria(fila, real)==motivo

def test_comparar_ronda_eliminatoria_dataframe_detalle_eliminatoria_real_sin_datos():

    eliminatoria_real=[]

    eliminatoria_porra=[('dieciseisavos', 'M73', 'seleccion-mexico', 'México', 3811, 'MEX', 'canada', 'Canadá', 5577, 'CAN', 'seleccion-mexico', 'México', 3811, 'MEX'),
                        ('dieciseisavos', 'M74', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'haiti', 'Haití', 5582, 'HTI', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('dieciseisavos', 'M75', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-escocia', 'Escocia', 3758, 'SCO', 'seleccion-japon', 'Japón', 3798, 'JPN'),
                        ('dieciseisavos', 'M76', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('dieciseisavos', 'M77', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-suecia', 'Suecia', 3074, 'SWE', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('dieciseisavos', 'M78', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV', 'seleccion-iraq', 'Iraq', 3816, 'IRQ', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV'),
                        ('dieciseisavos', 'M79', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR'),
                        ('dieciseisavos', 'M80', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'curazao', 'Curazao', 61757, 'CUR', 'seleccion-croacia', 'Croacia', 3766, 'HRV'),
                        ('dieciseisavos', 'M81', 'seleccion-australia', 'Australia', 3801, 'AUS', 'seleccion-qatar', 'Catar', 3799, 'QAT', 'seleccion-australia', 'Australia', 3801, 'AUS'),
                        ('dieciseisavos', 'M82', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'republica-checa', 'República Checa', 6188, 'CZE', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('dieciseisavos', 'M83', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-ghana', 'Ghana', 3791, 'GHA', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('dieciseisavos', 'M84', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'),
                        ('dieciseisavos', 'M85', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-iran', 'Irán', 3806, 'IRN', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH'),
                        ('dieciseisavos', 'M86', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'cabo-verde', 'Cabo Verde', 9158, 'CPV', 'seleccion-argelia', 'Argelia', 3787, 'DZA'),
                        ('dieciseisavos', 'M87', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY'),
                        ('dieciseisavos', 'M88', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-egipto', 'Egipto', 3788, 'EGY', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA')]

    df=compararRondaEliminatoriaDataFrameDetalle(eliminatoria_real, eliminatoria_porra)

    assert df.empty

def test_ronda_comparar_eliminatoria_dataframe_detalle_eliminatoria_porra_sin_datos():

    eliminatoria_real=[('dieciseisavos', 'M73', 'republica-checa', 'República Checa', 6188, 'CZE', 'canada', 'Canadá', 5577, 'CAN', 'republica-checa', 'República Checa', 6188, 'CZE'), 
                        ('dieciseisavos', 'M74', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('dieciseisavos', 'M75', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-marruecos', 'Marruecos', 3780, 'MAR', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD'),
                        ('dieciseisavos', 'M76', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('dieciseisavos', 'M77', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-suecia', 'Suecia', 3074, 'SWE', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('dieciseisavos', 'M78', 'seleccion-ecuador', 'Ecuador', 3771, 'ECU', 'seleccion-noruega', 'Noruega', 3759, 'NOR', 'seleccion-noruega', 'Noruega', 3759, 'NOR'),
                        ('dieciseisavos', 'M79', 'seleccion-mexico', 'México', 3811, 'MEX', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-mexico', 'México', 3811, 'MEX'),
                        ('dieciseisavos', 'M80', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG', 'senegal', 'Senegal', 5658, 'SEN', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG'),
                        ('dieciseisavos', 'M81', 'seleccion-turquia', 'Turquía', 3737, 'TUR', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-turquia', 'Turquía', 3737, 'TUR'),
                        ('dieciseisavos', 'M82', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('dieciseisavos', 'M83', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'seleccion-colombia', 'Colombia', 3774, 'COL'),
                        ('dieciseisavos', 'M84', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-austria', 'Austria', 3767, 'AUT', 'seleccion-espanola', 'España', 3850, 'ESP'),
                        ('dieciseisavos', 'M85', 'seleccion-suiza', 'Suiza', 3723, 'CHE', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'seleccion-suiza', 'Suiza', 3723, 'CHE'),
                        ('dieciseisavos', 'M86', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-uruguay', 'Uruguay', 3768, 'URY', 'seleccion-argentina', 'Argentina', 3770, 'ARG'),
                        ('dieciseisavos', 'M87', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-ghana', 'Ghana', 3791, 'GHA', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('dieciseisavos', 'M88', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-egipto', 'Egipto', 3788, 'EGY', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA')]

    eliminatoria_porra=[]

    df=compararRondaEliminatoriaDataFrameDetalle(eliminatoria_real, eliminatoria_porra)

    assert df.empty

def test_comparar_ronda_eliminatoria_dataframe_detalle_eliminatoria_porra_ronda_real_distinta_ronda_porra():

    eliminatoria_real=[('dieciseisavos', 'M73', 'republica-checa', 'República Checa', 6188, 'CZE', 'canada', 'Canadá', 5577, 'CAN', 'republica-checa', 'República Checa', 6188, 'CZE'), 
                        ('dieciseisavos', 'M74', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('dieciseisavos', 'M75', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-marruecos', 'Marruecos', 3780, 'MAR', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD'),
                        ('dieciseisavos', 'M76', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('dieciseisavos', 'M77', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-suecia', 'Suecia', 3074, 'SWE', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('dieciseisavos', 'M78', 'seleccion-ecuador', 'Ecuador', 3771, 'ECU', 'seleccion-noruega', 'Noruega', 3759, 'NOR', 'seleccion-noruega', 'Noruega', 3759, 'NOR'),
                        ('dieciseisavos', 'M79', 'seleccion-mexico', 'México', 3811, 'MEX', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-mexico', 'México', 3811, 'MEX'),
                        ('dieciseisavos', 'M80', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG', 'senegal', 'Senegal', 5658, 'SEN', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG'),
                        ('dieciseisavos', 'M81', 'seleccion-turquia', 'Turquía', 3737, 'TUR', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-turquia', 'Turquía', 3737, 'TUR'),
                        ('dieciseisavos', 'M82', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('dieciseisavos', 'M83', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'seleccion-colombia', 'Colombia', 3774, 'COL'),
                        ('dieciseisavos', 'M84', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-austria', 'Austria', 3767, 'AUT', 'seleccion-espanola', 'España', 3850, 'ESP'),
                        ('dieciseisavos', 'M85', 'seleccion-suiza', 'Suiza', 3723, 'CHE', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'seleccion-suiza', 'Suiza', 3723, 'CHE'),
                        ('dieciseisavos', 'M86', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-uruguay', 'Uruguay', 3768, 'URY', 'seleccion-argentina', 'Argentina', 3770, 'ARG'),
                        ('dieciseisavos', 'M87', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-ghana', 'Ghana', 3791, 'GHA', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('dieciseisavos', 'M88', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-egipto', 'Egipto', 3788, 'EGY', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA')]

    eliminatoria_porra=[('octavos', 'M89', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('octavos', 'M90', 'seleccion-mexico', 'México', 3811, 'MEX', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-japon', 'Japón', 3798, 'JPN'),
                        ('octavos', 'M91', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV'),
                        ('octavos', 'M92', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR'),
                        ('octavos', 'M93', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'),
                        ('octavos', 'M94', 'seleccion-australia', 'Australia', 3801, 'AUS', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('octavos', 'M95', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('octavos', 'M96', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY')]

    df=compararRondaEliminatoriaDataFrameDetalle(eliminatoria_real, eliminatoria_porra)

    assert df.empty

def test_comparar_ronda_eliminatoria_dataframe_detalle_eliminatoria_porra_un_partido_eliminatoria_real():

    eliminatoria_real=[('dieciseisavos', 'M73', 'republica-checa', 'República Checa', 6188, 'CZE', 'canada', 'Canadá', 5577, 'CAN', 'republica-checa', 'República Checa', 6188, 'CZE')]

    eliminatoria_porra=[('dieciseisavos', 'M73', 'seleccion-mexico', 'México', 3811, 'MEX', 'canada', 'Canadá', 5577, 'CAN', 'seleccion-mexico', 'México', 3811, 'MEX'),
                        ('dieciseisavos', 'M74', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'haiti', 'Haití', 5582, 'HTI', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('dieciseisavos', 'M75', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-escocia', 'Escocia', 3758, 'SCO', 'seleccion-japon', 'Japón', 3798, 'JPN'),
                        ('dieciseisavos', 'M76', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('dieciseisavos', 'M77', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-suecia', 'Suecia', 3074, 'SWE', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('dieciseisavos', 'M78', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV', 'seleccion-iraq', 'Iraq', 3816, 'IRQ', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV'),
                        ('dieciseisavos', 'M79', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR'),
                        ('dieciseisavos', 'M80', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'curazao', 'Curazao', 61757, 'CUR', 'seleccion-croacia', 'Croacia', 3766, 'HRV'),
                        ('dieciseisavos', 'M81', 'seleccion-australia', 'Australia', 3801, 'AUS', 'seleccion-qatar', 'Catar', 3799, 'QAT', 'seleccion-australia', 'Australia', 3801, 'AUS'),
                        ('dieciseisavos', 'M82', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'republica-checa', 'República Checa', 6188, 'CZE', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('dieciseisavos', 'M83', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-ghana', 'Ghana', 3791, 'GHA', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('dieciseisavos', 'M84', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'),
                        ('dieciseisavos', 'M85', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-iran', 'Irán', 3806, 'IRN', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH'),
                        ('dieciseisavos', 'M86', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'cabo-verde', 'Cabo Verde', 9158, 'CPV', 'seleccion-argelia', 'Argelia', 3787, 'DZA'),
                        ('dieciseisavos', 'M87', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY'),
                        ('dieciseisavos', 'M88', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-egipto', 'Egipto', 3788, 'EGY', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA')]

    df=compararRondaEliminatoriaDataFrameDetalle(eliminatoria_real, eliminatoria_porra)

    assert not df.empty
    assert len(df)==32
    assert df["puntos"].sum()==8

def test_comparar_ronda_eliminatoria_dataframe_detalle_eliminatoria_porra_dos_partidos_eliminatoria_real():

    eliminatoria_real=[('dieciseisavos', 'M73', 'republica-checa', 'República Checa', 6188, 'CZE', 'canada', 'Canadá', 5577, 'CAN', 'republica-checa', 'República Checa', 6188, 'CZE'),
                        ('dieciseisavos', 'M85', 'seleccion-suiza', 'Suiza', 3723, 'CHE', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'seleccion-suiza', 'Suiza', 3723, 'CHE')]

    eliminatoria_porra=[('dieciseisavos', 'M73', 'seleccion-mexico', 'México', 3811, 'MEX', 'canada', 'Canadá', 5577, 'CAN', 'seleccion-mexico', 'México', 3811, 'MEX'),
                        ('dieciseisavos', 'M74', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'haiti', 'Haití', 5582, 'HTI', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('dieciseisavos', 'M75', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-escocia', 'Escocia', 3758, 'SCO', 'seleccion-japon', 'Japón', 3798, 'JPN'),
                        ('dieciseisavos', 'M76', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('dieciseisavos', 'M77', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-suecia', 'Suecia', 3074, 'SWE', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('dieciseisavos', 'M78', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV', 'seleccion-iraq', 'Iraq', 3816, 'IRQ', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV'),
                        ('dieciseisavos', 'M79', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR'),
                        ('dieciseisavos', 'M80', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'curazao', 'Curazao', 61757, 'CUR', 'seleccion-croacia', 'Croacia', 3766, 'HRV'),
                        ('dieciseisavos', 'M81', 'seleccion-australia', 'Australia', 3801, 'AUS', 'seleccion-qatar', 'Catar', 3799, 'QAT', 'seleccion-australia', 'Australia', 3801, 'AUS'),
                        ('dieciseisavos', 'M82', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'republica-checa', 'República Checa', 6188, 'CZE', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('dieciseisavos', 'M83', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-ghana', 'Ghana', 3791, 'GHA', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('dieciseisavos', 'M84', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'),
                        ('dieciseisavos', 'M85', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-iran', 'Irán', 3806, 'IRN', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH'),
                        ('dieciseisavos', 'M86', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'cabo-verde', 'Cabo Verde', 9158, 'CPV', 'seleccion-argelia', 'Argelia', 3787, 'DZA'),
                        ('dieciseisavos', 'M87', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY'),
                        ('dieciseisavos', 'M88', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-egipto', 'Egipto', 3788, 'EGY', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA')]

    df=compararRondaEliminatoriaDataFrameDetalle(eliminatoria_real, eliminatoria_porra)

    assert not df.empty
    assert len(df)==32
    assert df["puntos"].sum()==12

def test_comparar_ronda_eliminatoria_dataframe_detalle_eliminatoria_porra_tres_partidos_eliminatoria_real():

    eliminatoria_real=[('dieciseisavos', 'M73', 'republica-checa', 'República Checa', 6188, 'CZE', 'canada', 'Canadá', 5577, 'CAN', 'republica-checa', 'República Checa', 6188, 'CZE'),
                        ('dieciseisavos', 'M85', 'seleccion-suiza', 'Suiza', 3723, 'CHE', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'seleccion-suiza', 'Suiza', 3723, 'CHE'),
                        ('dieciseisavos', 'M84', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-austria', 'Austria', 3767, 'AUT', 'seleccion-espanola', 'España', 3850, 'ESP')]

    eliminatoria_porra=[('dieciseisavos', 'M73', 'seleccion-mexico', 'México', 3811, 'MEX', 'canada', 'Canadá', 5577, 'CAN', 'seleccion-mexico', 'México', 3811, 'MEX'),
                        ('dieciseisavos', 'M74', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'haiti', 'Haití', 5582, 'HTI', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('dieciseisavos', 'M75', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-escocia', 'Escocia', 3758, 'SCO', 'seleccion-japon', 'Japón', 3798, 'JPN'),
                        ('dieciseisavos', 'M76', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('dieciseisavos', 'M77', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-suecia', 'Suecia', 3074, 'SWE', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('dieciseisavos', 'M78', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV', 'seleccion-iraq', 'Iraq', 3816, 'IRQ', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV'),
                        ('dieciseisavos', 'M79', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR'),
                        ('dieciseisavos', 'M80', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'curazao', 'Curazao', 61757, 'CUR', 'seleccion-croacia', 'Croacia', 3766, 'HRV'),
                        ('dieciseisavos', 'M81', 'seleccion-australia', 'Australia', 3801, 'AUS', 'seleccion-qatar', 'Catar', 3799, 'QAT', 'seleccion-australia', 'Australia', 3801, 'AUS'),
                        ('dieciseisavos', 'M82', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'republica-checa', 'República Checa', 6188, 'CZE', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('dieciseisavos', 'M83', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-ghana', 'Ghana', 3791, 'GHA', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('dieciseisavos', 'M84', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'),
                        ('dieciseisavos', 'M85', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-iran', 'Irán', 3806, 'IRN', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH'),
                        ('dieciseisavos', 'M86', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'cabo-verde', 'Cabo Verde', 9158, 'CPV', 'seleccion-argelia', 'Argelia', 3787, 'DZA'),
                        ('dieciseisavos', 'M87', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY'),
                        ('dieciseisavos', 'M88', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-egipto', 'Egipto', 3788, 'EGY', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA')]

    df=compararRondaEliminatoriaDataFrameDetalle(eliminatoria_real, eliminatoria_porra)

    assert not df.empty
    assert len(df)==32
    assert df["puntos"].sum()==16

def test_comparar_ronda_eliminatoria_dataframe_detalle_eliminatoria_porra_todos_eliminatoria():

    eliminatoria_real=[('dieciseisavos', 'M73', 'republica-checa', 'República Checa', 6188, 'CZE', 'canada', 'Canadá', 5577, 'CAN', 'republica-checa', 'República Checa', 6188, 'CZE'), 
                        ('dieciseisavos', 'M74', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('dieciseisavos', 'M75', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-marruecos', 'Marruecos', 3780, 'MAR', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD'),
                        ('dieciseisavos', 'M76', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('dieciseisavos', 'M77', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-suecia', 'Suecia', 3074, 'SWE', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('dieciseisavos', 'M78', 'seleccion-ecuador', 'Ecuador', 3771, 'ECU', 'seleccion-noruega', 'Noruega', 3759, 'NOR', 'seleccion-noruega', 'Noruega', 3759, 'NOR'),
                        ('dieciseisavos', 'M79', 'seleccion-mexico', 'México', 3811, 'MEX', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-mexico', 'México', 3811, 'MEX'),
                        ('dieciseisavos', 'M80', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG', 'senegal', 'Senegal', 5658, 'SEN', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG'),
                        ('dieciseisavos', 'M81', 'seleccion-turquia', 'Turquía', 3737, 'TUR', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-turquia', 'Turquía', 3737, 'TUR'),
                        ('dieciseisavos', 'M82', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('dieciseisavos', 'M83', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'seleccion-colombia', 'Colombia', 3774, 'COL'),
                        ('dieciseisavos', 'M84', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-austria', 'Austria', 3767, 'AUT', 'seleccion-espanola', 'España', 3850, 'ESP'),
                        ('dieciseisavos', 'M85', 'seleccion-suiza', 'Suiza', 3723, 'CHE', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'seleccion-suiza', 'Suiza', 3723, 'CHE'),
                        ('dieciseisavos', 'M86', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-uruguay', 'Uruguay', 3768, 'URY', 'seleccion-argentina', 'Argentina', 3770, 'ARG'),
                        ('dieciseisavos', 'M87', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-ghana', 'Ghana', 3791, 'GHA', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('dieciseisavos', 'M88', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-egipto', 'Egipto', 3788, 'EGY', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA')]

    eliminatoria_porra=[('dieciseisavos', 'M73', 'seleccion-mexico', 'México', 3811, 'MEX', 'canada', 'Canadá', 5577, 'CAN', 'seleccion-mexico', 'México', 3811, 'MEX'),
                        ('dieciseisavos', 'M74', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'haiti', 'Haití', 5582, 'HTI', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('dieciseisavos', 'M75', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-escocia', 'Escocia', 3758, 'SCO', 'seleccion-japon', 'Japón', 3798, 'JPN'),
                        ('dieciseisavos', 'M76', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('dieciseisavos', 'M77', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-suecia', 'Suecia', 3074, 'SWE', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('dieciseisavos', 'M78', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV', 'seleccion-iraq', 'Iraq', 3816, 'IRQ', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV'),
                        ('dieciseisavos', 'M79', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR'),
                        ('dieciseisavos', 'M80', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'curazao', 'Curazao', 61757, 'CUR', 'seleccion-croacia', 'Croacia', 3766, 'HRV'),
                        ('dieciseisavos', 'M81', 'seleccion-australia', 'Australia', 3801, 'AUS', 'seleccion-qatar', 'Catar', 3799, 'QAT', 'seleccion-australia', 'Australia', 3801, 'AUS'),
                        ('dieciseisavos', 'M82', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'republica-checa', 'República Checa', 6188, 'CZE', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('dieciseisavos', 'M83', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-ghana', 'Ghana', 3791, 'GHA', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('dieciseisavos', 'M84', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'),
                        ('dieciseisavos', 'M85', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-iran', 'Irán', 3806, 'IRN', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH'),
                        ('dieciseisavos', 'M86', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'cabo-verde', 'Cabo Verde', 9158, 'CPV', 'seleccion-argelia', 'Argelia', 3787, 'DZA'),
                        ('dieciseisavos', 'M87', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY'),
                        ('dieciseisavos', 'M88', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-egipto', 'Egipto', 3788, 'EGY', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA')]

    df=compararRondaEliminatoriaDataFrameDetalle(eliminatoria_real, eliminatoria_porra)

    assert not df.empty
    assert len(df)==32
    assert df["puntos"].sum()==92

def test_comparar_eliminatorias_dataframe_detalle_eliminatoria_real_sin_datos():

    eliminatoria_real=[]

    eliminatoria_porra=[('dieciseisavos', 'M73', 'seleccion-mexico', 'México', 3811, 'MEX', 'canada', 'Canadá', 5577, 'CAN', 'seleccion-mexico', 'México', 3811, 'MEX'),
                        ('dieciseisavos', 'M74', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'haiti', 'Haití', 5582, 'HTI', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('dieciseisavos', 'M75', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-escocia', 'Escocia', 3758, 'SCO', 'seleccion-japon', 'Japón', 3798, 'JPN'),
                        ('dieciseisavos', 'M76', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('dieciseisavos', 'M77', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-suecia', 'Suecia', 3074, 'SWE', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('dieciseisavos', 'M78', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV', 'seleccion-iraq', 'Iraq', 3816, 'IRQ', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV'),
                        ('dieciseisavos', 'M79', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR'),
                        ('dieciseisavos', 'M80', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'curazao', 'Curazao', 61757, 'CUR', 'seleccion-croacia', 'Croacia', 3766, 'HRV'),
                        ('dieciseisavos', 'M81', 'seleccion-australia', 'Australia', 3801, 'AUS', 'seleccion-qatar', 'Catar', 3799, 'QAT', 'seleccion-australia', 'Australia', 3801, 'AUS'),
                        ('dieciseisavos', 'M82', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'republica-checa', 'República Checa', 6188, 'CZE', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('dieciseisavos', 'M83', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-ghana', 'Ghana', 3791, 'GHA', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('dieciseisavos', 'M84', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'),
                        ('dieciseisavos', 'M85', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-iran', 'Irán', 3806, 'IRN', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH'),
                        ('dieciseisavos', 'M86', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'cabo-verde', 'Cabo Verde', 9158, 'CPV', 'seleccion-argelia', 'Argelia', 3787, 'DZA'),
                        ('dieciseisavos', 'M87', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY'),
                        ('dieciseisavos', 'M88', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-egipto', 'Egipto', 3788, 'EGY', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA')]

    df=compararEliminatoriasDisponiblesDataFrameDetalle(eliminatoria_real, eliminatoria_porra)

    assert df.empty

def test_comparar_eliminatorias_dataframe_detalle_eliminatoria_porra_sin_datos():

    eliminatoria_real=[('dieciseisavos', 'M73', 'republica-checa', 'República Checa', 6188, 'CZE', 'canada', 'Canadá', 5577, 'CAN', 'republica-checa', 'República Checa', 6188, 'CZE'), 
                        ('dieciseisavos', 'M74', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('dieciseisavos', 'M75', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-marruecos', 'Marruecos', 3780, 'MAR', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD'),
                        ('dieciseisavos', 'M76', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('dieciseisavos', 'M77', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-suecia', 'Suecia', 3074, 'SWE', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('dieciseisavos', 'M78', 'seleccion-ecuador', 'Ecuador', 3771, 'ECU', 'seleccion-noruega', 'Noruega', 3759, 'NOR', 'seleccion-noruega', 'Noruega', 3759, 'NOR'),
                        ('dieciseisavos', 'M79', 'seleccion-mexico', 'México', 3811, 'MEX', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-mexico', 'México', 3811, 'MEX'),
                        ('dieciseisavos', 'M80', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG', 'senegal', 'Senegal', 5658, 'SEN', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG'),
                        ('dieciseisavos', 'M81', 'seleccion-turquia', 'Turquía', 3737, 'TUR', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-turquia', 'Turquía', 3737, 'TUR'),
                        ('dieciseisavos', 'M82', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('dieciseisavos', 'M83', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'seleccion-colombia', 'Colombia', 3774, 'COL'),
                        ('dieciseisavos', 'M84', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-austria', 'Austria', 3767, 'AUT', 'seleccion-espanola', 'España', 3850, 'ESP'),
                        ('dieciseisavos', 'M85', 'seleccion-suiza', 'Suiza', 3723, 'CHE', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'seleccion-suiza', 'Suiza', 3723, 'CHE'),
                        ('dieciseisavos', 'M86', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-uruguay', 'Uruguay', 3768, 'URY', 'seleccion-argentina', 'Argentina', 3770, 'ARG'),
                        ('dieciseisavos', 'M87', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-ghana', 'Ghana', 3791, 'GHA', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('dieciseisavos', 'M88', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-egipto', 'Egipto', 3788, 'EGY', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA')]

    eliminatoria_porra=[]

    df=compararEliminatoriasDisponiblesDataFrameDetalle(eliminatoria_real, eliminatoria_porra)

    assert df.empty

def test_comparar_eliminatorias_dataframe_detalle_eliminatoria_porra_un_partido_ronda_real_una_ronda_porra():

    eliminatoria_real=[('dieciseisavos', 'M73', 'republica-checa', 'República Checa', 6188, 'CZE', 'canada', 'Canadá', 5577, 'CAN', 'republica-checa', 'República Checa', 6188, 'CZE')]

    eliminatoria_porra=[('dieciseisavos', 'M73', 'seleccion-mexico', 'México', 3811, 'MEX', 'canada', 'Canadá', 5577, 'CAN', 'seleccion-mexico', 'México', 3811, 'MEX'),
                        ('dieciseisavos', 'M74', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'haiti', 'Haití', 5582, 'HTI', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('dieciseisavos', 'M75', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-escocia', 'Escocia', 3758, 'SCO', 'seleccion-japon', 'Japón', 3798, 'JPN'),
                        ('dieciseisavos', 'M76', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('dieciseisavos', 'M77', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-suecia', 'Suecia', 3074, 'SWE', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('dieciseisavos', 'M78', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV', 'seleccion-iraq', 'Iraq', 3816, 'IRQ', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV'),
                        ('dieciseisavos', 'M79', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR'),
                        ('dieciseisavos', 'M80', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'curazao', 'Curazao', 61757, 'CUR', 'seleccion-croacia', 'Croacia', 3766, 'HRV'),
                        ('dieciseisavos', 'M81', 'seleccion-australia', 'Australia', 3801, 'AUS', 'seleccion-qatar', 'Catar', 3799, 'QAT', 'seleccion-australia', 'Australia', 3801, 'AUS'),
                        ('dieciseisavos', 'M82', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'republica-checa', 'República Checa', 6188, 'CZE', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('dieciseisavos', 'M83', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-ghana', 'Ghana', 3791, 'GHA', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('dieciseisavos', 'M84', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'),
                        ('dieciseisavos', 'M85', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-iran', 'Irán', 3806, 'IRN', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH'),
                        ('dieciseisavos', 'M86', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'cabo-verde', 'Cabo Verde', 9158, 'CPV', 'seleccion-argelia', 'Argelia', 3787, 'DZA'),
                        ('dieciseisavos', 'M87', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY'),
                        ('dieciseisavos', 'M88', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-egipto', 'Egipto', 3788, 'EGY', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA')]

    df=compararEliminatoriasDisponiblesDataFrameDetalle(eliminatoria_real, eliminatoria_porra)

    assert not df.empty
    assert len(df)==32
    assert sorted(df["ronda"].unique().tolist())==["dieciseisavos"]

def test_comparar_eliminatorias_dataframe_detalle_eliminatoria_porra_una_ronda_real_una_ronda_porra():

    eliminatoria_real=[('dieciseisavos', 'M73', 'republica-checa', 'República Checa', 6188, 'CZE', 'canada', 'Canadá', 5577, 'CAN', 'republica-checa', 'República Checa', 6188, 'CZE'), 
                        ('dieciseisavos', 'M74', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('dieciseisavos', 'M75', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-marruecos', 'Marruecos', 3780, 'MAR', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD'),
                        ('dieciseisavos', 'M76', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('dieciseisavos', 'M77', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-suecia', 'Suecia', 3074, 'SWE', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('dieciseisavos', 'M78', 'seleccion-ecuador', 'Ecuador', 3771, 'ECU', 'seleccion-noruega', 'Noruega', 3759, 'NOR', 'seleccion-noruega', 'Noruega', 3759, 'NOR'),
                        ('dieciseisavos', 'M79', 'seleccion-mexico', 'México', 3811, 'MEX', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-mexico', 'México', 3811, 'MEX'),
                        ('dieciseisavos', 'M80', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG', 'senegal', 'Senegal', 5658, 'SEN', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG'),
                        ('dieciseisavos', 'M81', 'seleccion-turquia', 'Turquía', 3737, 'TUR', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-turquia', 'Turquía', 3737, 'TUR'),
                        ('dieciseisavos', 'M82', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('dieciseisavos', 'M83', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'seleccion-colombia', 'Colombia', 3774, 'COL'),
                        ('dieciseisavos', 'M84', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-austria', 'Austria', 3767, 'AUT', 'seleccion-espanola', 'España', 3850, 'ESP'),
                        ('dieciseisavos', 'M85', 'seleccion-suiza', 'Suiza', 3723, 'CHE', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'seleccion-suiza', 'Suiza', 3723, 'CHE'),
                        ('dieciseisavos', 'M86', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-uruguay', 'Uruguay', 3768, 'URY', 'seleccion-argentina', 'Argentina', 3770, 'ARG'),
                        ('dieciseisavos', 'M87', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-ghana', 'Ghana', 3791, 'GHA', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('dieciseisavos', 'M88', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-egipto', 'Egipto', 3788, 'EGY', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA')]

    eliminatoria_porra=[('dieciseisavos', 'M73', 'seleccion-mexico', 'México', 3811, 'MEX', 'canada', 'Canadá', 5577, 'CAN', 'seleccion-mexico', 'México', 3811, 'MEX'),
                        ('dieciseisavos', 'M74', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'haiti', 'Haití', 5582, 'HTI', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('dieciseisavos', 'M75', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-escocia', 'Escocia', 3758, 'SCO', 'seleccion-japon', 'Japón', 3798, 'JPN'),
                        ('dieciseisavos', 'M76', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('dieciseisavos', 'M77', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-suecia', 'Suecia', 3074, 'SWE', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('dieciseisavos', 'M78', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV', 'seleccion-iraq', 'Iraq', 3816, 'IRQ', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV'),
                        ('dieciseisavos', 'M79', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR'),
                        ('dieciseisavos', 'M80', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'curazao', 'Curazao', 61757, 'CUR', 'seleccion-croacia', 'Croacia', 3766, 'HRV'),
                        ('dieciseisavos', 'M81', 'seleccion-australia', 'Australia', 3801, 'AUS', 'seleccion-qatar', 'Catar', 3799, 'QAT', 'seleccion-australia', 'Australia', 3801, 'AUS'),
                        ('dieciseisavos', 'M82', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'republica-checa', 'República Checa', 6188, 'CZE', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('dieciseisavos', 'M83', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-ghana', 'Ghana', 3791, 'GHA', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('dieciseisavos', 'M84', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'),
                        ('dieciseisavos', 'M85', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-iran', 'Irán', 3806, 'IRN', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH'),
                        ('dieciseisavos', 'M86', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'cabo-verde', 'Cabo Verde', 9158, 'CPV', 'seleccion-argelia', 'Argelia', 3787, 'DZA'),
                        ('dieciseisavos', 'M87', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY'),
                        ('dieciseisavos', 'M88', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-egipto', 'Egipto', 3788, 'EGY', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA')]

    df=compararEliminatoriasDisponiblesDataFrameDetalle(eliminatoria_real, eliminatoria_porra)

    assert not df.empty
    assert len(df)==32
    assert sorted(df["ronda"].unique().tolist())==["dieciseisavos"]

def test_comparar_eliminatorias_dataframe_detalle_eliminatoria_porra_una_ronda_real_dos_rondas_porra():

    eliminatoria_real=[('dieciseisavos', 'M73', 'republica-checa', 'República Checa', 6188, 'CZE', 'canada', 'Canadá', 5577, 'CAN', 'republica-checa', 'República Checa', 6188, 'CZE'), 
                        ('dieciseisavos', 'M74', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('dieciseisavos', 'M75', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-marruecos', 'Marruecos', 3780, 'MAR', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD'),
                        ('dieciseisavos', 'M76', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('dieciseisavos', 'M77', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-suecia', 'Suecia', 3074, 'SWE', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('dieciseisavos', 'M78', 'seleccion-ecuador', 'Ecuador', 3771, 'ECU', 'seleccion-noruega', 'Noruega', 3759, 'NOR', 'seleccion-noruega', 'Noruega', 3759, 'NOR'),
                        ('dieciseisavos', 'M79', 'seleccion-mexico', 'México', 3811, 'MEX', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-mexico', 'México', 3811, 'MEX'),
                        ('dieciseisavos', 'M80', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG', 'senegal', 'Senegal', 5658, 'SEN', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG'),
                        ('dieciseisavos', 'M81', 'seleccion-turquia', 'Turquía', 3737, 'TUR', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-turquia', 'Turquía', 3737, 'TUR'),
                        ('dieciseisavos', 'M82', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('dieciseisavos', 'M83', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'seleccion-colombia', 'Colombia', 3774, 'COL'),
                        ('dieciseisavos', 'M84', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-austria', 'Austria', 3767, 'AUT', 'seleccion-espanola', 'España', 3850, 'ESP'),
                        ('dieciseisavos', 'M85', 'seleccion-suiza', 'Suiza', 3723, 'CHE', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'seleccion-suiza', 'Suiza', 3723, 'CHE'),
                        ('dieciseisavos', 'M86', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-uruguay', 'Uruguay', 3768, 'URY', 'seleccion-argentina', 'Argentina', 3770, 'ARG'),
                        ('dieciseisavos', 'M87', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-ghana', 'Ghana', 3791, 'GHA', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('dieciseisavos', 'M88', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-egipto', 'Egipto', 3788, 'EGY', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA')]

    eliminatoria_porra=[('dieciseisavos', 'M73', 'seleccion-mexico', 'México', 3811, 'MEX', 'canada', 'Canadá', 5577, 'CAN', 'seleccion-mexico', 'México', 3811, 'MEX'),
                        ('dieciseisavos', 'M74', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'haiti', 'Haití', 5582, 'HTI', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('dieciseisavos', 'M75', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-escocia', 'Escocia', 3758, 'SCO', 'seleccion-japon', 'Japón', 3798, 'JPN'),
                        ('dieciseisavos', 'M76', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('dieciseisavos', 'M77', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-suecia', 'Suecia', 3074, 'SWE', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('dieciseisavos', 'M78', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV', 'seleccion-iraq', 'Iraq', 3816, 'IRQ', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV'),
                        ('dieciseisavos', 'M79', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR'),
                        ('dieciseisavos', 'M80', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'curazao', 'Curazao', 61757, 'CUR', 'seleccion-croacia', 'Croacia', 3766, 'HRV'),
                        ('dieciseisavos', 'M81', 'seleccion-australia', 'Australia', 3801, 'AUS', 'seleccion-qatar', 'Catar', 3799, 'QAT', 'seleccion-australia', 'Australia', 3801, 'AUS'),
                        ('dieciseisavos', 'M82', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'republica-checa', 'República Checa', 6188, 'CZE', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('dieciseisavos', 'M83', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-ghana', 'Ghana', 3791, 'GHA', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('dieciseisavos', 'M84', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'),
                        ('dieciseisavos', 'M85', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-iran', 'Irán', 3806, 'IRN', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH'),
                        ('dieciseisavos', 'M86', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'cabo-verde', 'Cabo Verde', 9158, 'CPV', 'seleccion-argelia', 'Argelia', 3787, 'DZA'),
                        ('dieciseisavos', 'M87', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY'),
                        ('dieciseisavos', 'M88', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-egipto', 'Egipto', 3788, 'EGY', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('octavos', 'M89', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('octavos', 'M90', 'seleccion-mexico', 'México', 3811, 'MEX', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-japon', 'Japón', 3798, 'JPN'),
                        ('octavos', 'M91', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV'),
                        ('octavos', 'M92', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR'),
                        ('octavos', 'M93', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'),
                        ('octavos', 'M94', 'seleccion-australia', 'Australia', 3801, 'AUS', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('octavos', 'M95', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('octavos', 'M96', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY')]

    df=compararEliminatoriasDisponiblesDataFrameDetalle(eliminatoria_real, eliminatoria_porra)

    assert not df.empty
    assert len(df)==32
    assert sorted(df["ronda"].unique().tolist())==["dieciseisavos"]

def test_comparar_eliminatorias_dataframe_detalle_eliminatoria_porra_un_partido_dos_rondas_real_dos_rondas_porra():

    eliminatoria_real=[('dieciseisavos', 'M73', 'republica-checa', 'República Checa', 6188, 'CZE', 'canada', 'Canadá', 5577, 'CAN', 'republica-checa', 'República Checa', 6188, 'CZE'), 
                        ('dieciseisavos', 'M74', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('dieciseisavos', 'M75', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-marruecos', 'Marruecos', 3780, 'MAR', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD'),
                        ('dieciseisavos', 'M76', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('dieciseisavos', 'M77', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-suecia', 'Suecia', 3074, 'SWE', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('dieciseisavos', 'M78', 'seleccion-ecuador', 'Ecuador', 3771, 'ECU', 'seleccion-noruega', 'Noruega', 3759, 'NOR', 'seleccion-noruega', 'Noruega', 3759, 'NOR'),
                        ('dieciseisavos', 'M79', 'seleccion-mexico', 'México', 3811, 'MEX', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-mexico', 'México', 3811, 'MEX'),
                        ('dieciseisavos', 'M80', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG', 'senegal', 'Senegal', 5658, 'SEN', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG'),
                        ('dieciseisavos', 'M81', 'seleccion-turquia', 'Turquía', 3737, 'TUR', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-turquia', 'Turquía', 3737, 'TUR'),
                        ('dieciseisavos', 'M82', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('dieciseisavos', 'M83', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'seleccion-colombia', 'Colombia', 3774, 'COL'),
                        ('dieciseisavos', 'M84', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-austria', 'Austria', 3767, 'AUT', 'seleccion-espanola', 'España', 3850, 'ESP'),
                        ('dieciseisavos', 'M85', 'seleccion-suiza', 'Suiza', 3723, 'CHE', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'seleccion-suiza', 'Suiza', 3723, 'CHE'),
                        ('dieciseisavos', 'M86', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-uruguay', 'Uruguay', 3768, 'URY', 'seleccion-argentina', 'Argentina', 3770, 'ARG'),
                        ('dieciseisavos', 'M87', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-ghana', 'Ghana', 3791, 'GHA', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('dieciseisavos', 'M88', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-egipto', 'Egipto', 3788, 'EGY', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('octavos', 'M89', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-alemania', 'Alemania', 3734, 'DEU')]

    eliminatoria_porra=[('dieciseisavos', 'M73', 'seleccion-mexico', 'México', 3811, 'MEX', 'canada', 'Canadá', 5577, 'CAN', 'seleccion-mexico', 'México', 3811, 'MEX'),
                        ('dieciseisavos', 'M74', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'haiti', 'Haití', 5582, 'HTI', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('dieciseisavos', 'M75', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-escocia', 'Escocia', 3758, 'SCO', 'seleccion-japon', 'Japón', 3798, 'JPN'),
                        ('dieciseisavos', 'M76', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('dieciseisavos', 'M77', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-suecia', 'Suecia', 3074, 'SWE', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('dieciseisavos', 'M78', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV', 'seleccion-iraq', 'Iraq', 3816, 'IRQ', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV'),
                        ('dieciseisavos', 'M79', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR'),
                        ('dieciseisavos', 'M80', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'curazao', 'Curazao', 61757, 'CUR', 'seleccion-croacia', 'Croacia', 3766, 'HRV'),
                        ('dieciseisavos', 'M81', 'seleccion-australia', 'Australia', 3801, 'AUS', 'seleccion-qatar', 'Catar', 3799, 'QAT', 'seleccion-australia', 'Australia', 3801, 'AUS'),
                        ('dieciseisavos', 'M82', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'republica-checa', 'República Checa', 6188, 'CZE', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('dieciseisavos', 'M83', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-ghana', 'Ghana', 3791, 'GHA', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('dieciseisavos', 'M84', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'),
                        ('dieciseisavos', 'M85', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-iran', 'Irán', 3806, 'IRN', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH'),
                        ('dieciseisavos', 'M86', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'cabo-verde', 'Cabo Verde', 9158, 'CPV', 'seleccion-argelia', 'Argelia', 3787, 'DZA'),
                        ('dieciseisavos', 'M87', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY'),
                        ('dieciseisavos', 'M88', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-egipto', 'Egipto', 3788, 'EGY', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('octavos', 'M89', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('octavos', 'M90', 'seleccion-mexico', 'México', 3811, 'MEX', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-japon', 'Japón', 3798, 'JPN'),
                        ('octavos', 'M91', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV'),
                        ('octavos', 'M92', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR'),
                        ('octavos', 'M93', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'),
                        ('octavos', 'M94', 'seleccion-australia', 'Australia', 3801, 'AUS', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('octavos', 'M95', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('octavos', 'M96', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY')]

    df=compararEliminatoriasDisponiblesDataFrameDetalle(eliminatoria_real, eliminatoria_porra)

    assert not df.empty
    assert len(df)==48
    assert sorted(df["ronda"].unique().tolist())==["dieciseisavos", "octavos"]

def test_comparar_eliminatorias_dataframe_detalle_eliminatoria_porra_dos_rondas_real_dos_rondas_porra():

    eliminatoria_real=[('dieciseisavos', 'M73', 'republica-checa', 'República Checa', 6188, 'CZE', 'canada', 'Canadá', 5577, 'CAN', 'republica-checa', 'República Checa', 6188, 'CZE'), 
                        ('dieciseisavos', 'M74', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('dieciseisavos', 'M75', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-marruecos', 'Marruecos', 3780, 'MAR', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD'),
                        ('dieciseisavos', 'M76', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('dieciseisavos', 'M77', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-suecia', 'Suecia', 3074, 'SWE', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('dieciseisavos', 'M78', 'seleccion-ecuador', 'Ecuador', 3771, 'ECU', 'seleccion-noruega', 'Noruega', 3759, 'NOR', 'seleccion-noruega', 'Noruega', 3759, 'NOR'),
                        ('dieciseisavos', 'M79', 'seleccion-mexico', 'México', 3811, 'MEX', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-mexico', 'México', 3811, 'MEX'),
                        ('dieciseisavos', 'M80', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG', 'senegal', 'Senegal', 5658, 'SEN', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG'),
                        ('dieciseisavos', 'M81', 'seleccion-turquia', 'Turquía', 3737, 'TUR', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-turquia', 'Turquía', 3737, 'TUR'),
                        ('dieciseisavos', 'M82', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('dieciseisavos', 'M83', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'seleccion-colombia', 'Colombia', 3774, 'COL'),
                        ('dieciseisavos', 'M84', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-austria', 'Austria', 3767, 'AUT', 'seleccion-espanola', 'España', 3850, 'ESP'),
                        ('dieciseisavos', 'M85', 'seleccion-suiza', 'Suiza', 3723, 'CHE', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'seleccion-suiza', 'Suiza', 3723, 'CHE'),
                        ('dieciseisavos', 'M86', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-uruguay', 'Uruguay', 3768, 'URY', 'seleccion-argentina', 'Argentina', 3770, 'ARG'),
                        ('dieciseisavos', 'M87', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-ghana', 'Ghana', 3791, 'GHA', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('dieciseisavos', 'M88', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-egipto', 'Egipto', 3788, 'EGY', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('octavos', 'M89', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('octavos', 'M90', 'republica-checa', 'República Checa', 6188, 'CZE', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD'),
                        ('octavos', 'M91', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-noruega', 'Noruega', 3759, 'NOR', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('octavos', 'M92', 'seleccion-mexico', 'México', 3811, 'MEX', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG'),
                        ('octavos', 'M93', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-espanola', 'España', 3850, 'ESP'),
                        ('octavos', 'M94', 'seleccion-turquia', 'Turquía', 3737, 'TUR', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('octavos', 'M95', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-argentina', 'Argentina', 3770, 'ARG'),
                        ('octavos', 'M96', 'seleccion-suiza', 'Suiza', 3723, 'CHE', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-portugal', 'Portugal', 3762, 'PRT')]

    eliminatoria_porra=[('dieciseisavos', 'M73', 'seleccion-mexico', 'México', 3811, 'MEX', 'canada', 'Canadá', 5577, 'CAN', 'seleccion-mexico', 'México', 3811, 'MEX'),
                        ('dieciseisavos', 'M74', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'haiti', 'Haití', 5582, 'HTI', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('dieciseisavos', 'M75', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-escocia', 'Escocia', 3758, 'SCO', 'seleccion-japon', 'Japón', 3798, 'JPN'),
                        ('dieciseisavos', 'M76', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('dieciseisavos', 'M77', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-suecia', 'Suecia', 3074, 'SWE', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('dieciseisavos', 'M78', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV', 'seleccion-iraq', 'Iraq', 3816, 'IRQ', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV'),
                        ('dieciseisavos', 'M79', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR'),
                        ('dieciseisavos', 'M80', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'curazao', 'Curazao', 61757, 'CUR', 'seleccion-croacia', 'Croacia', 3766, 'HRV'),
                        ('dieciseisavos', 'M81', 'seleccion-australia', 'Australia', 3801, 'AUS', 'seleccion-qatar', 'Catar', 3799, 'QAT', 'seleccion-australia', 'Australia', 3801, 'AUS'),
                        ('dieciseisavos', 'M82', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'republica-checa', 'República Checa', 6188, 'CZE', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('dieciseisavos', 'M83', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-ghana', 'Ghana', 3791, 'GHA', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('dieciseisavos', 'M84', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'),
                        ('dieciseisavos', 'M85', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-iran', 'Irán', 3806, 'IRN', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH'),
                        ('dieciseisavos', 'M86', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'cabo-verde', 'Cabo Verde', 9158, 'CPV', 'seleccion-argelia', 'Argelia', 3787, 'DZA'),
                        ('dieciseisavos', 'M87', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY'),
                        ('dieciseisavos', 'M88', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-egipto', 'Egipto', 3788, 'EGY', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('octavos', 'M89', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('octavos', 'M90', 'seleccion-mexico', 'México', 3811, 'MEX', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-japon', 'Japón', 3798, 'JPN'),
                        ('octavos', 'M91', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV'),
                        ('octavos', 'M92', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR'),
                        ('octavos', 'M93', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'),
                        ('octavos', 'M94', 'seleccion-australia', 'Australia', 3801, 'AUS', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('octavos', 'M95', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('octavos', 'M96', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY')]

    df=compararEliminatoriasDisponiblesDataFrameDetalle(eliminatoria_real, eliminatoria_porra)

    assert not df.empty
    assert len(df)==48
    assert sorted(df["ronda"].unique().tolist())==["dieciseisavos", "octavos"]

def test_comparar_eliminatorias_dataframe_detalle_eliminatoria_porra_todos():

    eliminatoria_real=[('dieciseisavos', 'M73', 'republica-checa', 'República Checa', 6188, 'CZE', 'canada', 'Canadá', 5577, 'CAN', 'republica-checa', 'República Checa', 6188, 'CZE'), 
                        ('dieciseisavos', 'M74', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('dieciseisavos', 'M75', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-marruecos', 'Marruecos', 3780, 'MAR', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD'),
                        ('dieciseisavos', 'M76', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('dieciseisavos', 'M77', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-suecia', 'Suecia', 3074, 'SWE', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('dieciseisavos', 'M78', 'seleccion-ecuador', 'Ecuador', 3771, 'ECU', 'seleccion-noruega', 'Noruega', 3759, 'NOR', 'seleccion-noruega', 'Noruega', 3759, 'NOR'),
                        ('dieciseisavos', 'M79', 'seleccion-mexico', 'México', 3811, 'MEX', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-mexico', 'México', 3811, 'MEX'),
                        ('dieciseisavos', 'M80', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG', 'senegal', 'Senegal', 5658, 'SEN', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG'),
                        ('dieciseisavos', 'M81', 'seleccion-turquia', 'Turquía', 3737, 'TUR', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-turquia', 'Turquía', 3737, 'TUR'),
                        ('dieciseisavos', 'M82', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('dieciseisavos', 'M83', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'seleccion-colombia', 'Colombia', 3774, 'COL'),
                        ('dieciseisavos', 'M84', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-austria', 'Austria', 3767, 'AUT', 'seleccion-espanola', 'España', 3850, 'ESP'),
                        ('dieciseisavos', 'M85', 'seleccion-suiza', 'Suiza', 3723, 'CHE', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'seleccion-suiza', 'Suiza', 3723, 'CHE'),
                        ('dieciseisavos', 'M86', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-uruguay', 'Uruguay', 3768, 'URY', 'seleccion-argentina', 'Argentina', 3770, 'ARG'),
                        ('dieciseisavos', 'M87', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-ghana', 'Ghana', 3791, 'GHA', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('dieciseisavos', 'M88', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-egipto', 'Egipto', 3788, 'EGY', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('octavos', 'M89', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('octavos', 'M90', 'republica-checa', 'República Checa', 6188, 'CZE', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD'),
                        ('octavos', 'M91', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-noruega', 'Noruega', 3759, 'NOR', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('octavos', 'M92', 'seleccion-mexico', 'México', 3811, 'MEX', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG'),
                        ('octavos', 'M93', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-espanola', 'España', 3850, 'ESP'),
                        ('octavos', 'M94', 'seleccion-turquia', 'Turquía', 3737, 'TUR', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('octavos', 'M95', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-argentina', 'Argentina', 3770, 'ARG'),
                        ('octavos', 'M96', 'seleccion-suiza', 'Suiza', 3723, 'CHE', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('cuartos', 'M97', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('cuartos', 'M98', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-espanola', 'España', 3850, 'ESP'),
                        ('cuartos', 'M99', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('cuartos', 'M100', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-argentina', 'Argentina', 3770, 'ARG'),
                        ('semifinales', 'M101', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-espanola', 'España', 3850, 'ESP'),
                        ('semifinales', 'M102', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-argentina', 'Argentina', 3770, 'ARG'),
                        ('tercer_puesto', 'M103', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('final', 'M104', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-espanola', 'España', 3850, 'ESP')]

    eliminatoria_porra=[('dieciseisavos', 'M73', 'seleccion-mexico', 'México', 3811, 'MEX', 'canada', 'Canadá', 5577, 'CAN', 'seleccion-mexico', 'México', 3811, 'MEX'),
                        ('dieciseisavos', 'M74', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'haiti', 'Haití', 5582, 'HTI', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('dieciseisavos', 'M75', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-escocia', 'Escocia', 3758, 'SCO', 'seleccion-japon', 'Japón', 3798, 'JPN'),
                        ('dieciseisavos', 'M76', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('dieciseisavos', 'M77', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-suecia', 'Suecia', 3074, 'SWE', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('dieciseisavos', 'M78', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV', 'seleccion-iraq', 'Iraq', 3816, 'IRQ', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV'),
                        ('dieciseisavos', 'M79', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR'),
                        ('dieciseisavos', 'M80', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'curazao', 'Curazao', 61757, 'CUR', 'seleccion-croacia', 'Croacia', 3766, 'HRV'),
                        ('dieciseisavos', 'M81', 'seleccion-australia', 'Australia', 3801, 'AUS', 'seleccion-qatar', 'Catar', 3799, 'QAT', 'seleccion-australia', 'Australia', 3801, 'AUS'),
                        ('dieciseisavos', 'M82', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'republica-checa', 'República Checa', 6188, 'CZE', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('dieciseisavos', 'M83', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-ghana', 'Ghana', 3791, 'GHA', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('dieciseisavos', 'M84', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'),
                        ('dieciseisavos', 'M85', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-iran', 'Irán', 3806, 'IRN', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH'),
                        ('dieciseisavos', 'M86', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'cabo-verde', 'Cabo Verde', 9158, 'CPV', 'seleccion-argelia', 'Argelia', 3787, 'DZA'),
                        ('dieciseisavos', 'M87', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY'),
                        ('dieciseisavos', 'M88', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-egipto', 'Egipto', 3788, 'EGY', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('octavos', 'M89', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('octavos', 'M90', 'seleccion-mexico', 'México', 3811, 'MEX', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-japon', 'Japón', 3798, 'JPN'),
                        ('octavos', 'M91', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV'),
                        ('octavos', 'M92', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR'),
                        ('octavos', 'M93', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'),
                        ('octavos', 'M94', 'seleccion-australia', 'Australia', 3801, 'AUS', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('octavos', 'M95', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('octavos', 'M96', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY'),
                        ('cuartos', 'M97', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('cuartos', 'M98', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'),
                        ('cuartos', 'M99', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR'),
                        ('cuartos', 'M100', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('semifinales', 'M101', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'),
                        ('semifinales', 'M102', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('tercer_puesto', 'M103', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('final', 'M104', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU')]

    df=compararEliminatoriasDisponiblesDataFrameDetalle(eliminatoria_real, eliminatoria_porra)

    assert not df.empty
    assert len(df)==64
    assert sorted(df["ronda"].unique().tolist())==["cuartos", "dieciseisavos", "final", "octavos", "semifinales", "tercer_puesto"]

def test_calcular_puntos_totales_eliminatorias_eliminatoria_real_sin_datos():

    eliminatoria_real=[]

    eliminatoria_porra=[('dieciseisavos', 'M73', 'seleccion-mexico', 'México', 3811, 'MEX', 'canada', 'Canadá', 5577, 'CAN', 'seleccion-mexico', 'México', 3811, 'MEX'),
                        ('dieciseisavos', 'M74', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'haiti', 'Haití', 5582, 'HTI', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('dieciseisavos', 'M75', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-escocia', 'Escocia', 3758, 'SCO', 'seleccion-japon', 'Japón', 3798, 'JPN'),
                        ('dieciseisavos', 'M76', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('dieciseisavos', 'M77', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-suecia', 'Suecia', 3074, 'SWE', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('dieciseisavos', 'M78', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV', 'seleccion-iraq', 'Iraq', 3816, 'IRQ', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV'),
                        ('dieciseisavos', 'M79', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR'),
                        ('dieciseisavos', 'M80', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'curazao', 'Curazao', 61757, 'CUR', 'seleccion-croacia', 'Croacia', 3766, 'HRV'),
                        ('dieciseisavos', 'M81', 'seleccion-australia', 'Australia', 3801, 'AUS', 'seleccion-qatar', 'Catar', 3799, 'QAT', 'seleccion-australia', 'Australia', 3801, 'AUS'),
                        ('dieciseisavos', 'M82', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'republica-checa', 'República Checa', 6188, 'CZE', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('dieciseisavos', 'M83', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-ghana', 'Ghana', 3791, 'GHA', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('dieciseisavos', 'M84', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'),
                        ('dieciseisavos', 'M85', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-iran', 'Irán', 3806, 'IRN', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH'),
                        ('dieciseisavos', 'M86', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'cabo-verde', 'Cabo Verde', 9158, 'CPV', 'seleccion-argelia', 'Argelia', 3787, 'DZA'),
                        ('dieciseisavos', 'M87', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY'),
                        ('dieciseisavos', 'M88', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-egipto', 'Egipto', 3788, 'EGY', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA')]

    assert calcularPuntosTotalesEliminatorias(eliminatoria_real, eliminatoria_porra)==0

def test_calcular_puntos_totales_eliminatorias_eliminatoria_porra_sin_datos():

    eliminatoria_real=[('dieciseisavos', 'M73', 'republica-checa', 'República Checa', 6188, 'CZE', 'canada', 'Canadá', 5577, 'CAN', 'republica-checa', 'República Checa', 6188, 'CZE'), 
                        ('dieciseisavos', 'M74', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('dieciseisavos', 'M75', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-marruecos', 'Marruecos', 3780, 'MAR', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD'),
                        ('dieciseisavos', 'M76', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('dieciseisavos', 'M77', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-suecia', 'Suecia', 3074, 'SWE', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('dieciseisavos', 'M78', 'seleccion-ecuador', 'Ecuador', 3771, 'ECU', 'seleccion-noruega', 'Noruega', 3759, 'NOR', 'seleccion-noruega', 'Noruega', 3759, 'NOR'),
                        ('dieciseisavos', 'M79', 'seleccion-mexico', 'México', 3811, 'MEX', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-mexico', 'México', 3811, 'MEX'),
                        ('dieciseisavos', 'M80', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG', 'senegal', 'Senegal', 5658, 'SEN', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG'),
                        ('dieciseisavos', 'M81', 'seleccion-turquia', 'Turquía', 3737, 'TUR', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-turquia', 'Turquía', 3737, 'TUR'),
                        ('dieciseisavos', 'M82', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('dieciseisavos', 'M83', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'seleccion-colombia', 'Colombia', 3774, 'COL'),
                        ('dieciseisavos', 'M84', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-austria', 'Austria', 3767, 'AUT', 'seleccion-espanola', 'España', 3850, 'ESP'),
                        ('dieciseisavos', 'M85', 'seleccion-suiza', 'Suiza', 3723, 'CHE', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'seleccion-suiza', 'Suiza', 3723, 'CHE'),
                        ('dieciseisavos', 'M86', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-uruguay', 'Uruguay', 3768, 'URY', 'seleccion-argentina', 'Argentina', 3770, 'ARG'),
                        ('dieciseisavos', 'M87', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-ghana', 'Ghana', 3791, 'GHA', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('dieciseisavos', 'M88', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-egipto', 'Egipto', 3788, 'EGY', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA')]

    eliminatoria_porra=[]

    assert calcularPuntosTotalesEliminatorias(eliminatoria_real, eliminatoria_porra)==0

def test_calcular_puntos_totales_eliminatorias_porra_un_partido_ronda_real_una_ronda_porra():

    eliminatoria_real=[('dieciseisavos', 'M73', 'republica-checa', 'República Checa', 6188, 'CZE', 'canada', 'Canadá', 5577, 'CAN', 'republica-checa', 'República Checa', 6188, 'CZE')]

    eliminatoria_porra=[('dieciseisavos', 'M73', 'seleccion-mexico', 'México', 3811, 'MEX', 'canada', 'Canadá', 5577, 'CAN', 'seleccion-mexico', 'México', 3811, 'MEX'),
                        ('dieciseisavos', 'M74', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'haiti', 'Haití', 5582, 'HTI', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('dieciseisavos', 'M75', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-escocia', 'Escocia', 3758, 'SCO', 'seleccion-japon', 'Japón', 3798, 'JPN'),
                        ('dieciseisavos', 'M76', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('dieciseisavos', 'M77', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-suecia', 'Suecia', 3074, 'SWE', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('dieciseisavos', 'M78', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV', 'seleccion-iraq', 'Iraq', 3816, 'IRQ', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV'),
                        ('dieciseisavos', 'M79', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR'),
                        ('dieciseisavos', 'M80', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'curazao', 'Curazao', 61757, 'CUR', 'seleccion-croacia', 'Croacia', 3766, 'HRV'),
                        ('dieciseisavos', 'M81', 'seleccion-australia', 'Australia', 3801, 'AUS', 'seleccion-qatar', 'Catar', 3799, 'QAT', 'seleccion-australia', 'Australia', 3801, 'AUS'),
                        ('dieciseisavos', 'M82', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'republica-checa', 'República Checa', 6188, 'CZE', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('dieciseisavos', 'M83', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-ghana', 'Ghana', 3791, 'GHA', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('dieciseisavos', 'M84', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'),
                        ('dieciseisavos', 'M85', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-iran', 'Irán', 3806, 'IRN', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH'),
                        ('dieciseisavos', 'M86', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'cabo-verde', 'Cabo Verde', 9158, 'CPV', 'seleccion-argelia', 'Argelia', 3787, 'DZA'),
                        ('dieciseisavos', 'M87', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY'),
                        ('dieciseisavos', 'M88', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-egipto', 'Egipto', 3788, 'EGY', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA')]

    assert calcularPuntosTotalesEliminatorias(eliminatoria_real, eliminatoria_porra)==8

def test_calcular_puntos_totales_eliminatorias_porra_una_ronda_real_una_ronda_porra():

    eliminatoria_real=[('dieciseisavos', 'M73', 'republica-checa', 'República Checa', 6188, 'CZE', 'canada', 'Canadá', 5577, 'CAN', 'republica-checa', 'República Checa', 6188, 'CZE'), 
                        ('dieciseisavos', 'M74', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('dieciseisavos', 'M75', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-marruecos', 'Marruecos', 3780, 'MAR', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD'),
                        ('dieciseisavos', 'M76', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('dieciseisavos', 'M77', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-suecia', 'Suecia', 3074, 'SWE', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('dieciseisavos', 'M78', 'seleccion-ecuador', 'Ecuador', 3771, 'ECU', 'seleccion-noruega', 'Noruega', 3759, 'NOR', 'seleccion-noruega', 'Noruega', 3759, 'NOR'),
                        ('dieciseisavos', 'M79', 'seleccion-mexico', 'México', 3811, 'MEX', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-mexico', 'México', 3811, 'MEX'),
                        ('dieciseisavos', 'M80', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG', 'senegal', 'Senegal', 5658, 'SEN', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG'),
                        ('dieciseisavos', 'M81', 'seleccion-turquia', 'Turquía', 3737, 'TUR', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-turquia', 'Turquía', 3737, 'TUR'),
                        ('dieciseisavos', 'M82', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('dieciseisavos', 'M83', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'seleccion-colombia', 'Colombia', 3774, 'COL'),
                        ('dieciseisavos', 'M84', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-austria', 'Austria', 3767, 'AUT', 'seleccion-espanola', 'España', 3850, 'ESP'),
                        ('dieciseisavos', 'M85', 'seleccion-suiza', 'Suiza', 3723, 'CHE', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'seleccion-suiza', 'Suiza', 3723, 'CHE'),
                        ('dieciseisavos', 'M86', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-uruguay', 'Uruguay', 3768, 'URY', 'seleccion-argentina', 'Argentina', 3770, 'ARG'),
                        ('dieciseisavos', 'M87', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-ghana', 'Ghana', 3791, 'GHA', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('dieciseisavos', 'M88', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-egipto', 'Egipto', 3788, 'EGY', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA')]

    eliminatoria_porra=[('dieciseisavos', 'M73', 'seleccion-mexico', 'México', 3811, 'MEX', 'canada', 'Canadá', 5577, 'CAN', 'seleccion-mexico', 'México', 3811, 'MEX'),
                        ('dieciseisavos', 'M74', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'haiti', 'Haití', 5582, 'HTI', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('dieciseisavos', 'M75', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-escocia', 'Escocia', 3758, 'SCO', 'seleccion-japon', 'Japón', 3798, 'JPN'),
                        ('dieciseisavos', 'M76', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('dieciseisavos', 'M77', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-suecia', 'Suecia', 3074, 'SWE', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('dieciseisavos', 'M78', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV', 'seleccion-iraq', 'Iraq', 3816, 'IRQ', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV'),
                        ('dieciseisavos', 'M79', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR'),
                        ('dieciseisavos', 'M80', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'curazao', 'Curazao', 61757, 'CUR', 'seleccion-croacia', 'Croacia', 3766, 'HRV'),
                        ('dieciseisavos', 'M81', 'seleccion-australia', 'Australia', 3801, 'AUS', 'seleccion-qatar', 'Catar', 3799, 'QAT', 'seleccion-australia', 'Australia', 3801, 'AUS'),
                        ('dieciseisavos', 'M82', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'republica-checa', 'República Checa', 6188, 'CZE', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('dieciseisavos', 'M83', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-ghana', 'Ghana', 3791, 'GHA', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('dieciseisavos', 'M84', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'),
                        ('dieciseisavos', 'M85', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-iran', 'Irán', 3806, 'IRN', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH'),
                        ('dieciseisavos', 'M86', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'cabo-verde', 'Cabo Verde', 9158, 'CPV', 'seleccion-argelia', 'Argelia', 3787, 'DZA'),
                        ('dieciseisavos', 'M87', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY'),
                        ('dieciseisavos', 'M88', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-egipto', 'Egipto', 3788, 'EGY', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA')]

    assert calcularPuntosTotalesEliminatorias(eliminatoria_real, eliminatoria_porra)==92

def test_calcular_puntos_totales_eliminatorias_porra_una_ronda_real_dos_rondas_porra():

    eliminatoria_real=[('dieciseisavos', 'M73', 'republica-checa', 'República Checa', 6188, 'CZE', 'canada', 'Canadá', 5577, 'CAN', 'republica-checa', 'República Checa', 6188, 'CZE'), 
                        ('dieciseisavos', 'M74', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('dieciseisavos', 'M75', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-marruecos', 'Marruecos', 3780, 'MAR', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD'),
                        ('dieciseisavos', 'M76', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('dieciseisavos', 'M77', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-suecia', 'Suecia', 3074, 'SWE', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('dieciseisavos', 'M78', 'seleccion-ecuador', 'Ecuador', 3771, 'ECU', 'seleccion-noruega', 'Noruega', 3759, 'NOR', 'seleccion-noruega', 'Noruega', 3759, 'NOR'),
                        ('dieciseisavos', 'M79', 'seleccion-mexico', 'México', 3811, 'MEX', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-mexico', 'México', 3811, 'MEX'),
                        ('dieciseisavos', 'M80', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG', 'senegal', 'Senegal', 5658, 'SEN', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG'),
                        ('dieciseisavos', 'M81', 'seleccion-turquia', 'Turquía', 3737, 'TUR', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-turquia', 'Turquía', 3737, 'TUR'),
                        ('dieciseisavos', 'M82', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('dieciseisavos', 'M83', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'seleccion-colombia', 'Colombia', 3774, 'COL'),
                        ('dieciseisavos', 'M84', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-austria', 'Austria', 3767, 'AUT', 'seleccion-espanola', 'España', 3850, 'ESP'),
                        ('dieciseisavos', 'M85', 'seleccion-suiza', 'Suiza', 3723, 'CHE', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'seleccion-suiza', 'Suiza', 3723, 'CHE'),
                        ('dieciseisavos', 'M86', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-uruguay', 'Uruguay', 3768, 'URY', 'seleccion-argentina', 'Argentina', 3770, 'ARG'),
                        ('dieciseisavos', 'M87', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-ghana', 'Ghana', 3791, 'GHA', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('dieciseisavos', 'M88', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-egipto', 'Egipto', 3788, 'EGY', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA')]

    eliminatoria_porra=[('dieciseisavos', 'M73', 'seleccion-mexico', 'México', 3811, 'MEX', 'canada', 'Canadá', 5577, 'CAN', 'seleccion-mexico', 'México', 3811, 'MEX'),
                        ('dieciseisavos', 'M74', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'haiti', 'Haití', 5582, 'HTI', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('dieciseisavos', 'M75', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-escocia', 'Escocia', 3758, 'SCO', 'seleccion-japon', 'Japón', 3798, 'JPN'),
                        ('dieciseisavos', 'M76', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('dieciseisavos', 'M77', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-suecia', 'Suecia', 3074, 'SWE', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('dieciseisavos', 'M78', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV', 'seleccion-iraq', 'Iraq', 3816, 'IRQ', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV'),
                        ('dieciseisavos', 'M79', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR'),
                        ('dieciseisavos', 'M80', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'curazao', 'Curazao', 61757, 'CUR', 'seleccion-croacia', 'Croacia', 3766, 'HRV'),
                        ('dieciseisavos', 'M81', 'seleccion-australia', 'Australia', 3801, 'AUS', 'seleccion-qatar', 'Catar', 3799, 'QAT', 'seleccion-australia', 'Australia', 3801, 'AUS'),
                        ('dieciseisavos', 'M82', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'republica-checa', 'República Checa', 6188, 'CZE', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('dieciseisavos', 'M83', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-ghana', 'Ghana', 3791, 'GHA', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('dieciseisavos', 'M84', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'),
                        ('dieciseisavos', 'M85', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-iran', 'Irán', 3806, 'IRN', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH'),
                        ('dieciseisavos', 'M86', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'cabo-verde', 'Cabo Verde', 9158, 'CPV', 'seleccion-argelia', 'Argelia', 3787, 'DZA'),
                        ('dieciseisavos', 'M87', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY'),
                        ('dieciseisavos', 'M88', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-egipto', 'Egipto', 3788, 'EGY', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('octavos', 'M89', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('octavos', 'M90', 'seleccion-mexico', 'México', 3811, 'MEX', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-japon', 'Japón', 3798, 'JPN'),
                        ('octavos', 'M91', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV'),
                        ('octavos', 'M92', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR'),
                        ('octavos', 'M93', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'),
                        ('octavos', 'M94', 'seleccion-australia', 'Australia', 3801, 'AUS', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('octavos', 'M95', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('octavos', 'M96', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY')]

    assert calcularPuntosTotalesEliminatorias(eliminatoria_real, eliminatoria_porra)==92

def test_calcular_puntos_totales_eliminatorias_porra_un_partido_dos_rondas_real_dos_rondas_porra():

    eliminatoria_real=[('dieciseisavos', 'M73', 'republica-checa', 'República Checa', 6188, 'CZE', 'canada', 'Canadá', 5577, 'CAN', 'republica-checa', 'República Checa', 6188, 'CZE'), 
                        ('dieciseisavos', 'M74', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('dieciseisavos', 'M75', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-marruecos', 'Marruecos', 3780, 'MAR', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD'),
                        ('dieciseisavos', 'M76', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('dieciseisavos', 'M77', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-suecia', 'Suecia', 3074, 'SWE', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('dieciseisavos', 'M78', 'seleccion-ecuador', 'Ecuador', 3771, 'ECU', 'seleccion-noruega', 'Noruega', 3759, 'NOR', 'seleccion-noruega', 'Noruega', 3759, 'NOR'),
                        ('dieciseisavos', 'M79', 'seleccion-mexico', 'México', 3811, 'MEX', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-mexico', 'México', 3811, 'MEX'),
                        ('dieciseisavos', 'M80', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG', 'senegal', 'Senegal', 5658, 'SEN', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG'),
                        ('dieciseisavos', 'M81', 'seleccion-turquia', 'Turquía', 3737, 'TUR', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-turquia', 'Turquía', 3737, 'TUR'),
                        ('dieciseisavos', 'M82', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('dieciseisavos', 'M83', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'seleccion-colombia', 'Colombia', 3774, 'COL'),
                        ('dieciseisavos', 'M84', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-austria', 'Austria', 3767, 'AUT', 'seleccion-espanola', 'España', 3850, 'ESP'),
                        ('dieciseisavos', 'M85', 'seleccion-suiza', 'Suiza', 3723, 'CHE', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'seleccion-suiza', 'Suiza', 3723, 'CHE'),
                        ('dieciseisavos', 'M86', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-uruguay', 'Uruguay', 3768, 'URY', 'seleccion-argentina', 'Argentina', 3770, 'ARG'),
                        ('dieciseisavos', 'M87', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-ghana', 'Ghana', 3791, 'GHA', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('dieciseisavos', 'M88', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-egipto', 'Egipto', 3788, 'EGY', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('octavos', 'M89', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-alemania', 'Alemania', 3734, 'DEU')]

    eliminatoria_porra=[('dieciseisavos', 'M73', 'seleccion-mexico', 'México', 3811, 'MEX', 'canada', 'Canadá', 5577, 'CAN', 'seleccion-mexico', 'México', 3811, 'MEX'),
                        ('dieciseisavos', 'M74', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'haiti', 'Haití', 5582, 'HTI', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('dieciseisavos', 'M75', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-escocia', 'Escocia', 3758, 'SCO', 'seleccion-japon', 'Japón', 3798, 'JPN'),
                        ('dieciseisavos', 'M76', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('dieciseisavos', 'M77', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-suecia', 'Suecia', 3074, 'SWE', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('dieciseisavos', 'M78', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV', 'seleccion-iraq', 'Iraq', 3816, 'IRQ', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV'),
                        ('dieciseisavos', 'M79', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR'),
                        ('dieciseisavos', 'M80', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'curazao', 'Curazao', 61757, 'CUR', 'seleccion-croacia', 'Croacia', 3766, 'HRV'),
                        ('dieciseisavos', 'M81', 'seleccion-australia', 'Australia', 3801, 'AUS', 'seleccion-qatar', 'Catar', 3799, 'QAT', 'seleccion-australia', 'Australia', 3801, 'AUS'),
                        ('dieciseisavos', 'M82', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'republica-checa', 'República Checa', 6188, 'CZE', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('dieciseisavos', 'M83', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-ghana', 'Ghana', 3791, 'GHA', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('dieciseisavos', 'M84', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'),
                        ('dieciseisavos', 'M85', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-iran', 'Irán', 3806, 'IRN', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH'),
                        ('dieciseisavos', 'M86', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'cabo-verde', 'Cabo Verde', 9158, 'CPV', 'seleccion-argelia', 'Argelia', 3787, 'DZA'),
                        ('dieciseisavos', 'M87', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY'),
                        ('dieciseisavos', 'M88', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-egipto', 'Egipto', 3788, 'EGY', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('octavos', 'M89', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('octavos', 'M90', 'seleccion-mexico', 'México', 3811, 'MEX', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-japon', 'Japón', 3798, 'JPN'),
                        ('octavos', 'M91', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV'),
                        ('octavos', 'M92', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR'),
                        ('octavos', 'M93', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'),
                        ('octavos', 'M94', 'seleccion-australia', 'Australia', 3801, 'AUS', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('octavos', 'M95', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('octavos', 'M96', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY')]

    assert calcularPuntosTotalesEliminatorias(eliminatoria_real, eliminatoria_porra)==104

def test_calcular_puntos_totales_eliminatorias_porra_dos_rondas_real_dos_rondas_porra():

    eliminatoria_real=[('dieciseisavos', 'M73', 'republica-checa', 'República Checa', 6188, 'CZE', 'canada', 'Canadá', 5577, 'CAN', 'republica-checa', 'República Checa', 6188, 'CZE'), 
                        ('dieciseisavos', 'M74', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('dieciseisavos', 'M75', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-marruecos', 'Marruecos', 3780, 'MAR', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD'),
                        ('dieciseisavos', 'M76', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('dieciseisavos', 'M77', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-suecia', 'Suecia', 3074, 'SWE', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('dieciseisavos', 'M78', 'seleccion-ecuador', 'Ecuador', 3771, 'ECU', 'seleccion-noruega', 'Noruega', 3759, 'NOR', 'seleccion-noruega', 'Noruega', 3759, 'NOR'),
                        ('dieciseisavos', 'M79', 'seleccion-mexico', 'México', 3811, 'MEX', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-mexico', 'México', 3811, 'MEX'),
                        ('dieciseisavos', 'M80', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG', 'senegal', 'Senegal', 5658, 'SEN', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG'),
                        ('dieciseisavos', 'M81', 'seleccion-turquia', 'Turquía', 3737, 'TUR', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-turquia', 'Turquía', 3737, 'TUR'),
                        ('dieciseisavos', 'M82', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('dieciseisavos', 'M83', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'seleccion-colombia', 'Colombia', 3774, 'COL'),
                        ('dieciseisavos', 'M84', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-austria', 'Austria', 3767, 'AUT', 'seleccion-espanola', 'España', 3850, 'ESP'),
                        ('dieciseisavos', 'M85', 'seleccion-suiza', 'Suiza', 3723, 'CHE', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'seleccion-suiza', 'Suiza', 3723, 'CHE'),
                        ('dieciseisavos', 'M86', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-uruguay', 'Uruguay', 3768, 'URY', 'seleccion-argentina', 'Argentina', 3770, 'ARG'),
                        ('dieciseisavos', 'M87', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-ghana', 'Ghana', 3791, 'GHA', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('dieciseisavos', 'M88', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-egipto', 'Egipto', 3788, 'EGY', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('octavos', 'M89', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('octavos', 'M90', 'republica-checa', 'República Checa', 6188, 'CZE', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD'),
                        ('octavos', 'M91', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-noruega', 'Noruega', 3759, 'NOR', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('octavos', 'M92', 'seleccion-mexico', 'México', 3811, 'MEX', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG'),
                        ('octavos', 'M93', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-espanola', 'España', 3850, 'ESP'),
                        ('octavos', 'M94', 'seleccion-turquia', 'Turquía', 3737, 'TUR', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('octavos', 'M95', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-argentina', 'Argentina', 3770, 'ARG'),
                        ('octavos', 'M96', 'seleccion-suiza', 'Suiza', 3723, 'CHE', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-portugal', 'Portugal', 3762, 'PRT')]

    eliminatoria_porra=[('dieciseisavos', 'M73', 'seleccion-mexico', 'México', 3811, 'MEX', 'canada', 'Canadá', 5577, 'CAN', 'seleccion-mexico', 'México', 3811, 'MEX'),
                        ('dieciseisavos', 'M74', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'haiti', 'Haití', 5582, 'HTI', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('dieciseisavos', 'M75', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-escocia', 'Escocia', 3758, 'SCO', 'seleccion-japon', 'Japón', 3798, 'JPN'),
                        ('dieciseisavos', 'M76', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('dieciseisavos', 'M77', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-suecia', 'Suecia', 3074, 'SWE', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('dieciseisavos', 'M78', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV', 'seleccion-iraq', 'Iraq', 3816, 'IRQ', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV'),
                        ('dieciseisavos', 'M79', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR'),
                        ('dieciseisavos', 'M80', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'curazao', 'Curazao', 61757, 'CUR', 'seleccion-croacia', 'Croacia', 3766, 'HRV'),
                        ('dieciseisavos', 'M81', 'seleccion-australia', 'Australia', 3801, 'AUS', 'seleccion-qatar', 'Catar', 3799, 'QAT', 'seleccion-australia', 'Australia', 3801, 'AUS'),
                        ('dieciseisavos', 'M82', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'republica-checa', 'República Checa', 6188, 'CZE', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('dieciseisavos', 'M83', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-ghana', 'Ghana', 3791, 'GHA', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('dieciseisavos', 'M84', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'),
                        ('dieciseisavos', 'M85', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-iran', 'Irán', 3806, 'IRN', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH'),
                        ('dieciseisavos', 'M86', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'cabo-verde', 'Cabo Verde', 9158, 'CPV', 'seleccion-argelia', 'Argelia', 3787, 'DZA'),
                        ('dieciseisavos', 'M87', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY'),
                        ('dieciseisavos', 'M88', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-egipto', 'Egipto', 3788, 'EGY', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('octavos', 'M89', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('octavos', 'M90', 'seleccion-mexico', 'México', 3811, 'MEX', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-japon', 'Japón', 3798, 'JPN'),
                        ('octavos', 'M91', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV'),
                        ('octavos', 'M92', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR'),
                        ('octavos', 'M93', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'),
                        ('octavos', 'M94', 'seleccion-australia', 'Australia', 3801, 'AUS', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('octavos', 'M95', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('octavos', 'M96', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY')]

    assert calcularPuntosTotalesEliminatorias(eliminatoria_real, eliminatoria_porra)==134

def test_calcular_puntos_totales_eliminatorias_porra_todos():

    eliminatoria_real=[('dieciseisavos', 'M73', 'republica-checa', 'República Checa', 6188, 'CZE', 'canada', 'Canadá', 5577, 'CAN', 'republica-checa', 'República Checa', 6188, 'CZE'), 
                        ('dieciseisavos', 'M74', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('dieciseisavos', 'M75', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-marruecos', 'Marruecos', 3780, 'MAR', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD'),
                        ('dieciseisavos', 'M76', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('dieciseisavos', 'M77', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-suecia', 'Suecia', 3074, 'SWE', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('dieciseisavos', 'M78', 'seleccion-ecuador', 'Ecuador', 3771, 'ECU', 'seleccion-noruega', 'Noruega', 3759, 'NOR', 'seleccion-noruega', 'Noruega', 3759, 'NOR'),
                        ('dieciseisavos', 'M79', 'seleccion-mexico', 'México', 3811, 'MEX', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-mexico', 'México', 3811, 'MEX'),
                        ('dieciseisavos', 'M80', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG', 'senegal', 'Senegal', 5658, 'SEN', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG'),
                        ('dieciseisavos', 'M81', 'seleccion-turquia', 'Turquía', 3737, 'TUR', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-turquia', 'Turquía', 3737, 'TUR'),
                        ('dieciseisavos', 'M82', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('dieciseisavos', 'M83', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'seleccion-colombia', 'Colombia', 3774, 'COL'),
                        ('dieciseisavos', 'M84', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-austria', 'Austria', 3767, 'AUT', 'seleccion-espanola', 'España', 3850, 'ESP'),
                        ('dieciseisavos', 'M85', 'seleccion-suiza', 'Suiza', 3723, 'CHE', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'seleccion-suiza', 'Suiza', 3723, 'CHE'),
                        ('dieciseisavos', 'M86', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-uruguay', 'Uruguay', 3768, 'URY', 'seleccion-argentina', 'Argentina', 3770, 'ARG'),
                        ('dieciseisavos', 'M87', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-ghana', 'Ghana', 3791, 'GHA', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('dieciseisavos', 'M88', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-egipto', 'Egipto', 3788, 'EGY', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('octavos', 'M89', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('octavos', 'M90', 'republica-checa', 'República Checa', 6188, 'CZE', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD'),
                        ('octavos', 'M91', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-noruega', 'Noruega', 3759, 'NOR', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('octavos', 'M92', 'seleccion-mexico', 'México', 3811, 'MEX', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG'),
                        ('octavos', 'M93', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-espanola', 'España', 3850, 'ESP'),
                        ('octavos', 'M94', 'seleccion-turquia', 'Turquía', 3737, 'TUR', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('octavos', 'M95', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-argentina', 'Argentina', 3770, 'ARG'),
                        ('octavos', 'M96', 'seleccion-suiza', 'Suiza', 3723, 'CHE', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('cuartos', 'M97', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('cuartos', 'M98', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-espanola', 'España', 3850, 'ESP'),
                        ('cuartos', 'M99', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('cuartos', 'M100', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-argentina', 'Argentina', 3770, 'ARG'),
                        ('semifinales', 'M101', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-espanola', 'España', 3850, 'ESP'),
                        ('semifinales', 'M102', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-argentina', 'Argentina', 3770, 'ARG'),
                        ('tercer_puesto', 'M103', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('final', 'M104', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-espanola', 'España', 3850, 'ESP')]

    eliminatoria_porra=[('dieciseisavos', 'M73', 'seleccion-mexico', 'México', 3811, 'MEX', 'canada', 'Canadá', 5577, 'CAN', 'seleccion-mexico', 'México', 3811, 'MEX'),
                        ('dieciseisavos', 'M74', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'haiti', 'Haití', 5582, 'HTI', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('dieciseisavos', 'M75', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-escocia', 'Escocia', 3758, 'SCO', 'seleccion-japon', 'Japón', 3798, 'JPN'),
                        ('dieciseisavos', 'M76', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('dieciseisavos', 'M77', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-suecia', 'Suecia', 3074, 'SWE', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('dieciseisavos', 'M78', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV', 'seleccion-iraq', 'Iraq', 3816, 'IRQ', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV'),
                        ('dieciseisavos', 'M79', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR'),
                        ('dieciseisavos', 'M80', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'curazao', 'Curazao', 61757, 'CUR', 'seleccion-croacia', 'Croacia', 3766, 'HRV'),
                        ('dieciseisavos', 'M81', 'seleccion-australia', 'Australia', 3801, 'AUS', 'seleccion-qatar', 'Catar', 3799, 'QAT', 'seleccion-australia', 'Australia', 3801, 'AUS'),
                        ('dieciseisavos', 'M82', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'republica-checa', 'República Checa', 6188, 'CZE', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('dieciseisavos', 'M83', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-ghana', 'Ghana', 3791, 'GHA', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('dieciseisavos', 'M84', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'),
                        ('dieciseisavos', 'M85', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-iran', 'Irán', 3806, 'IRN', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH'),
                        ('dieciseisavos', 'M86', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'cabo-verde', 'Cabo Verde', 9158, 'CPV', 'seleccion-argelia', 'Argelia', 3787, 'DZA'),
                        ('dieciseisavos', 'M87', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY'),
                        ('dieciseisavos', 'M88', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-egipto', 'Egipto', 3788, 'EGY', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('octavos', 'M89', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('octavos', 'M90', 'seleccion-mexico', 'México', 3811, 'MEX', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-japon', 'Japón', 3798, 'JPN'),
                        ('octavos', 'M91', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV'),
                        ('octavos', 'M92', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR'),
                        ('octavos', 'M93', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'),
                        ('octavos', 'M94', 'seleccion-australia', 'Australia', 3801, 'AUS', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('octavos', 'M95', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('octavos', 'M96', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY'),
                        ('cuartos', 'M97', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('cuartos', 'M98', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'),
                        ('cuartos', 'M99', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR'),
                        ('cuartos', 'M100', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('semifinales', 'M101', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'),
                        ('semifinales', 'M102', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('tercer_puesto', 'M103', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('final', 'M104', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU')]

    assert calcularPuntosTotalesEliminatorias(eliminatoria_real, eliminatoria_porra)==144

def test_obtener_final_eliminatoria_sin_datos():

    eliminatoria=[]
   
    assert not obtenerFinalEliminatoria(eliminatoria)

def test_obtener_final_eliminatoria_sin_final():

    eliminatoria=[('dieciseisavos', 'M73', 'republica-checa', 'República Checa', 6188, 'CZE', 'canada', 'Canadá', 5577, 'CAN', 'republica-checa', 'República Checa', 6188, 'CZE'), 
                        ('dieciseisavos', 'M74', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('dieciseisavos', 'M75', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-marruecos', 'Marruecos', 3780, 'MAR', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD'),
                        ('dieciseisavos', 'M76', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('dieciseisavos', 'M77', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-suecia', 'Suecia', 3074, 'SWE', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('dieciseisavos', 'M78', 'seleccion-ecuador', 'Ecuador', 3771, 'ECU', 'seleccion-noruega', 'Noruega', 3759, 'NOR', 'seleccion-noruega', 'Noruega', 3759, 'NOR'),
                        ('dieciseisavos', 'M79', 'seleccion-mexico', 'México', 3811, 'MEX', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-mexico', 'México', 3811, 'MEX'),
                        ('dieciseisavos', 'M80', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG', 'senegal', 'Senegal', 5658, 'SEN', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG'),
                        ('dieciseisavos', 'M81', 'seleccion-turquia', 'Turquía', 3737, 'TUR', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-turquia', 'Turquía', 3737, 'TUR'),
                        ('dieciseisavos', 'M82', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('dieciseisavos', 'M83', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'seleccion-colombia', 'Colombia', 3774, 'COL'),
                        ('dieciseisavos', 'M84', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-austria', 'Austria', 3767, 'AUT', 'seleccion-espanola', 'España', 3850, 'ESP'),
                        ('dieciseisavos', 'M85', 'seleccion-suiza', 'Suiza', 3723, 'CHE', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'seleccion-suiza', 'Suiza', 3723, 'CHE'),
                        ('dieciseisavos', 'M86', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-uruguay', 'Uruguay', 3768, 'URY', 'seleccion-argentina', 'Argentina', 3770, 'ARG'),
                        ('dieciseisavos', 'M87', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-ghana', 'Ghana', 3791, 'GHA', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('dieciseisavos', 'M88', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-egipto', 'Egipto', 3788, 'EGY', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('octavos', 'M89', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('octavos', 'M90', 'republica-checa', 'República Checa', 6188, 'CZE', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD'),
                        ('octavos', 'M91', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-noruega', 'Noruega', 3759, 'NOR', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('octavos', 'M92', 'seleccion-mexico', 'México', 3811, 'MEX', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG'),
                        ('octavos', 'M93', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-espanola', 'España', 3850, 'ESP'),
                        ('octavos', 'M94', 'seleccion-turquia', 'Turquía', 3737, 'TUR', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('octavos', 'M95', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-argentina', 'Argentina', 3770, 'ARG'),
                        ('octavos', 'M96', 'seleccion-suiza', 'Suiza', 3723, 'CHE', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('cuartos', 'M97', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('cuartos', 'M98', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-espanola', 'España', 3850, 'ESP'),
                        ('cuartos', 'M99', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('cuartos', 'M100', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-argentina', 'Argentina', 3770, 'ARG')]
   
    assert not obtenerFinalEliminatoria(eliminatoria)

def test_obtener_final_eliminatoria():

    eliminatoria=[('dieciseisavos', 'M73', 'republica-checa', 'República Checa', 6188, 'CZE', 'canada', 'Canadá', 5577, 'CAN', 'republica-checa', 'República Checa', 6188, 'CZE'), 
                        ('dieciseisavos', 'M74', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('dieciseisavos', 'M75', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-marruecos', 'Marruecos', 3780, 'MAR', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD'),
                        ('dieciseisavos', 'M76', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('dieciseisavos', 'M77', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-suecia', 'Suecia', 3074, 'SWE', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('dieciseisavos', 'M78', 'seleccion-ecuador', 'Ecuador', 3771, 'ECU', 'seleccion-noruega', 'Noruega', 3759, 'NOR', 'seleccion-noruega', 'Noruega', 3759, 'NOR'),
                        ('dieciseisavos', 'M79', 'seleccion-mexico', 'México', 3811, 'MEX', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-mexico', 'México', 3811, 'MEX'),
                        ('dieciseisavos', 'M80', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG', 'senegal', 'Senegal', 5658, 'SEN', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG'),
                        ('dieciseisavos', 'M81', 'seleccion-turquia', 'Turquía', 3737, 'TUR', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-turquia', 'Turquía', 3737, 'TUR'),
                        ('dieciseisavos', 'M82', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('dieciseisavos', 'M83', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'seleccion-colombia', 'Colombia', 3774, 'COL'),
                        ('dieciseisavos', 'M84', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-austria', 'Austria', 3767, 'AUT', 'seleccion-espanola', 'España', 3850, 'ESP'),
                        ('dieciseisavos', 'M85', 'seleccion-suiza', 'Suiza', 3723, 'CHE', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'seleccion-suiza', 'Suiza', 3723, 'CHE'),
                        ('dieciseisavos', 'M86', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-uruguay', 'Uruguay', 3768, 'URY', 'seleccion-argentina', 'Argentina', 3770, 'ARG'),
                        ('dieciseisavos', 'M87', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-ghana', 'Ghana', 3791, 'GHA', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('dieciseisavos', 'M88', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-egipto', 'Egipto', 3788, 'EGY', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('octavos', 'M89', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('octavos', 'M90', 'republica-checa', 'República Checa', 6188, 'CZE', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD'),
                        ('octavos', 'M91', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-noruega', 'Noruega', 3759, 'NOR', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('octavos', 'M92', 'seleccion-mexico', 'México', 3811, 'MEX', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG'),
                        ('octavos', 'M93', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-espanola', 'España', 3850, 'ESP'),
                        ('octavos', 'M94', 'seleccion-turquia', 'Turquía', 3737, 'TUR', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('octavos', 'M95', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-argentina', 'Argentina', 3770, 'ARG'),
                        ('octavos', 'M96', 'seleccion-suiza', 'Suiza', 3723, 'CHE', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('cuartos', 'M97', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('cuartos', 'M98', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-espanola', 'España', 3850, 'ESP'),
                        ('cuartos', 'M99', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('cuartos', 'M100', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-argentina', 'Argentina', 3770, 'ARG'),
                        ('semifinales', 'M101', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-espanola', 'España', 3850, 'ESP'),
                        ('semifinales', 'M102', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-argentina', 'Argentina', 3770, 'ARG'),
                        ('tercer_puesto', 'M103', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('final', 'M104', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-espanola', 'España', 3850, 'ESP')]

    assert obtenerFinalEliminatoria(eliminatoria)

def test_calcular_bonus_campeon_eliminatorias_real_sin_datos():

    eliminatoria_real=[]

    eliminatoria_porra=[('dieciseisavos', 'M73', 'seleccion-mexico', 'México', 3811, 'MEX', 'canada', 'Canadá', 5577, 'CAN', 'seleccion-mexico', 'México', 3811, 'MEX'),
                        ('dieciseisavos', 'M74', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'haiti', 'Haití', 5582, 'HTI', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('dieciseisavos', 'M75', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-escocia', 'Escocia', 3758, 'SCO', 'seleccion-japon', 'Japón', 3798, 'JPN'),
                        ('dieciseisavos', 'M76', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('dieciseisavos', 'M77', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-suecia', 'Suecia', 3074, 'SWE', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('dieciseisavos', 'M78', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV', 'seleccion-iraq', 'Iraq', 3816, 'IRQ', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV'),
                        ('dieciseisavos', 'M79', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR'),
                        ('dieciseisavos', 'M80', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'curazao', 'Curazao', 61757, 'CUR', 'seleccion-croacia', 'Croacia', 3766, 'HRV'),
                        ('dieciseisavos', 'M81', 'seleccion-australia', 'Australia', 3801, 'AUS', 'seleccion-qatar', 'Catar', 3799, 'QAT', 'seleccion-australia', 'Australia', 3801, 'AUS'),
                        ('dieciseisavos', 'M82', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'republica-checa', 'República Checa', 6188, 'CZE', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('dieciseisavos', 'M83', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-ghana', 'Ghana', 3791, 'GHA', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('dieciseisavos', 'M84', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'),
                        ('dieciseisavos', 'M85', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-iran', 'Irán', 3806, 'IRN', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH'),
                        ('dieciseisavos', 'M86', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'cabo-verde', 'Cabo Verde', 9158, 'CPV', 'seleccion-argelia', 'Argelia', 3787, 'DZA'),
                        ('dieciseisavos', 'M87', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY'),
                        ('dieciseisavos', 'M88', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-egipto', 'Egipto', 3788, 'EGY', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('octavos', 'M89', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('octavos', 'M90', 'seleccion-mexico', 'México', 3811, 'MEX', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-japon', 'Japón', 3798, 'JPN'),
                        ('octavos', 'M91', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV'),
                        ('octavos', 'M92', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR'),
                        ('octavos', 'M93', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'),
                        ('octavos', 'M94', 'seleccion-australia', 'Australia', 3801, 'AUS', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('octavos', 'M95', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('octavos', 'M96', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY'),
                        ('cuartos', 'M97', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('cuartos', 'M98', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'),
                        ('cuartos', 'M99', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR'),
                        ('cuartos', 'M100', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('semifinales', 'M101', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'),
                        ('semifinales', 'M102', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('tercer_puesto', 'M103', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('final', 'M104', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU')]

    assert calcularBonusCampeonEliminatorias(eliminatoria_real, eliminatoria_porra)==0

def test_calcular_bonus_campeon_eliminatorias_porra_sin_datos():

    eliminatoria_real=[('dieciseisavos', 'M73', 'republica-checa', 'República Checa', 6188, 'CZE', 'canada', 'Canadá', 5577, 'CAN', 'republica-checa', 'República Checa', 6188, 'CZE'), 
                        ('dieciseisavos', 'M74', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('dieciseisavos', 'M75', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-marruecos', 'Marruecos', 3780, 'MAR', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD'),
                        ('dieciseisavos', 'M76', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('dieciseisavos', 'M77', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-suecia', 'Suecia', 3074, 'SWE', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('dieciseisavos', 'M78', 'seleccion-ecuador', 'Ecuador', 3771, 'ECU', 'seleccion-noruega', 'Noruega', 3759, 'NOR', 'seleccion-noruega', 'Noruega', 3759, 'NOR'),
                        ('dieciseisavos', 'M79', 'seleccion-mexico', 'México', 3811, 'MEX', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-mexico', 'México', 3811, 'MEX'),
                        ('dieciseisavos', 'M80', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG', 'senegal', 'Senegal', 5658, 'SEN', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG'),
                        ('dieciseisavos', 'M81', 'seleccion-turquia', 'Turquía', 3737, 'TUR', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-turquia', 'Turquía', 3737, 'TUR'),
                        ('dieciseisavos', 'M82', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('dieciseisavos', 'M83', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'seleccion-colombia', 'Colombia', 3774, 'COL'),
                        ('dieciseisavos', 'M84', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-austria', 'Austria', 3767, 'AUT', 'seleccion-espanola', 'España', 3850, 'ESP'),
                        ('dieciseisavos', 'M85', 'seleccion-suiza', 'Suiza', 3723, 'CHE', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'seleccion-suiza', 'Suiza', 3723, 'CHE'),
                        ('dieciseisavos', 'M86', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-uruguay', 'Uruguay', 3768, 'URY', 'seleccion-argentina', 'Argentina', 3770, 'ARG'),
                        ('dieciseisavos', 'M87', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-ghana', 'Ghana', 3791, 'GHA', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('dieciseisavos', 'M88', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-egipto', 'Egipto', 3788, 'EGY', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('octavos', 'M89', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('octavos', 'M90', 'republica-checa', 'República Checa', 6188, 'CZE', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD'),
                        ('octavos', 'M91', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-noruega', 'Noruega', 3759, 'NOR', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('octavos', 'M92', 'seleccion-mexico', 'México', 3811, 'MEX', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG'),
                        ('octavos', 'M93', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-espanola', 'España', 3850, 'ESP'),
                        ('octavos', 'M94', 'seleccion-turquia', 'Turquía', 3737, 'TUR', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('octavos', 'M95', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-argentina', 'Argentina', 3770, 'ARG'),
                        ('octavos', 'M96', 'seleccion-suiza', 'Suiza', 3723, 'CHE', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('cuartos', 'M97', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('cuartos', 'M98', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-espanola', 'España', 3850, 'ESP'),
                        ('cuartos', 'M99', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('cuartos', 'M100', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-argentina', 'Argentina', 3770, 'ARG'),
                        ('semifinales', 'M101', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-espanola', 'España', 3850, 'ESP'),
                        ('semifinales', 'M102', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-argentina', 'Argentina', 3770, 'ARG'),
                        ('tercer_puesto', 'M103', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('final', 'M104', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-espanola', 'España', 3850, 'ESP')]

    eliminatoria_porra=[]

    assert calcularBonusCampeonEliminatorias(eliminatoria_real, eliminatoria_porra)==0

def test_calcular_bonus_campeon_eliminatorias_reaL_sin_final():

    eliminatoria_real=[('dieciseisavos', 'M73', 'republica-checa', 'República Checa', 6188, 'CZE', 'canada', 'Canadá', 5577, 'CAN', 'republica-checa', 'República Checa', 6188, 'CZE'), 
                        ('dieciseisavos', 'M74', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('dieciseisavos', 'M75', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-marruecos', 'Marruecos', 3780, 'MAR', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD'),
                        ('dieciseisavos', 'M76', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('dieciseisavos', 'M77', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-suecia', 'Suecia', 3074, 'SWE', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('dieciseisavos', 'M78', 'seleccion-ecuador', 'Ecuador', 3771, 'ECU', 'seleccion-noruega', 'Noruega', 3759, 'NOR', 'seleccion-noruega', 'Noruega', 3759, 'NOR'),
                        ('dieciseisavos', 'M79', 'seleccion-mexico', 'México', 3811, 'MEX', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-mexico', 'México', 3811, 'MEX'),
                        ('dieciseisavos', 'M80', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG', 'senegal', 'Senegal', 5658, 'SEN', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG'),
                        ('dieciseisavos', 'M81', 'seleccion-turquia', 'Turquía', 3737, 'TUR', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-turquia', 'Turquía', 3737, 'TUR'),
                        ('dieciseisavos', 'M82', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('dieciseisavos', 'M83', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'seleccion-colombia', 'Colombia', 3774, 'COL'),
                        ('dieciseisavos', 'M84', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-austria', 'Austria', 3767, 'AUT', 'seleccion-espanola', 'España', 3850, 'ESP'),
                        ('dieciseisavos', 'M85', 'seleccion-suiza', 'Suiza', 3723, 'CHE', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'seleccion-suiza', 'Suiza', 3723, 'CHE'),
                        ('dieciseisavos', 'M86', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-uruguay', 'Uruguay', 3768, 'URY', 'seleccion-argentina', 'Argentina', 3770, 'ARG'),
                        ('dieciseisavos', 'M87', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-ghana', 'Ghana', 3791, 'GHA', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('dieciseisavos', 'M88', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-egipto', 'Egipto', 3788, 'EGY', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('octavos', 'M89', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('octavos', 'M90', 'republica-checa', 'República Checa', 6188, 'CZE', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD'),
                        ('octavos', 'M91', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-noruega', 'Noruega', 3759, 'NOR', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('octavos', 'M92', 'seleccion-mexico', 'México', 3811, 'MEX', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG'),
                        ('octavos', 'M93', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-espanola', 'España', 3850, 'ESP'),
                        ('octavos', 'M94', 'seleccion-turquia', 'Turquía', 3737, 'TUR', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('octavos', 'M95', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-argentina', 'Argentina', 3770, 'ARG'),
                        ('octavos', 'M96', 'seleccion-suiza', 'Suiza', 3723, 'CHE', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('cuartos', 'M97', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('cuartos', 'M98', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-espanola', 'España', 3850, 'ESP'),
                        ('cuartos', 'M99', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('cuartos', 'M100', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-argentina', 'Argentina', 3770, 'ARG'),
                        ('semifinales', 'M101', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-espanola', 'España', 3850, 'ESP'),
                        ('semifinales', 'M102', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-argentina', 'Argentina', 3770, 'ARG'),
                        ('tercer_puesto', 'M103', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-francia', 'Francia', 3750, 'FRA')]

    eliminatoria_porra=[('dieciseisavos', 'M73', 'seleccion-mexico', 'México', 3811, 'MEX', 'canada', 'Canadá', 5577, 'CAN', 'seleccion-mexico', 'México', 3811, 'MEX'),
                        ('dieciseisavos', 'M74', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'haiti', 'Haití', 5582, 'HTI', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('dieciseisavos', 'M75', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-escocia', 'Escocia', 3758, 'SCO', 'seleccion-japon', 'Japón', 3798, 'JPN'),
                        ('dieciseisavos', 'M76', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('dieciseisavos', 'M77', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-suecia', 'Suecia', 3074, 'SWE', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('dieciseisavos', 'M78', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV', 'seleccion-iraq', 'Iraq', 3816, 'IRQ', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV'),
                        ('dieciseisavos', 'M79', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR'),
                        ('dieciseisavos', 'M80', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'curazao', 'Curazao', 61757, 'CUR', 'seleccion-croacia', 'Croacia', 3766, 'HRV'),
                        ('dieciseisavos', 'M81', 'seleccion-australia', 'Australia', 3801, 'AUS', 'seleccion-qatar', 'Catar', 3799, 'QAT', 'seleccion-australia', 'Australia', 3801, 'AUS'),
                        ('dieciseisavos', 'M82', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'republica-checa', 'República Checa', 6188, 'CZE', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('dieciseisavos', 'M83', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-ghana', 'Ghana', 3791, 'GHA', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('dieciseisavos', 'M84', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'),
                        ('dieciseisavos', 'M85', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-iran', 'Irán', 3806, 'IRN', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH'),
                        ('dieciseisavos', 'M86', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'cabo-verde', 'Cabo Verde', 9158, 'CPV', 'seleccion-argelia', 'Argelia', 3787, 'DZA'),
                        ('dieciseisavos', 'M87', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY'),
                        ('dieciseisavos', 'M88', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-egipto', 'Egipto', 3788, 'EGY', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('octavos', 'M89', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('octavos', 'M90', 'seleccion-mexico', 'México', 3811, 'MEX', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-japon', 'Japón', 3798, 'JPN'),
                        ('octavos', 'M91', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV'),
                        ('octavos', 'M92', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR'),
                        ('octavos', 'M93', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'),
                        ('octavos', 'M94', 'seleccion-australia', 'Australia', 3801, 'AUS', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('octavos', 'M95', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('octavos', 'M96', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY'),
                        ('cuartos', 'M97', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('cuartos', 'M98', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'),
                        ('cuartos', 'M99', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR'),
                        ('cuartos', 'M100', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('semifinales', 'M101', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'),
                        ('semifinales', 'M102', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('tercer_puesto', 'M103', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('final', 'M104', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU')]

    assert calcularBonusCampeonEliminatorias(eliminatoria_real, eliminatoria_porra)==0

def test_calcular_bonus_campeon_eliminatorias_campeon_erroneo():

    eliminatoria_real=[('dieciseisavos', 'M73', 'republica-checa', 'República Checa', 6188, 'CZE', 'canada', 'Canadá', 5577, 'CAN', 'republica-checa', 'República Checa', 6188, 'CZE'), 
                        ('dieciseisavos', 'M74', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('dieciseisavos', 'M75', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-marruecos', 'Marruecos', 3780, 'MAR', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD'),
                        ('dieciseisavos', 'M76', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('dieciseisavos', 'M77', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-suecia', 'Suecia', 3074, 'SWE', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('dieciseisavos', 'M78', 'seleccion-ecuador', 'Ecuador', 3771, 'ECU', 'seleccion-noruega', 'Noruega', 3759, 'NOR', 'seleccion-noruega', 'Noruega', 3759, 'NOR'),
                        ('dieciseisavos', 'M79', 'seleccion-mexico', 'México', 3811, 'MEX', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-mexico', 'México', 3811, 'MEX'),
                        ('dieciseisavos', 'M80', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG', 'senegal', 'Senegal', 5658, 'SEN', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG'),
                        ('dieciseisavos', 'M81', 'seleccion-turquia', 'Turquía', 3737, 'TUR', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-turquia', 'Turquía', 3737, 'TUR'),
                        ('dieciseisavos', 'M82', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('dieciseisavos', 'M83', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'seleccion-colombia', 'Colombia', 3774, 'COL'),
                        ('dieciseisavos', 'M84', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-austria', 'Austria', 3767, 'AUT', 'seleccion-espanola', 'España', 3850, 'ESP'),
                        ('dieciseisavos', 'M85', 'seleccion-suiza', 'Suiza', 3723, 'CHE', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'seleccion-suiza', 'Suiza', 3723, 'CHE'),
                        ('dieciseisavos', 'M86', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-uruguay', 'Uruguay', 3768, 'URY', 'seleccion-argentina', 'Argentina', 3770, 'ARG'),
                        ('dieciseisavos', 'M87', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-ghana', 'Ghana', 3791, 'GHA', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('dieciseisavos', 'M88', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-egipto', 'Egipto', 3788, 'EGY', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('octavos', 'M89', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('octavos', 'M90', 'republica-checa', 'República Checa', 6188, 'CZE', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD'),
                        ('octavos', 'M91', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-noruega', 'Noruega', 3759, 'NOR', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('octavos', 'M92', 'seleccion-mexico', 'México', 3811, 'MEX', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG'),
                        ('octavos', 'M93', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-espanola', 'España', 3850, 'ESP'),
                        ('octavos', 'M94', 'seleccion-turquia', 'Turquía', 3737, 'TUR', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('octavos', 'M95', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-argentina', 'Argentina', 3770, 'ARG'),
                        ('octavos', 'M96', 'seleccion-suiza', 'Suiza', 3723, 'CHE', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('cuartos', 'M97', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('cuartos', 'M98', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-espanola', 'España', 3850, 'ESP'),
                        ('cuartos', 'M99', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('cuartos', 'M100', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-argentina', 'Argentina', 3770, 'ARG'),
                        ('semifinales', 'M101', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-espanola', 'España', 3850, 'ESP'),
                        ('semifinales', 'M102', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-argentina', 'Argentina', 3770, 'ARG'),
                        ('tercer_puesto', 'M103', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('final', 'M104', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-espanola', 'España', 3850, 'ESP')]

    eliminatoria_porra=[('dieciseisavos', 'M73', 'seleccion-mexico', 'México', 3811, 'MEX', 'canada', 'Canadá', 5577, 'CAN', 'seleccion-mexico', 'México', 3811, 'MEX'),
                        ('dieciseisavos', 'M74', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'haiti', 'Haití', 5582, 'HTI', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('dieciseisavos', 'M75', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-escocia', 'Escocia', 3758, 'SCO', 'seleccion-japon', 'Japón', 3798, 'JPN'),
                        ('dieciseisavos', 'M76', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('dieciseisavos', 'M77', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-suecia', 'Suecia', 3074, 'SWE', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('dieciseisavos', 'M78', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV', 'seleccion-iraq', 'Iraq', 3816, 'IRQ', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV'),
                        ('dieciseisavos', 'M79', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR'),
                        ('dieciseisavos', 'M80', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'curazao', 'Curazao', 61757, 'CUR', 'seleccion-croacia', 'Croacia', 3766, 'HRV'),
                        ('dieciseisavos', 'M81', 'seleccion-australia', 'Australia', 3801, 'AUS', 'seleccion-qatar', 'Catar', 3799, 'QAT', 'seleccion-australia', 'Australia', 3801, 'AUS'),
                        ('dieciseisavos', 'M82', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'republica-checa', 'República Checa', 6188, 'CZE', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('dieciseisavos', 'M83', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-ghana', 'Ghana', 3791, 'GHA', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('dieciseisavos', 'M84', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'),
                        ('dieciseisavos', 'M85', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-iran', 'Irán', 3806, 'IRN', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH'),
                        ('dieciseisavos', 'M86', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'cabo-verde', 'Cabo Verde', 9158, 'CPV', 'seleccion-argelia', 'Argelia', 3787, 'DZA'),
                        ('dieciseisavos', 'M87', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY'),
                        ('dieciseisavos', 'M88', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-egipto', 'Egipto', 3788, 'EGY', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('octavos', 'M89', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('octavos', 'M90', 'seleccion-mexico', 'México', 3811, 'MEX', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-japon', 'Japón', 3798, 'JPN'),
                        ('octavos', 'M91', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV'),
                        ('octavos', 'M92', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR'),
                        ('octavos', 'M93', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'),
                        ('octavos', 'M94', 'seleccion-australia', 'Australia', 3801, 'AUS', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('octavos', 'M95', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('octavos', 'M96', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY'),
                        ('cuartos', 'M97', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('cuartos', 'M98', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'),
                        ('cuartos', 'M99', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR'),
                        ('cuartos', 'M100', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('semifinales', 'M101', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'),
                        ('semifinales', 'M102', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('tercer_puesto', 'M103', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('final', 'M104', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU')]

    assert calcularBonusCampeonEliminatorias(eliminatoria_real, eliminatoria_porra)==0

def test_calcular_bonus_campeon_eliminatorias_campeon_acertado():

    eliminatoria_real=[('dieciseisavos', 'M73', 'republica-checa', 'República Checa', 6188, 'CZE', 'canada', 'Canadá', 5577, 'CAN', 'republica-checa', 'República Checa', 6188, 'CZE'), 
                        ('dieciseisavos', 'M74', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('dieciseisavos', 'M75', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-marruecos', 'Marruecos', 3780, 'MAR', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD'),
                        ('dieciseisavos', 'M76', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('dieciseisavos', 'M77', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-suecia', 'Suecia', 3074, 'SWE', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('dieciseisavos', 'M78', 'seleccion-ecuador', 'Ecuador', 3771, 'ECU', 'seleccion-noruega', 'Noruega', 3759, 'NOR', 'seleccion-noruega', 'Noruega', 3759, 'NOR'),
                        ('dieciseisavos', 'M79', 'seleccion-mexico', 'México', 3811, 'MEX', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-mexico', 'México', 3811, 'MEX'),
                        ('dieciseisavos', 'M80', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG', 'senegal', 'Senegal', 5658, 'SEN', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG'),
                        ('dieciseisavos', 'M81', 'seleccion-turquia', 'Turquía', 3737, 'TUR', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-turquia', 'Turquía', 3737, 'TUR'),
                        ('dieciseisavos', 'M82', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('dieciseisavos', 'M83', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'seleccion-colombia', 'Colombia', 3774, 'COL'),
                        ('dieciseisavos', 'M84', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-austria', 'Austria', 3767, 'AUT', 'seleccion-espanola', 'España', 3850, 'ESP'),
                        ('dieciseisavos', 'M85', 'seleccion-suiza', 'Suiza', 3723, 'CHE', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'seleccion-suiza', 'Suiza', 3723, 'CHE'),
                        ('dieciseisavos', 'M86', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-uruguay', 'Uruguay', 3768, 'URY', 'seleccion-argentina', 'Argentina', 3770, 'ARG'),
                        ('dieciseisavos', 'M87', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-ghana', 'Ghana', 3791, 'GHA', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('dieciseisavos', 'M88', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-egipto', 'Egipto', 3788, 'EGY', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('octavos', 'M89', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('octavos', 'M90', 'republica-checa', 'República Checa', 6188, 'CZE', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD'),
                        ('octavos', 'M91', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-noruega', 'Noruega', 3759, 'NOR', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('octavos', 'M92', 'seleccion-mexico', 'México', 3811, 'MEX', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG'),
                        ('octavos', 'M93', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-espanola', 'España', 3850, 'ESP'),
                        ('octavos', 'M94', 'seleccion-turquia', 'Turquía', 3737, 'TUR', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('octavos', 'M95', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-argentina', 'Argentina', 3770, 'ARG'),
                        ('octavos', 'M96', 'seleccion-suiza', 'Suiza', 3723, 'CHE', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('cuartos', 'M97', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('cuartos', 'M98', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-espanola', 'España', 3850, 'ESP'),
                        ('cuartos', 'M99', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('cuartos', 'M100', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-argentina', 'Argentina', 3770, 'ARG'),
                        ('semifinales', 'M101', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-espanola', 'España', 3850, 'ESP'),
                        ('semifinales', 'M102', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-argentina', 'Argentina', 3770, 'ARG'),
                        ('tercer_puesto', 'M103', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('final', 'M104', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-espanola', 'España', 3850, 'ESP')]

    eliminatoria_porra=[('dieciseisavos', 'M73', 'seleccion-mexico', 'México', 3811, 'MEX', 'canada', 'Canadá', 5577, 'CAN', 'seleccion-mexico', 'México', 3811, 'MEX'),
                        ('dieciseisavos', 'M74', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'haiti', 'Haití', 5582, 'HTI', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('dieciseisavos', 'M75', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-escocia', 'Escocia', 3758, 'SCO', 'seleccion-japon', 'Japón', 3798, 'JPN'),
                        ('dieciseisavos', 'M76', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('dieciseisavos', 'M77', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-suecia', 'Suecia', 3074, 'SWE', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('dieciseisavos', 'M78', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV', 'seleccion-iraq', 'Iraq', 3816, 'IRQ', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV'),
                        ('dieciseisavos', 'M79', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR'),
                        ('dieciseisavos', 'M80', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'curazao', 'Curazao', 61757, 'CUR', 'seleccion-croacia', 'Croacia', 3766, 'HRV'),
                        ('dieciseisavos', 'M81', 'seleccion-australia', 'Australia', 3801, 'AUS', 'seleccion-qatar', 'Catar', 3799, 'QAT', 'seleccion-australia', 'Australia', 3801, 'AUS'),
                        ('dieciseisavos', 'M82', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'republica-checa', 'República Checa', 6188, 'CZE', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('dieciseisavos', 'M83', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-ghana', 'Ghana', 3791, 'GHA', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('dieciseisavos', 'M84', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'),
                        ('dieciseisavos', 'M85', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-iran', 'Irán', 3806, 'IRN', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH'),
                        ('dieciseisavos', 'M86', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'cabo-verde', 'Cabo Verde', 9158, 'CPV', 'seleccion-argelia', 'Argelia', 3787, 'DZA'),
                        ('dieciseisavos', 'M87', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY'),
                        ('dieciseisavos', 'M88', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-egipto', 'Egipto', 3788, 'EGY', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('octavos', 'M89', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('octavos', 'M90', 'seleccion-mexico', 'México', 3811, 'MEX', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-japon', 'Japón', 3798, 'JPN'),
                        ('octavos', 'M91', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV'),
                        ('octavos', 'M92', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR'),
                        ('octavos', 'M93', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'),
                        ('octavos', 'M94', 'seleccion-australia', 'Australia', 3801, 'AUS', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('octavos', 'M95', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('octavos', 'M96', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY'),
                        ('cuartos', 'M97', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('cuartos', 'M98', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'),
                        ('cuartos', 'M99', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR'),
                        ('cuartos', 'M100', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('semifinales', 'M101', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'),
                        ('semifinales', 'M102', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('tercer_puesto', 'M103', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('final', 'M104', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-espanola', 'España', 3850, 'ESP')]

    assert calcularBonusCampeonEliminatorias(eliminatoria_real, eliminatoria_porra)==35

def test_calcular_bonus_final_exacta_eliminatorias_real_sin_datos():

    eliminatoria_real=[]

    eliminatoria_porra=[('dieciseisavos', 'M73', 'seleccion-mexico', 'México', 3811, 'MEX', 'canada', 'Canadá', 5577, 'CAN', 'seleccion-mexico', 'México', 3811, 'MEX'),
                        ('dieciseisavos', 'M74', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'haiti', 'Haití', 5582, 'HTI', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('dieciseisavos', 'M75', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-escocia', 'Escocia', 3758, 'SCO', 'seleccion-japon', 'Japón', 3798, 'JPN'),
                        ('dieciseisavos', 'M76', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('dieciseisavos', 'M77', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-suecia', 'Suecia', 3074, 'SWE', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('dieciseisavos', 'M78', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV', 'seleccion-iraq', 'Iraq', 3816, 'IRQ', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV'),
                        ('dieciseisavos', 'M79', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR'),
                        ('dieciseisavos', 'M80', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'curazao', 'Curazao', 61757, 'CUR', 'seleccion-croacia', 'Croacia', 3766, 'HRV'),
                        ('dieciseisavos', 'M81', 'seleccion-australia', 'Australia', 3801, 'AUS', 'seleccion-qatar', 'Catar', 3799, 'QAT', 'seleccion-australia', 'Australia', 3801, 'AUS'),
                        ('dieciseisavos', 'M82', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'republica-checa', 'República Checa', 6188, 'CZE', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('dieciseisavos', 'M83', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-ghana', 'Ghana', 3791, 'GHA', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('dieciseisavos', 'M84', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'),
                        ('dieciseisavos', 'M85', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-iran', 'Irán', 3806, 'IRN', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH'),
                        ('dieciseisavos', 'M86', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'cabo-verde', 'Cabo Verde', 9158, 'CPV', 'seleccion-argelia', 'Argelia', 3787, 'DZA'),
                        ('dieciseisavos', 'M87', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY'),
                        ('dieciseisavos', 'M88', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-egipto', 'Egipto', 3788, 'EGY', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('octavos', 'M89', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('octavos', 'M90', 'seleccion-mexico', 'México', 3811, 'MEX', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-japon', 'Japón', 3798, 'JPN'),
                        ('octavos', 'M91', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV'),
                        ('octavos', 'M92', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR'),
                        ('octavos', 'M93', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'),
                        ('octavos', 'M94', 'seleccion-australia', 'Australia', 3801, 'AUS', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('octavos', 'M95', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('octavos', 'M96', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY'),
                        ('cuartos', 'M97', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('cuartos', 'M98', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'),
                        ('cuartos', 'M99', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR'),
                        ('cuartos', 'M100', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('semifinales', 'M101', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'),
                        ('semifinales', 'M102', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('tercer_puesto', 'M103', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('final', 'M104', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU')]

    assert calcularBonusFinalExactaEliminatorias(eliminatoria_real, eliminatoria_porra)==0

def test_calcular_bonus_final_exacta_eliminatorias_porra_sin_datos():

    eliminatoria_real=[('dieciseisavos', 'M73', 'republica-checa', 'República Checa', 6188, 'CZE', 'canada', 'Canadá', 5577, 'CAN', 'republica-checa', 'República Checa', 6188, 'CZE'), 
                        ('dieciseisavos', 'M74', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('dieciseisavos', 'M75', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-marruecos', 'Marruecos', 3780, 'MAR', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD'),
                        ('dieciseisavos', 'M76', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('dieciseisavos', 'M77', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-suecia', 'Suecia', 3074, 'SWE', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('dieciseisavos', 'M78', 'seleccion-ecuador', 'Ecuador', 3771, 'ECU', 'seleccion-noruega', 'Noruega', 3759, 'NOR', 'seleccion-noruega', 'Noruega', 3759, 'NOR'),
                        ('dieciseisavos', 'M79', 'seleccion-mexico', 'México', 3811, 'MEX', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-mexico', 'México', 3811, 'MEX'),
                        ('dieciseisavos', 'M80', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG', 'senegal', 'Senegal', 5658, 'SEN', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG'),
                        ('dieciseisavos', 'M81', 'seleccion-turquia', 'Turquía', 3737, 'TUR', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-turquia', 'Turquía', 3737, 'TUR'),
                        ('dieciseisavos', 'M82', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('dieciseisavos', 'M83', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'seleccion-colombia', 'Colombia', 3774, 'COL'),
                        ('dieciseisavos', 'M84', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-austria', 'Austria', 3767, 'AUT', 'seleccion-espanola', 'España', 3850, 'ESP'),
                        ('dieciseisavos', 'M85', 'seleccion-suiza', 'Suiza', 3723, 'CHE', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'seleccion-suiza', 'Suiza', 3723, 'CHE'),
                        ('dieciseisavos', 'M86', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-uruguay', 'Uruguay', 3768, 'URY', 'seleccion-argentina', 'Argentina', 3770, 'ARG'),
                        ('dieciseisavos', 'M87', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-ghana', 'Ghana', 3791, 'GHA', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('dieciseisavos', 'M88', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-egipto', 'Egipto', 3788, 'EGY', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('octavos', 'M89', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('octavos', 'M90', 'republica-checa', 'República Checa', 6188, 'CZE', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD'),
                        ('octavos', 'M91', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-noruega', 'Noruega', 3759, 'NOR', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('octavos', 'M92', 'seleccion-mexico', 'México', 3811, 'MEX', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG'),
                        ('octavos', 'M93', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-espanola', 'España', 3850, 'ESP'),
                        ('octavos', 'M94', 'seleccion-turquia', 'Turquía', 3737, 'TUR', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('octavos', 'M95', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-argentina', 'Argentina', 3770, 'ARG'),
                        ('octavos', 'M96', 'seleccion-suiza', 'Suiza', 3723, 'CHE', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('cuartos', 'M97', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('cuartos', 'M98', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-espanola', 'España', 3850, 'ESP'),
                        ('cuartos', 'M99', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('cuartos', 'M100', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-argentina', 'Argentina', 3770, 'ARG'),
                        ('semifinales', 'M101', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-espanola', 'España', 3850, 'ESP'),
                        ('semifinales', 'M102', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-argentina', 'Argentina', 3770, 'ARG'),
                        ('tercer_puesto', 'M103', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('final', 'M104', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-espanola', 'España', 3850, 'ESP')]

    eliminatoria_porra=[]

    assert calcularBonusFinalExactaEliminatorias(eliminatoria_real, eliminatoria_porra)==0

def test_calcular_bonus_final_exacta_eliminatorias_reaL_sin_final():

    eliminatoria_real=[('dieciseisavos', 'M73', 'republica-checa', 'República Checa', 6188, 'CZE', 'canada', 'Canadá', 5577, 'CAN', 'republica-checa', 'República Checa', 6188, 'CZE'), 
                        ('dieciseisavos', 'M74', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('dieciseisavos', 'M75', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-marruecos', 'Marruecos', 3780, 'MAR', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD'),
                        ('dieciseisavos', 'M76', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('dieciseisavos', 'M77', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-suecia', 'Suecia', 3074, 'SWE', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('dieciseisavos', 'M78', 'seleccion-ecuador', 'Ecuador', 3771, 'ECU', 'seleccion-noruega', 'Noruega', 3759, 'NOR', 'seleccion-noruega', 'Noruega', 3759, 'NOR'),
                        ('dieciseisavos', 'M79', 'seleccion-mexico', 'México', 3811, 'MEX', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-mexico', 'México', 3811, 'MEX'),
                        ('dieciseisavos', 'M80', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG', 'senegal', 'Senegal', 5658, 'SEN', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG'),
                        ('dieciseisavos', 'M81', 'seleccion-turquia', 'Turquía', 3737, 'TUR', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-turquia', 'Turquía', 3737, 'TUR'),
                        ('dieciseisavos', 'M82', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('dieciseisavos', 'M83', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'seleccion-colombia', 'Colombia', 3774, 'COL'),
                        ('dieciseisavos', 'M84', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-austria', 'Austria', 3767, 'AUT', 'seleccion-espanola', 'España', 3850, 'ESP'),
                        ('dieciseisavos', 'M85', 'seleccion-suiza', 'Suiza', 3723, 'CHE', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'seleccion-suiza', 'Suiza', 3723, 'CHE'),
                        ('dieciseisavos', 'M86', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-uruguay', 'Uruguay', 3768, 'URY', 'seleccion-argentina', 'Argentina', 3770, 'ARG'),
                        ('dieciseisavos', 'M87', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-ghana', 'Ghana', 3791, 'GHA', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('dieciseisavos', 'M88', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-egipto', 'Egipto', 3788, 'EGY', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('octavos', 'M89', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('octavos', 'M90', 'republica-checa', 'República Checa', 6188, 'CZE', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD'),
                        ('octavos', 'M91', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-noruega', 'Noruega', 3759, 'NOR', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('octavos', 'M92', 'seleccion-mexico', 'México', 3811, 'MEX', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG'),
                        ('octavos', 'M93', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-espanola', 'España', 3850, 'ESP'),
                        ('octavos', 'M94', 'seleccion-turquia', 'Turquía', 3737, 'TUR', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('octavos', 'M95', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-argentina', 'Argentina', 3770, 'ARG'),
                        ('octavos', 'M96', 'seleccion-suiza', 'Suiza', 3723, 'CHE', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('cuartos', 'M97', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('cuartos', 'M98', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-espanola', 'España', 3850, 'ESP'),
                        ('cuartos', 'M99', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('cuartos', 'M100', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-argentina', 'Argentina', 3770, 'ARG'),
                        ('semifinales', 'M101', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-espanola', 'España', 3850, 'ESP'),
                        ('semifinales', 'M102', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-argentina', 'Argentina', 3770, 'ARG'),
                        ('tercer_puesto', 'M103', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-francia', 'Francia', 3750, 'FRA')]

    eliminatoria_porra=[('dieciseisavos', 'M73', 'seleccion-mexico', 'México', 3811, 'MEX', 'canada', 'Canadá', 5577, 'CAN', 'seleccion-mexico', 'México', 3811, 'MEX'),
                        ('dieciseisavos', 'M74', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'haiti', 'Haití', 5582, 'HTI', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('dieciseisavos', 'M75', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-escocia', 'Escocia', 3758, 'SCO', 'seleccion-japon', 'Japón', 3798, 'JPN'),
                        ('dieciseisavos', 'M76', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('dieciseisavos', 'M77', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-suecia', 'Suecia', 3074, 'SWE', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('dieciseisavos', 'M78', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV', 'seleccion-iraq', 'Iraq', 3816, 'IRQ', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV'),
                        ('dieciseisavos', 'M79', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR'),
                        ('dieciseisavos', 'M80', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'curazao', 'Curazao', 61757, 'CUR', 'seleccion-croacia', 'Croacia', 3766, 'HRV'),
                        ('dieciseisavos', 'M81', 'seleccion-australia', 'Australia', 3801, 'AUS', 'seleccion-qatar', 'Catar', 3799, 'QAT', 'seleccion-australia', 'Australia', 3801, 'AUS'),
                        ('dieciseisavos', 'M82', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'republica-checa', 'República Checa', 6188, 'CZE', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('dieciseisavos', 'M83', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-ghana', 'Ghana', 3791, 'GHA', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('dieciseisavos', 'M84', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'),
                        ('dieciseisavos', 'M85', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-iran', 'Irán', 3806, 'IRN', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH'),
                        ('dieciseisavos', 'M86', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'cabo-verde', 'Cabo Verde', 9158, 'CPV', 'seleccion-argelia', 'Argelia', 3787, 'DZA'),
                        ('dieciseisavos', 'M87', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY'),
                        ('dieciseisavos', 'M88', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-egipto', 'Egipto', 3788, 'EGY', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('octavos', 'M89', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('octavos', 'M90', 'seleccion-mexico', 'México', 3811, 'MEX', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-japon', 'Japón', 3798, 'JPN'),
                        ('octavos', 'M91', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV'),
                        ('octavos', 'M92', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR'),
                        ('octavos', 'M93', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'),
                        ('octavos', 'M94', 'seleccion-australia', 'Australia', 3801, 'AUS', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('octavos', 'M95', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('octavos', 'M96', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY'),
                        ('cuartos', 'M97', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('cuartos', 'M98', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'),
                        ('cuartos', 'M99', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR'),
                        ('cuartos', 'M100', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('semifinales', 'M101', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'),
                        ('semifinales', 'M102', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('tercer_puesto', 'M103', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('final', 'M104', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU')]

    assert calcularBonusFinalExactaEliminatorias(eliminatoria_real, eliminatoria_porra)==0

@pytest.mark.parametrize(["final_porra"],
    [   
        (('final', 'M104', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'),),
        (('final', 'M104', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-espanola', 'España', 3850, 'ESP'),),
        (('final', 'M104', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),)
    ]
)
def test_calcular_bonus_final_exacta_eliminatorias_final_erronea(final_porra):

    eliminatoria_real=[('dieciseisavos', 'M73', 'republica-checa', 'República Checa', 6188, 'CZE', 'canada', 'Canadá', 5577, 'CAN', 'republica-checa', 'República Checa', 6188, 'CZE'), 
                        ('dieciseisavos', 'M74', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('dieciseisavos', 'M75', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-marruecos', 'Marruecos', 3780, 'MAR', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD'),
                        ('dieciseisavos', 'M76', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('dieciseisavos', 'M77', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-suecia', 'Suecia', 3074, 'SWE', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('dieciseisavos', 'M78', 'seleccion-ecuador', 'Ecuador', 3771, 'ECU', 'seleccion-noruega', 'Noruega', 3759, 'NOR', 'seleccion-noruega', 'Noruega', 3759, 'NOR'),
                        ('dieciseisavos', 'M79', 'seleccion-mexico', 'México', 3811, 'MEX', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-mexico', 'México', 3811, 'MEX'),
                        ('dieciseisavos', 'M80', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG', 'senegal', 'Senegal', 5658, 'SEN', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG'),
                        ('dieciseisavos', 'M81', 'seleccion-turquia', 'Turquía', 3737, 'TUR', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-turquia', 'Turquía', 3737, 'TUR'),
                        ('dieciseisavos', 'M82', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('dieciseisavos', 'M83', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'seleccion-colombia', 'Colombia', 3774, 'COL'),
                        ('dieciseisavos', 'M84', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-austria', 'Austria', 3767, 'AUT', 'seleccion-espanola', 'España', 3850, 'ESP'),
                        ('dieciseisavos', 'M85', 'seleccion-suiza', 'Suiza', 3723, 'CHE', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'seleccion-suiza', 'Suiza', 3723, 'CHE'),
                        ('dieciseisavos', 'M86', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-uruguay', 'Uruguay', 3768, 'URY', 'seleccion-argentina', 'Argentina', 3770, 'ARG'),
                        ('dieciseisavos', 'M87', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-ghana', 'Ghana', 3791, 'GHA', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('dieciseisavos', 'M88', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-egipto', 'Egipto', 3788, 'EGY', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('octavos', 'M89', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('octavos', 'M90', 'republica-checa', 'República Checa', 6188, 'CZE', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD'),
                        ('octavos', 'M91', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-noruega', 'Noruega', 3759, 'NOR', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('octavos', 'M92', 'seleccion-mexico', 'México', 3811, 'MEX', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG'),
                        ('octavos', 'M93', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-espanola', 'España', 3850, 'ESP'),
                        ('octavos', 'M94', 'seleccion-turquia', 'Turquía', 3737, 'TUR', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('octavos', 'M95', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-argentina', 'Argentina', 3770, 'ARG'),
                        ('octavos', 'M96', 'seleccion-suiza', 'Suiza', 3723, 'CHE', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('cuartos', 'M97', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('cuartos', 'M98', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-espanola', 'España', 3850, 'ESP'),
                        ('cuartos', 'M99', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('cuartos', 'M100', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-argentina', 'Argentina', 3770, 'ARG'),
                        ('semifinales', 'M101', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-espanola', 'España', 3850, 'ESP'),
                        ('semifinales', 'M102', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-argentina', 'Argentina', 3770, 'ARG'),
                        ('tercer_puesto', 'M103', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('final', 'M104', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-espanola', 'España', 3850, 'ESP')]

    eliminatoria_porra=[('dieciseisavos', 'M73', 'seleccion-mexico', 'México', 3811, 'MEX', 'canada', 'Canadá', 5577, 'CAN', 'seleccion-mexico', 'México', 3811, 'MEX'),
                        ('dieciseisavos', 'M74', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'haiti', 'Haití', 5582, 'HTI', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('dieciseisavos', 'M75', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-escocia', 'Escocia', 3758, 'SCO', 'seleccion-japon', 'Japón', 3798, 'JPN'),
                        ('dieciseisavos', 'M76', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('dieciseisavos', 'M77', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-suecia', 'Suecia', 3074, 'SWE', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('dieciseisavos', 'M78', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV', 'seleccion-iraq', 'Iraq', 3816, 'IRQ', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV'),
                        ('dieciseisavos', 'M79', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR'),
                        ('dieciseisavos', 'M80', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'curazao', 'Curazao', 61757, 'CUR', 'seleccion-croacia', 'Croacia', 3766, 'HRV'),
                        ('dieciseisavos', 'M81', 'seleccion-australia', 'Australia', 3801, 'AUS', 'seleccion-qatar', 'Catar', 3799, 'QAT', 'seleccion-australia', 'Australia', 3801, 'AUS'),
                        ('dieciseisavos', 'M82', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'republica-checa', 'República Checa', 6188, 'CZE', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('dieciseisavos', 'M83', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-ghana', 'Ghana', 3791, 'GHA', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('dieciseisavos', 'M84', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'),
                        ('dieciseisavos', 'M85', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-iran', 'Irán', 3806, 'IRN', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH'),
                        ('dieciseisavos', 'M86', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'cabo-verde', 'Cabo Verde', 9158, 'CPV', 'seleccion-argelia', 'Argelia', 3787, 'DZA'),
                        ('dieciseisavos', 'M87', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY'),
                        ('dieciseisavos', 'M88', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-egipto', 'Egipto', 3788, 'EGY', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('octavos', 'M89', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('octavos', 'M90', 'seleccion-mexico', 'México', 3811, 'MEX', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-japon', 'Japón', 3798, 'JPN'),
                        ('octavos', 'M91', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV'),
                        ('octavos', 'M92', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR'),
                        ('octavos', 'M93', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'),
                        ('octavos', 'M94', 'seleccion-australia', 'Australia', 3801, 'AUS', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('octavos', 'M95', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('octavos', 'M96', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY'),
                        ('cuartos', 'M97', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('cuartos', 'M98', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'),
                        ('cuartos', 'M99', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR'),
                        ('cuartos', 'M100', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('semifinales', 'M101', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'),
                        ('semifinales', 'M102', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('tercer_puesto', 'M103', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        final_porra]

    assert calcularBonusFinalExactaEliminatorias(eliminatoria_real, eliminatoria_porra)==0

def test_calcular_bonus_final_exacta_eliminatorias_final_exacta():

    eliminatoria_real=[('dieciseisavos', 'M73', 'republica-checa', 'República Checa', 6188, 'CZE', 'canada', 'Canadá', 5577, 'CAN', 'republica-checa', 'República Checa', 6188, 'CZE'), 
                        ('dieciseisavos', 'M74', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('dieciseisavos', 'M75', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-marruecos', 'Marruecos', 3780, 'MAR', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD'),
                        ('dieciseisavos', 'M76', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('dieciseisavos', 'M77', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-suecia', 'Suecia', 3074, 'SWE', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('dieciseisavos', 'M78', 'seleccion-ecuador', 'Ecuador', 3771, 'ECU', 'seleccion-noruega', 'Noruega', 3759, 'NOR', 'seleccion-noruega', 'Noruega', 3759, 'NOR'),
                        ('dieciseisavos', 'M79', 'seleccion-mexico', 'México', 3811, 'MEX', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-mexico', 'México', 3811, 'MEX'),
                        ('dieciseisavos', 'M80', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG', 'senegal', 'Senegal', 5658, 'SEN', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG'),
                        ('dieciseisavos', 'M81', 'seleccion-turquia', 'Turquía', 3737, 'TUR', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-turquia', 'Turquía', 3737, 'TUR'),
                        ('dieciseisavos', 'M82', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('dieciseisavos', 'M83', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'seleccion-colombia', 'Colombia', 3774, 'COL'),
                        ('dieciseisavos', 'M84', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-austria', 'Austria', 3767, 'AUT', 'seleccion-espanola', 'España', 3850, 'ESP'),
                        ('dieciseisavos', 'M85', 'seleccion-suiza', 'Suiza', 3723, 'CHE', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'seleccion-suiza', 'Suiza', 3723, 'CHE'),
                        ('dieciseisavos', 'M86', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-uruguay', 'Uruguay', 3768, 'URY', 'seleccion-argentina', 'Argentina', 3770, 'ARG'),
                        ('dieciseisavos', 'M87', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-ghana', 'Ghana', 3791, 'GHA', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('dieciseisavos', 'M88', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-egipto', 'Egipto', 3788, 'EGY', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('octavos', 'M89', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('octavos', 'M90', 'republica-checa', 'República Checa', 6188, 'CZE', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD'),
                        ('octavos', 'M91', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-noruega', 'Noruega', 3759, 'NOR', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('octavos', 'M92', 'seleccion-mexico', 'México', 3811, 'MEX', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG'),
                        ('octavos', 'M93', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-espanola', 'España', 3850, 'ESP'),
                        ('octavos', 'M94', 'seleccion-turquia', 'Turquía', 3737, 'TUR', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('octavos', 'M95', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-argentina', 'Argentina', 3770, 'ARG'),
                        ('octavos', 'M96', 'seleccion-suiza', 'Suiza', 3723, 'CHE', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('cuartos', 'M97', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('cuartos', 'M98', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-espanola', 'España', 3850, 'ESP'),
                        ('cuartos', 'M99', 'seleccion-inglaterra', 'Inglaterra', 3745, 'ENG', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('cuartos', 'M100', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-argentina', 'Argentina', 3770, 'ARG'),
                        ('semifinales', 'M101', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-espanola', 'España', 3850, 'ESP'),
                        ('semifinales', 'M102', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-argentina', 'Argentina', 3770, 'ARG'),
                        ('tercer_puesto', 'M103', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('final', 'M104', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-espanola', 'España', 3850, 'ESP')]

    eliminatoria_porra=[('dieciseisavos', 'M73', 'seleccion-mexico', 'México', 3811, 'MEX', 'canada', 'Canadá', 5577, 'CAN', 'seleccion-mexico', 'México', 3811, 'MEX'),
                        ('dieciseisavos', 'M74', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'haiti', 'Haití', 5582, 'HTI', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('dieciseisavos', 'M75', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-escocia', 'Escocia', 3758, 'SCO', 'seleccion-japon', 'Japón', 3798, 'JPN'),
                        ('dieciseisavos', 'M76', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-holanda', 'Países Bajos', 3761, 'NLD', 'seleccion-brasil', 'Brasil', 3775, 'BRA'),
                        ('dieciseisavos', 'M77', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-suecia', 'Suecia', 3074, 'SWE', 'seleccion-francia', 'Francia', 3750, 'FRA'),
                        ('dieciseisavos', 'M78', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV', 'seleccion-iraq', 'Iraq', 3816, 'IRQ', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV'),
                        ('dieciseisavos', 'M79', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR'),
                        ('dieciseisavos', 'M80', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'curazao', 'Curazao', 61757, 'CUR', 'seleccion-croacia', 'Croacia', 3766, 'HRV'),
                        ('dieciseisavos', 'M81', 'seleccion-australia', 'Australia', 3801, 'AUS', 'seleccion-qatar', 'Catar', 3799, 'QAT', 'seleccion-australia', 'Australia', 3801, 'AUS'),
                        ('dieciseisavos', 'M82', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'republica-checa', 'República Checa', 6188, 'CZE', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('dieciseisavos', 'M83', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-ghana', 'Ghana', 3791, 'GHA', 'seleccion-portugal', 'Portugal', 3762, 'PRT'),
                        ('dieciseisavos', 'M84', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'),
                        ('dieciseisavos', 'M85', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-iran', 'Irán', 3806, 'IRN', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH'),
                        ('dieciseisavos', 'M86', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'cabo-verde', 'Cabo Verde', 9158, 'CPV', 'seleccion-argelia', 'Argelia', 3787, 'DZA'),
                        ('dieciseisavos', 'M87', 'seleccion-colombia', 'Colombia', 3774, 'COL', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY'),
                        ('dieciseisavos', 'M88', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-egipto', 'Egipto', 3788, 'EGY', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('octavos', 'M89', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-francia', 'Francia', 3750, 'FRA', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('octavos', 'M90', 'seleccion-mexico', 'México', 3811, 'MEX', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-japon', 'Japón', 3798, 'JPN'),
                        ('octavos', 'M91', 'seleccion-brasil', 'Brasil', 3775, 'BRA', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV'),
                        ('octavos', 'M92', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-croacia', 'Croacia', 3766, 'HRV', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR'),
                        ('octavos', 'M93', 'seleccion-portugal', 'Portugal', 3762, 'PRT', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'),
                        ('octavos', 'M94', 'seleccion-australia', 'Australia', 3801, 'AUS', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-belgica', 'Bélgica', 3738, 'BEL'),
                        ('octavos', 'M95', 'seleccion-argelia', 'Argelia', 3787, 'DZA', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('octavos', 'M96', 'seleccion-bosnia-herzegovina', 'Bosnia-Herzegovina', 3741, 'BIH', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY'),
                        ('cuartos', 'M97', 'seleccion-japon', 'Japón', 3798, 'JPN', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('cuartos', 'M98', 'seleccion-belgica', 'Bélgica', 3738, 'BEL', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'),
                        ('cuartos', 'M99', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-costa-marfil', 'Costa de Marfil', 3795, 'CIV', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR'),
                        ('cuartos', 'M100', 'seleccion-paraguay', 'Paraguay', 3773, 'PRY', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('semifinales', 'M101', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU', 'seleccion-arabia-saudi', 'Arabia Saudí', 3803, 'SAU'),
                        ('semifinales', 'M102', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA', 'seleccion-estados-unidos', 'Estados Unidos', 3810, 'USA'),
                        ('tercer_puesto', 'M103', 'seleccion-alemania', 'Alemania', 3734, 'DEU', 'seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'seleccion-alemania', 'Alemania', 3734, 'DEU'),
                        ('final', 'M104', 'seleccion-espanola', 'España', 3850, 'ESP', 'seleccion-argentina', 'Argentina', 3770, 'ARG', 'seleccion-espanola', 'España', 3850, 'ESP')]

    assert calcularBonusFinalExactaEliminatorias(eliminatoria_real, eliminatoria_porra)==15