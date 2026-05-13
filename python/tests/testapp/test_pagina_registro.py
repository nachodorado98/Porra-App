import pytest
import json

def test_pagina_registro(cliente):

	respuesta=cliente.get("/registro")

	contenido=respuesta.data.decode()

	respuesta.status_code==200
	assert "<h1>Crear Una Cuenta</h1>" in contenido
	assert "<h3>¿Quieres crear o unirte a una liga?</h3>" in contenido
	assert '<div id="contenedor-codigo-generado" style="display:none;">' in contenido
	assert '<div id="contenedor-codigo" style="display:none;">' in contenido

def test_pagina_generar_codigo(cliente):

	respuesta=cliente.get("/registro/generar_codigo")

	contenido=respuesta.data.decode()

	respuesta.status_code==200

	diccionario_contenido=json.loads(contenido)

	codigo=diccionario_contenido["codigo"]

	assert f'"codigo": "{codigo}"' in contenido
	assert len(codigo)==6
	assert codigo.isalnum() and codigo.isupper()

@pytest.mark.parametrize(["codigo"],
    [("123456",),("ABCDE",),("ABCDE&",),("ABCDEFG",),("A1BC2DEF",)]
)
def test_pagina_verificar_codigo_no_valido(cliente, codigo):

	respuesta=cliente.get(f"/registro/verificar_codigo/{codigo}")

	contenido=respuesta.data.decode()

	respuesta.status_code==200

	diccionario_valido=json.loads(contenido)

	valido=diccionario_valido["valido"]

	assert not valido

@pytest.mark.parametrize(["codigo"],
    [("ABCDEF",),("ABCDE1",),("ZK5Z1Q",),("3YYZKP",),("GTMRIJ",),("abcdef",)]
)
def test_pagina_verificar_codigo_valido(cliente, codigo):

	respuesta=cliente.get(f"/registro/verificar_codigo/{codigo}")

	contenido=respuesta.data.decode()

	respuesta.status_code==200

	diccionario_valido=json.loads(contenido)

	valido=diccionario_valido["valido"]

	assert valido

@pytest.mark.parametrize(["usuario", "nombre", "apellido", "contrasena", "correo", "codigo"],
    [
        (None, "nacho", "dorado", "Ab!CdEfGhIJK3LMN", "correo@correo.es", "3YYZKP"),
        ("golden98", None, "dorado", "Ab!CdEfGhIJK3LMN", "correo@correo.es", "3YYZKP"),
        ("golden98", "nacho", None, "Ab!CdEfGhIJK3LMN", "correo@correo.es", "3YYZKP"),
        ("golden98", "nacho", "dorado", None, "correo@correo.es", "3YYZKP"),
        ("carlos-456", "nacho", "dorado", "Ab!CdEfGhIJK3LMN", "correo@correo.es", "3YYZKP"),
        ("golden98", "nacho1", "dorado", "Ab!CdEfGhIJK3LMN", "correo@correo.es", "3YYZKP"),
        ("golden98", "nacho", "dorado2", "Ab!CdEfGhIJK3LMN", "correo@correo.es", "3YYZKP"),
        ("golden98", "nachogolden", "dorado", "12345678", "correo@.es", "3YYZKP")
    ]
)
def test_pagina_singup_datos_incorrectos(cliente, usuario, correo, nombre, apellido, contrasena, codigo):

	respuesta=cliente.post("/singup", data={"usuario":usuario, "correo":correo, "nombre":nombre,
											"apellido":apellido, "contrasena":contrasena,
											"codigo_final":codigo, "accion_liga":"crear"})

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location=="/registro"
	assert "<h1>Redirecting...</h1>" in contenido

