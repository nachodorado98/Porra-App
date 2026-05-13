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
	[("hola",),("123456",),("HOLA",),("123HE?",),("KKGA03G5",)]
)
def test_pagina_verificar_codigo_no_valido(cliente, codigo):

	respuesta=cliente.get(f"/registro/verificar_codigo/{codigo}")

	contenido=respuesta.data.decode()

	respuesta.status_code==200

	diccionario_valido=json.loads(contenido)

	valido=diccionario_valido["valido"]

	assert not valido

@pytest.mark.parametrize(["codigo"],
	[("hola12",),("12345A",),("HOLAAA",),("123HE6",),("KKGA03",),("PLKTEO",)]
)
def test_pagina_verificar_codigo_valido(cliente, codigo):

	respuesta=cliente.get(f"/registro/verificar_codigo/{codigo}")

	contenido=respuesta.data.decode()

	respuesta.status_code==200

	diccionario_valido=json.loads(contenido)

	valido=diccionario_valido["valido"]

	assert valido