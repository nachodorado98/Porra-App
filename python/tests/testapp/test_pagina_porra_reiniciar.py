import pytest
import json
from datetime import datetime, timedelta

def test_pagina_porra_reiniciar_sin_login(cliente, conexion):

	respuesta=cliente.get("/porra/reiniciar", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

def test_pagina_porra_reiniciar_sin_iniciar(cliente, conexion_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		conexion_usuario.c.execute("SELECT * FROM grupo_equipos_porra")

		assert not conexion_usuario.c.fetchall()

		conexion_usuario.c.execute("SELECT * FROM mejores_terceros_porra")

		assert not conexion_usuario.c.fetchall()

		conexion_usuario.c.execute("SELECT * FROM eliminatorias_porra")

		assert not conexion_usuario.c.fetchall()

		conexion_usuario.c.execute("SELECT grupos_completados, mejores_terceros_completados, eliminatorias_completadas, porra_completada FROM estado_porra")

		estado=conexion_usuario.c.fetchone()

		assert not estado["grupos_completados"]
		assert not estado["mejores_terceros_completados"]
		assert not estado["eliminatorias_completadas"]
		assert not estado["porra_completada"]

		respuesta=cliente_abierto.get("/porra/reiniciar")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/porra"
		assert "<h1>Redirecting...</h1>" in contenido

		conexion_usuario.c.execute("SELECT * FROM grupo_equipos_porra")

		assert not conexion_usuario.c.fetchall()

		conexion_usuario.c.execute("SELECT * FROM mejores_terceros_porra")

		assert not conexion_usuario.c.fetchall()

		conexion_usuario.c.execute("SELECT * FROM eliminatorias_porra")

		assert not conexion_usuario.c.fetchall()

		conexion_usuario.c.execute("SELECT grupos_completados, mejores_terceros_completados, eliminatorias_completadas, porra_completada FROM estado_porra")

		estado=conexion_usuario.c.fetchone()

		assert not estado["grupos_completados"]
		assert not estado["mejores_terceros_completados"]
		assert not estado["eliminatorias_completadas"]
		assert not estado["porra_completada"]

@pytest.mark.parametrize(["dias"],
	[(2,),(22,),(5,),(13,),(25,),(1,),(0,)]
)
def test_pagina_porra_reiniciar_porra_cerrada(cliente, conexion_usuario, porra_grupos, porra_mejores_terceros, partidos_bracket, dias):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra_grupos})

		cliente_abierto.post("/porra/mejores_terceros/guardar", json={"equipos":porra_mejores_terceros})

		cliente_abierto.post("/porra/eliminatorias/guardar", data={"elecciones_eliminatorias":json.dumps(partidos_bracket)})

		conexion_usuario.c.execute("SELECT * FROM grupo_equipos_porra")

		assert conexion_usuario.c.fetchall()

		conexion_usuario.c.execute("SELECT * FROM mejores_terceros_porra")

		assert conexion_usuario.c.fetchall()

		conexion_usuario.c.execute("SELECT * FROM eliminatorias_porra")

		assert conexion_usuario.c.fetchall()

		conexion_usuario.c.execute("SELECT grupos_completados, mejores_terceros_completados, eliminatorias_completadas, porra_completada FROM estado_porra")

		estado=conexion_usuario.c.fetchone()

		assert estado["grupos_completados"]
		assert estado["mejores_terceros_completados"]
		assert estado["eliminatorias_completadas"]
		assert estado["porra_completada"]

		fecha_anterior=(datetime.now()-timedelta(days=dias)).strftime("%Y-%m-%d")

		conexion_usuario.insertarClaveValorMaestro("fecha_cierre_porra", fecha_anterior)

		respuesta=cliente_abierto.get("/porra/reiniciar")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/porra"
		assert "<h1>Redirecting...</h1>" in contenido

		conexion_usuario.c.execute("SELECT * FROM grupo_equipos_porra")

		assert conexion_usuario.c.fetchall()

		conexion_usuario.c.execute("SELECT * FROM mejores_terceros_porra")

		assert conexion_usuario.c.fetchall()

		conexion_usuario.c.execute("SELECT * FROM eliminatorias_porra")

		assert conexion_usuario.c.fetchall()

		conexion_usuario.c.execute("SELECT grupos_completados, mejores_terceros_completados, eliminatorias_completadas, porra_completada FROM estado_porra")

		estado=conexion_usuario.c.fetchone()

		assert estado["grupos_completados"]
		assert estado["mejores_terceros_completados"]
		assert estado["eliminatorias_completadas"]
		assert estado["porra_completada"]

