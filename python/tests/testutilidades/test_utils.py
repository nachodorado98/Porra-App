import pytest

from src.utilidades.utils import codigo_valido, usuario_correcto, nombre_correcto, apellido_correcto, contrasena_correcta
from src.utilidades.utils import correo_correcto, datos_correctos, generarHash, comprobarHash, obtenerGruposEquiposLimpios
from src.utilidades.utils import validarEquiposGrupo, gruposPorraCorrectos

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
        (['seleccion-brasil', 'seleccion-marruecos', 'seleccion-escocia', 'haiti'],)
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
