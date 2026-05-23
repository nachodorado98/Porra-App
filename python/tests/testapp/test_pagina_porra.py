def test_pagina_porra_sin_login(cliente, conexion):

	respuesta=cliente.get("/porra", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

def test_pagina_porra(cliente, conexion_usuario):

	respuesta=cliente.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Proximamente....</h1>" in contenido
	assert "<h2>¡Estamos trabajando para tener todo listo para esta gran cita!</h2>" in contenido