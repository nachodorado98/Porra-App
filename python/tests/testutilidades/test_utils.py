import pytest
import os

from src.utilidades.utils import codigo_valido, usuario_correcto, nombre_correcto, apellido_correcto, contrasena_correcta
from src.utilidades.utils import correo_correcto, datos_correctos, generarHash, comprobarHash, obtenerGruposEquiposLimpios
from src.utilidades.utils import validarEquiposGrupo, gruposPorraCorrectos, obtenerTercerosGruposEquiposLimpios, mejoresTercerosPorraCorrectos
from src.utilidades.utils import obtenerPasoEstado, obtenerPasosPorra, obtenerCombinacionMejoresTerceros, construirLookup, crearBracketDieciseisavos
from src.utilidades.utils import crearCarpeta, borrarCarpeta, vaciarCarpeta, extraerExtension

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
        ({'grupo_completo': False, 'mejor_tercero_completo': False}, 0),
        ({'grupo_completo': True, 'mejor_tercero_completo': False}, 1),
        ({'grupo_completo': True, 'mejor_tercero_completo': True}, 2),
    ]
)
def test_obtener_paso_estado(estado, paso):

    assert obtenerPasoEstado(estado)==paso

@pytest.mark.parametrize(["estado_porra", "paso"],
    [((False, False), 0), ((True, False), 1), ((True, True), 2)]
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