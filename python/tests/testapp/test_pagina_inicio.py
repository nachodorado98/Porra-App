def test_pagina_inicio(cliente):

	respuesta=cliente.get("/")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

def test_pagina_health(cliente):

	respuesta=cliente.get("/health")

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "OK" in contenido