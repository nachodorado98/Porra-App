def test_pagina_forgot_password(cliente):

	respuesta=cliente.get("/forgot_password")

	contenido=respuesta.data.decode()

	respuesta.status_code==200
	assert "<h1>Recuperar contraseña</h1>" in contenido