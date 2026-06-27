import pytest
import json
from unittest.mock import patch
from datetime import datetime, timedelta

def test_pagina_registro(cliente, conexion):

	respuesta=cliente.get("/registro")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Crear Una Cuenta</h1>" in contenido
	assert "<h3>¿Quieres crear o unirte a una liga?</h3>" in contenido
	assert '<div id="contenedor-codigo-generado" style="display:none;">' in contenido
	assert '<div id="contenedor-codigo" style="display:none;">' in contenido

def test_pagina_generar_codigo_no_valido_existente(cliente, conexion):

	with patch("src.blueprints.registro.random.choices") as mock_random:
		with patch("src.blueprints.registro.Conexion") as MockConexion:

			mock_random.return_value=list("ABC123")

			instancia=MockConexion.return_value
			instancia.existe_codigo_liga.return_value=True

			respuesta=cliente.get("/registro/generar_codigo")

			contenido=respuesta.data.decode()

			assert respuesta.status_code==404
			assert "error" in contenido
			assert "Codigo No Valido" in contenido

def test_pagina_generar_codigo(cliente, conexion):

	respuesta=cliente.get("/registro/generar_codigo")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200

	diccionario_contenido=json.loads(contenido)

	codigo=diccionario_contenido["codigo"]

	assert f'"codigo": "{codigo}"' in contenido
	assert len(codigo)==6
	assert codigo.isalnum() and codigo.isupper()

@pytest.mark.parametrize(["codigo"],
	[("123456",),("ABCDE",),("ABCDE&",),("ABCDEFG",),("A1BC2DEF",)]
)
def test_pagina_verificar_codigo_no_valido(cliente, conexion, codigo):

	respuesta=cliente.get(f"/registro/verificar_codigo/{codigo}")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==404
	assert "error" in contenido
	assert "Codigo No Valido" in contenido

@pytest.mark.parametrize(["codigo"],
	[("ABCDEF",),("ABCDE1",),("ZK5Z1Q",),("3YYZKP",),("GTMRIJ",),("abcdef",)]
)
def test_pagina_verificar_codigo_valido_no_existente(cliente, conexion, codigo):

	respuesta=cliente.get(f"/registro/verificar_codigo/{codigo}")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==404
	assert "error" in contenido
	assert "Codigo No Existente" in contenido

@pytest.mark.parametrize(["codigo"],
	[("ABCDEF",),("ABCDE1",),("ZK5Z1Q",),("3YYZKP",),("GTMRIJ",),("abcdef",)]
)
def test_pagina_verificar_codigo_valido_existente(cliente, conexion, codigo):

	conexion.insertarCodigoLiga(codigo)

	respuesta=cliente.get(f"/registro/verificar_codigo/{codigo}")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200

	diccionario_valido=json.loads(contenido)

	valido=diccionario_valido["valido"]

	assert valido