@pytest.mark.parametrize(["dias"],
	[(2,),(22,),(5,),(13,),(25,),(1,)]
)
def test_pagina_porra_reiniciar_porra_abierta(cliente, conexion_usuario, porra_grupos, porra_mejores_terceros, partidos_bracket, dias):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra_grupos})

		cliente_abierto.post("/porra/mejores_terceros/guardar", json={"equipos":porra_mejores_terceros})

		cliente_abierto.post("/porra/eliminatorias/guardar", data={"elecciones_eliminatorias":json.dumps(partidos_bracket)})

		conexion_usuario.c.execute("SELECT * FROM grupo_equipos_porra")

		assert conexion_usuario.c.fetchall()

		conexion_usuario.c.execute("SELECT * FROM mejores_terceros_porra")

		assert conexion_usuario.c.fetchall()

		conexion_usuario.c.execute("SELECT * FROM eliminatorias_porra")

		assert conexion_usuario.c.fetchall()

		conexion_usuario.c.execute("SELECT grupos_completados, mejores_terceros_completados, eliminatorias_completadas, porra_completada FROM estado_porra")

		estado=conexion_usuario.c.fetchone()

		assert estado["grupos_completados"]
		assert estado["mejores_terceros_completados"]
		assert estado["eliminatorias_completadas"]
		assert estado["porra_completada"]

		fecha_posterior=(datetime.now()+timedelta(days=dias)).strftime("%Y-%m-%d")

		conexion_usuario.insertarClaveValorMaestro("fecha_cierre_porra", fecha_posterior)

		respuesta=cliente_abierto.get("/porra/reiniciar")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/porra"
		assert "<h1>Redirecting...</h1>" in contenido

		conexion_usuario.c.execute("SELECT * FROM grupo_equipos_porra")

		assert not conexion_usuario.c.fetchall()

		conexion_usuario.c.execute("SELECT * FROM mejores_terceros_porra")

		assert not conexion_usuario.c.fetchall()

		conexion_usuario.c.execute("SELECT * FROM eliminatorias_porra")

		assert not conexion_usuario.c.fetchall()

		conexion_usuario.c.execute("SELECT grupos_completados, mejores_terceros_completados, eliminatorias_completadas, porra_completada FROM estado_porra")

		estado=conexion_usuario.c.fetchone()

		assert not estado["grupos_completados"]
		assert not estado["mejores_terceros_completados"]
		assert not estado["eliminatorias_completadas"]
		assert not estado["porra_completada"]

def test_pagina_porra_reiniciar(cliente, conexion_usuario, porra_grupos, porra_mejores_terceros, partidos_bracket):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra_grupos})

		cliente_abierto.post("/porra/mejores_terceros/guardar", json={"equipos":porra_mejores_terceros})

		cliente_abierto.post("/porra/eliminatorias/guardar", data={"elecciones_eliminatorias":json.dumps(partidos_bracket)})

		conexion_usuario.c.execute("SELECT * FROM grupo_equipos_porra")

		assert conexion_usuario.c.fetchall()

		conexion_usuario.c.execute("SELECT * FROM mejores_terceros_porra")

		assert conexion_usuario.c.fetchall()

		conexion_usuario.c.execute("SELECT * FROM eliminatorias_porra")

		assert conexion_usuario.c.fetchall()

		conexion_usuario.c.execute("SELECT grupos_completados, mejores_terceros_completados, eliminatorias_completadas, porra_completada FROM estado_porra")

		estado=conexion_usuario.c.fetchone()

		assert estado["grupos_completados"]
		assert estado["mejores_terceros_completados"]
		assert estado["eliminatorias_completadas"]
		assert estado["porra_completada"]

		respuesta=cliente_abierto.get("/porra/reiniciar")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/porra"
		assert "<h1>Redirecting...</h1>" in contenido

		conexion_usuario.c.execute("SELECT * FROM grupo_equipos_porra")

		assert not conexion_usuario.c.fetchall()

		conexion_usuario.c.execute("SELECT * FROM mejores_terceros_porra")

		assert not conexion_usuario.c.fetchall()

		conexion_usuario.c.execute("SELECT * FROM eliminatorias_porra")

		assert not conexion_usuario.c.fetchall()

		conexion_usuario.c.execute("SELECT grupos_completados, mejores_terceros_completados, eliminatorias_completadas, porra_completada FROM estado_porra")

		estado=conexion_usuario.c.fetchone()

		assert not estado["grupos_completados"]
		assert not estado["mejores_terceros_completados"]
		assert not estado["eliminatorias_completadas"]
		assert not estado["porra_completada"]