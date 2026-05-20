import pytest

def test_pagina_inicio_sin_login(cliente, conexion):

	respuesta=cliente.get("/inicio", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

@pytest.mark.parametrize(["usuario"],
	[("nacho",),("nacho98",),("usuario_correcto",), ("amanda",)]
)
def test_pagina_inicio_con_login_usuario_no_existe(cliente, conexion, usuario):

	respuesta=cliente.post("/login", data={"usuario": "nacho", "contrasena": "Ab!CdEfGhIJK3LMN"})

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location=="/"
	assert "<h1>Redirecting...</h1>" in contenido

@pytest.mark.parametrize(["contrasena"],
	[("213214hhj&&ff",),("354354vff",),("2223321",), ("fdfgh&&55fjfkAfh",)]
)
def test_pagina_inicio_con_login_usuario_existe_contrasena_error(cliente, conexion, contrasena):

	respuesta=cliente.post("/singup", data={"usuario":"nacho98", "correo":"usuario@gmail.com", "nombre":"nacho",
											"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
											"codigo_final":"3YYZKP", "accion_liga":"crear"})

	respuesta=cliente.post("/login", data={"usuario": "nacho98", "contrasena": contrasena})

	contenido=respuesta.data.decode()

	assert respuesta.status_code==302
	assert respuesta.location=="/"
	assert "<h1>Redirecting...</h1>" in contenido

def test_pagina_inicio_con_login(cliente, conexion):

	respuesta=cliente.post("/singup", data={"usuario":"nacho98", "correo":"usuario@gmail.com", "nombre":"nacho",
											"apellido":"dorado", "contrasena":"Ab!CdEfGhIJK3LMN",
											"codigo_final":"3YYZKP", "accion_liga":"crear"})

	respuesta=cliente.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "Bienvenido de nuevo, Nacho. Tu codigo de liga es: 3YYZKP" in contenido