@pytest.mark.parametrize(["usuario", "nombre", "apellido", "contrasena", "correo", "codigo"],
    [
        ("nacho98", "nacho", "dorado", "Ab!CdEfGhIJK3LMN", "usuario@gmail.com", "123456"),
        ("golden98", "nachogolden", "dorado", "Abcd1234!","correo@correo.es", "ABCDE"),
        ("carlos_456", "nachogolden", "dorado", "22&NachoD&19", "ejemplo123@yahoo.com", None),
        ("carlos_456", "nachogolden", "dorado", "12345678", "ejemplo123@yahoo.com", "ABCDE&"),
        ("golden98", "nachogolden", "dorado", "Abcd1234!","correo@correo.es", "A1BC2DEF")
    ]
)
def test_pagina_singup_datos_correctos_codigo_no_valido(cliente, usuario, correo, nombre, apellido, contrasena, codigo):

	respuesta=cliente.post("/singup", data={"usuario":usuario, "correo":correo, "nombre":nombre,
											"apellido":apellido, "contrasena":contrasena,
											"codigo_final":codigo, "accion_liga":"crear"})

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location=="/registro"
	assert "<h1>Redirecting...</h1>" in contenido

@pytest.mark.parametrize(["usuario", "nombre", "apellido", "contrasena", "correo", "codigo"],
    [
        ("nacho98", "nacho", "dorado", "Ab!CdEfGhIJK3LMN", "usuario@gmail.com", "ABCDEF"),
        ("golden98", "nachogolden", "dorado", "Abcd1234!","correo@correo.es", "ABCDE1"),
        ("carlos_456", "nachogolden", "dorado", "22&NachoD&19", "ejemplo123@yahoo.com", "ZK5Z1Q"),
        ("carlos_456", "nachogolden", "dorado", "12345678", "ejemplo123@yahoo.com", "3YYZKP"),
        ("golden98", "nachogolden", "dorado", "Abcd1234!","correo@correo.es", "GTMRIJ")
    ]
)
def test_pagina_singup_datos_correctos_codigo_valido(cliente, usuario, correo, nombre, apellido, contrasena, codigo):

	respuesta=cliente.post("/singup", data={"usuario":usuario, "correo":correo, "nombre":nombre,
											"apellido":apellido, "contrasena":contrasena,
											"codigo_final":codigo, "accion_liga":"crear"})

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Bienvenido/a</h1>" in contenido
	assert f"<p>Gracias por registrarte en nuestra plataforma, {nombre.title()}.</p>" in contenido
	assert f"<p>Se ha creado la nueva liga con codigo <strong>{ codigo }</strong>.</p>" in contenido
	assert f"<p>Te has unido a la liga con codigo <strong>{ codigo }</strong>.</p>" not in contenido
	assert "<p>¡Esperamos que disfrutes de la experiencia a la que proximamente podras acceder!</p>" in contenido

def test_pagina_singup_crear_liga(cliente):

	respuesta=cliente.post("/singup", data={"usuario":"nacho98", "correo":"usuario@gmail.com", "nombre":"nacho",
											"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
											"codigo_final":"3YYZKP", "accion_liga":"crear"})

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Bienvenido/a</h1>" in contenido
	assert "<p>Gracias por registrarte en nuestra plataforma, Nacho.</p>" in contenido
	assert "<p>Se ha creado la nueva liga con codigo <strong>3YYZKP</strong>.</p>" in contenido
	assert "<p>Te has unido a la liga con codigo <strong>3YYZKP</strong>.</p>" not in contenido
	assert "<p>¡Esperamos que disfrutes de la experiencia a la que proximamente podras acceder!</p>" in contenido

def test_pagina_singup_unirse_liga(cliente):

	respuesta=cliente.post("/singup", data={"usuario":"nacho98", "correo":"usuario@gmail.com", "nombre":"nacho",
											"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
											"codigo_final":"3YYZKP", "accion_liga":"unirse"})

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Bienvenido/a</h1>" in contenido
	assert "<p>Gracias por registrarte en nuestra plataforma, Nacho.</p>" in contenido
	assert "<p>Se ha creado la nueva liga con codigo <strong>3YYZKP</strong>.</p>" not in contenido
	assert "<p>Te has unido a la liga con codigo <strong>3YYZKP</strong>.</p>" in contenido
	assert "<p>¡Esperamos que disfrutes de la experiencia a la que proximamente podras acceder!</p>" in contenido