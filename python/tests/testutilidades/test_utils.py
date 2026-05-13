import pytest

from src.utilidades.utils import codigo_valido, usuario_correcto, nombre_correcto, apellido_correcto, contrasena_correcta
from src.utilidades.utils import correo_correcto, datos_correctos, generarHash, comprobarHash

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