@pytest.mark.parametrize(["usuario"],
	[(None,), ("",), (" ",), ("carlos-456",), ("usuario raro",), ("nacho@98",)]
)
def test_pagina_singup_usuario_incorrecto(cliente, conexion, usuario):

	respuesta=cliente.post("/singup", data={"usuario":usuario, "correo":"correo@correo.es", "nombre":"nacho",
											"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
											"codigo_final":"3YYZKP", "accion_liga":"crear"}, follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert respuesta.request.path=="/registro"
	assert '<div class="mensaje error">El usuario no es válido</div>' in contenido

@pytest.mark.parametrize(["nombre"],
	[(None,), ("",), (" ",), ("nacho1",), ("nacho_",), ("nacho@",)]
)
def test_pagina_singup_nombre_incorrecto(cliente, conexion, nombre):

	respuesta=cliente.post("/singup", data={"usuario":"golden98", "correo":"correo@correo.es", "nombre":nombre,
											"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
											"codigo_final":"3YYZKP", "accion_liga":"crear"}, follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert respuesta.request.path=="/registro"
	assert '<div class="mensaje error">El nombre introducido no es válido</div>' in contenido

@pytest.mark.parametrize(["apellido"],
	[(None,), ("",), (" ",), ("dorado1",), ("dorado_",), ("dorado@",)]
)
def test_pagina_singup_apellido_incorrecto(cliente, conexion, apellido):

	respuesta=cliente.post("/singup", data={"usuario":"golden98", "correo":"correo@correo.es", "nombre":"nacho",
											"apellido":apellido, "contrasena":"Ab!CdEfGhIJK3LMN",
											"codigo_final":"3YYZKP", "accion_liga":"crear"}, follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert respuesta.request.path=="/registro"
	assert '<div class="mensaje error">El apellido introducido no es válido</div>' in contenido

@pytest.mark.parametrize(["contrasena"],
	[(None,), ("",), (" ",), ("1234567",), ("abc defgh",)]
)
def test_pagina_singup_contrasena_incorrecta(cliente, conexion, contrasena):

	respuesta=cliente.post("/singup", data={"usuario":"golden98", "correo":"correo@correo.es", "nombre":"nacho",
											"apellido":"dorado", "contrasena":contrasena,
											"codigo_final":"3YYZKP", "accion_liga":"crear"}, follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert respuesta.request.path=="/registro"
	assert '<div class="mensaje error">La contraseña debe tener al menos 8 caracteres y no contener espacios</div>' in contenido

@pytest.mark.parametrize(["correo"],
	[(None,), ("",), (" ",), ("correo",), ("correo@",), ("correo@.es",), ("correo.es",), ("@correo.es",)]
)
def test_pagina_singup_correo_incorrecto(cliente, conexion, correo):

	respuesta=cliente.post("/singup", data={"usuario":"golden98", "correo":correo, "nombre":"nacho",
											"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
											"codigo_final":"3YYZKP", "accion_liga":"crear"}, follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert respuesta.request.path=="/registro"
	assert '<div class="mensaje error">El correo electrónico no es válido</div>' in contenido

@pytest.mark.parametrize(["usuario", "nombre", "apellido", "contrasena", "correo", "codigo"],
	[
		("nacho98", "nacho", "dorado", "Ab!CdEfGhIJK3LMN", "usuario@gmail.com", "123456"),
		("golden98", "nachogolden", "dorado", "Abcd1234!","correo@correo.es", "ABCDE"),
		("carlos_456", "nachogolden", "dorado", "22&NachoD&19", "ejemplo123@yahoo.com", None),
		("carlos_456", "nachogolden", "dorado", "12345678", "ejemplo123@yahoo.com", "ABCDE&"),
		("golden98", "nachogolden", "dorado", "Abcd1234!","correo@correo.es", "A1BC2DEF")
	]
)
def test_pagina_singup_datos_correctos_codigo_no_valido(cliente, conexion, usuario, correo, nombre, apellido, contrasena, codigo):

	respuesta=cliente.post("/singup", data={"usuario":usuario, "correo":correo, "nombre":nombre,
											"apellido":apellido, "contrasena":contrasena,
											"codigo_final":codigo, "accion_liga":"crear"}, follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert respuesta.request.path=="/registro"
	assert '<div class="mensaje error">El código de liga no es válido</div>' in contenido

@pytest.mark.parametrize(["accion"],
	[("unir",),("crea",),("join",),("hola",),("jhsjdjdf3432",)]
)
def test_pagina_singup_datos_correctos_codigo_valido_accion_erronea(cliente, conexion, accion):

	respuesta=cliente.post("/singup", data={"usuario":"nacho98", "correo":"usuario@gmail.com", "nombre":"nacho",
											"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
											"codigo_final":"3YYZKP", "accion_liga":accion}, follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert respuesta.request.path=="/registro"
	assert '<div class="mensaje error">Debes seleccionar si quieres crear o unirte a una liga</div>' in contenido

@pytest.mark.parametrize(["dias"],
	[(2,),(22,),(5,),(13,),(25,),(1,),(0,)]
)
def test_pagina_singup_porra_cerrada(cliente, conexion, dias):

	fecha_anterior=(datetime.now()-timedelta(days=dias)).strftime("%Y-%m-%d")

	conexion.insertarClaveValorMaestro("fecha_cierre_porra", fecha_anterior)

	conexion.insertarCodigoLiga("3YYZKP")

	respuesta=cliente.post("/singup", data={"usuario":"nacho98", "correo":"usuario@gmail.com", "nombre":"nacho",
											"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
											"codigo_final":"3YYZKP", "accion_liga":"unirse"}, follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert respuesta.request.path=="/registro"
	assert '<div class="mensaje error">El registro está cerrado actualmente</div>' in contenido

@pytest.mark.parametrize(["usuario"],
	[("nacho98",),("naCho98",),("nacho",),("amanditaa",),("amanda99",)]
)
def test_pagina_singup_usuario_existente(cliente, conexion, usuario):

	conexion.insertarCodigoLiga("3YYZKP")

	conexion.insertarUsuario(usuario, "nacho@gmail.es", "Ab!CdEfGhIJK3LMN", "nachogolden", "dorado", "3YYZKP")

	respuesta=cliente.post("/singup", data={"usuario":usuario, "correo":"usuario@gmail.com", "nombre":"nacho",
											"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
											"codigo_final":"3YYZKP", "accion_liga":"unirse"}, follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert respuesta.request.path=="/registro"
	assert '<div class="mensaje error">El usuario introducido ya existe</div>' in contenido

@pytest.mark.parametrize(["correo"],
	[("usuario@gmail.com",),("correo@gmail.com",),("nacho@gmail.com",),("golden@gmail.com",),("hola123@gmail.com",)]
)
def test_pagina_singup_correo_existente(cliente, conexion, correo):

	conexion.insertarCodigoLiga("3YYZKP")

	conexion.insertarUsuario("nacho98", correo, "Ab!CdEfGhIJK3LMN", "nachogolden", "dorado", "3YYZKP")

	respuesta=cliente.post("/singup", data={"usuario":"nacho99", "correo":correo, "nombre":"nacho",
											"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
											"codigo_final":"3YYZKP", "accion_liga":"unirse"}, follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert respuesta.request.path=="/registro"
	assert '<div class="mensaje error">El correo introducido ya está registrado</div>' in contenido

def test_pagina_singup_crear_liga_codigo_existente(cliente, conexion):

	conexion.insertarCodigoLiga("3YYZKP")

	respuesta=cliente.post("/singup", data={"usuario":"nacho98", "correo":"usuario@gmail.com", "nombre":"nacho",
											"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
											"codigo_final":"3YYZKP", "accion_liga":"crear"}, follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert respuesta.request.path=="/registro"
	assert '<div class="mensaje error">El código de liga introducido ya existe</div>' in contenido

def test_pagina_singup_crear_liga_codigo_no_existente(cliente, conexion):

	respuesta=cliente.post("/singup", data={"usuario":"nacho98", "correo":"usuario@gmail.com", "nombre":"nacho",
											"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
											"codigo_final":"3YYZKP", "accion_liga":"crear"})

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Bienvenido/a</h1>" in contenido
	assert "<p>Gracias por registrarte en nuestra plataforma, Nacho.</p>" in contenido
	assert "<p>Se ha creado la nueva liga con codigo <strong>3YYZKP</strong>.</p>" in contenido
	assert "<p>Te has unido a la liga con codigo <strong>3YYZKP</strong>.</p>" not in contenido
	assert "<p>¡Esperamos que disfrutes de la experiencia a la que ya puedes acceder!</p>" in contenido

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	assert len(usuarios)==1

	conexion.c.execute("SELECT * FROM estado_porra")

	estado_porras=conexion.c.fetchall()

	assert len(estado_porras)==1

	conexion.c.execute("SELECT * FROM puntuaciones")

	puntuacion=conexion.c.fetchall()

	assert len(puntuacion)==1

def test_pagina_singup_unirse_liga_codigo_no_existente(cliente, conexion):

	respuesta=cliente.post("/singup", data={"usuario":"nacho98", "correo":"usuario@gmail.com", "nombre":"nacho",
											"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
											"codigo_final":"3YYZKP", "accion_liga":"unirse"}, follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert respuesta.request.path=="/registro"
	assert '<div class="mensaje error">El código de liga introducido no existe</div>' in contenido

def test_pagina_singup_unirse_liga_codigo_existente(cliente, conexion):

	conexion.insertarCodigoLiga("3YYZKP")

	respuesta=cliente.post("/singup", data={"usuario":"nacho98", "correo":"usuario@gmail.com", "nombre":"nacho",
											"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
											"codigo_final":"3YYZKP", "accion_liga":"unirse"})

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Bienvenido/a</h1>" in contenido
	assert "<p>Gracias por registrarte en nuestra plataforma, Nacho.</p>" in contenido
	assert "<p>Se ha creado la nueva liga con codigo <strong>3YYZKP</strong>.</p>" not in contenido
	assert "<p>Te has unido a la liga con codigo <strong>3YYZKP</strong>.</p>" in contenido
	assert "<p>¡Esperamos que disfrutes de la experiencia a la que ya puedes acceder!</p>" in contenido

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	assert len(usuarios)==1

	conexion.c.execute("SELECT * FROM estado_porra")

	estado_porras=conexion.c.fetchall()

	assert len(estado_porras)==1

	conexion.c.execute("SELECT * FROM puntuaciones")

	puntuacion=conexion.c.fetchall()

	assert len(puntuacion)==1