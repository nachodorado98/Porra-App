import json
import pytest
from datetime import datetime, timedelta

def test_pagina_porra_mejores_terceros_sin_login(cliente, conexion):

	respuesta=cliente.get("/porra/mejores_terceros", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

def test_pagina_porra_mejores_terceros_grupos_no_completados(cliente, conexion_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/porra/mejores_terceros")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/porra/grupos"
		assert "<h1>Redirecting...</h1>" in contenido

@pytest.mark.parametrize(["dias"],
	[(2,),(22,),(5,),(13,),(25,),(1,),(0,)]
)
def test_pagina_porra_mejores_terceros_porra_cerrada(cliente, conexion_usuario, porra_grupos, dias):

	fecha_anterior=(datetime.now()-timedelta(days=dias)).strftime("%Y-%m-%d")

	conexion_usuario.insertarClaveValorMaestro("fecha_cierre_porra", fecha_anterior)

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra_grupos})

		respuesta=cliente_abierto.get("/porra/mejores_terceros")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/porra"
		assert "<h1>Redirecting...</h1>" in contenido

@pytest.mark.parametrize(["dias"],
	[(2,),(22,),(5,),(13,),(25,),(1,)]
)
def test_pagina_porra_mejores_terceros_porra_abierta(cliente, conexion_usuario, porra_grupos, dias):

	fecha_posterior=(datetime.now()+timedelta(days=dias)).strftime("%Y-%m-%d")

	conexion_usuario.insertarClaveValorMaestro("fecha_cierre_porra", fecha_posterior)

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra_grupos})

		respuesta=cliente_abierto.get("/porra/mejores_terceros")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<div class="mejores-terceros-wrapper">' in contenido
		assert '<div class="info-terceros">' in contenido
		assert '<h1>Mejores Terceros' in contenido
		assert '<div class="terceros-grid">' in contenido
		assert '<div class="tercero-card"' in contenido

def test_pagina_porra_mejores_terceros(cliente, conexion_usuario, porra_grupos):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra_grupos})

		respuesta=cliente_abierto.get("/porra/mejores_terceros")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<div class="mejores-terceros-wrapper">' in contenido
		assert '<div class="info-terceros">' in contenido
		assert '<h1>Mejores Terceros' in contenido
		assert '<div class="terceros-grid">' in contenido
		assert '<div class="tercero-card"' in contenido

		for grupo in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']:

			assert f'<div class="grupo-badge">{grupo }</div>' in contenido

		assert '<div id="modalResumen" class="modal-overlay">' in contenido
		assert "<h2>Confirmar Mejores Terceros</h2>" in contenido

def test_pagina_porra_mejores_terceros_porra_ya_hecha(cliente, conexion_usuario, porra_grupos, porra_mejores_terceros):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra_grupos})

		cliente_abierto.post("/porra/mejores_terceros/guardar", json={"equipos":porra_mejores_terceros})

		respuesta=cliente_abierto.get("/porra/mejores_terceros")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/porra"
		assert "<h1>Redirecting...</h1>" in contenido

def test_pagina_porra_mejores_terceros_guardar_sin_login(cliente, conexion):

	respuesta=cliente.post("/porra/mejores_terceros/guardar", data={},  follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

def test_pagina_porra_mejores_terceros_guardar_sin_porra_grupos(cliente, conexion_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.post("/porra/mejores_terceros/guardar", json={})

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/porra/grupos"
		assert "<h1>Redirecting...</h1>" in contenido

def test_pagina_porra_mejores_terceros_guardar_sin_data(cliente, conexion_usuario, porra_grupos):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra_grupos})

		respuesta=cliente_abierto.post("/porra/mejores_terceros/guardar", json={})

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/porra/mejores_terceros"
		assert "<h1>Redirecting...</h1>" in contenido

def test_pagina_porra_mejores_terceros_guardar_data_erronea(cliente, conexion_usuario, porra_grupos):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra_grupos})

		respuesta=cliente_abierto.post("/porra/mejores_terceros/guardar", json={"data":"data"})

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/porra/mejores_terceros"
		assert "<h1>Redirecting...</h1>" in contenido

@pytest.mark.parametrize(["porra_terceros"],
    [
        ([{'equipo_id': 'seleccion-brasil', 'grupo': 'C'},
            {'equipo_id': 'seleccion-espanola', 'grupo': 'H'},
            {'equipo_id': 'seleccion-alemania', 'grupo': 'E'},
            {'equipo_id': 'seleccion-holanda', 'grupo': 'F'},
            {'equipo_id': 'seleccion-francia', 'grupo': 'I'},
            {'equipo_id': 'seleccion-argentina', 'grupo': 'J'},
            {'equipo_id': 'seleccion-inglaterra', 'grupo': 'L'}],),
        ([{'equipo_id': 'seleccion-brasil', 'grupo': 'C'},
            {'equipo_id': 'seleccion-espanola', 'grupo': 'H'},
            {'equipo_id': 'seleccion-inglaterra', 'grupo': 'L'}],),
        ([{'equipo_id': 'seleccion-brasil', 'grupo': 'C'}],),
        ([],),
        ([{'equipo_id': 'seleccion-brasil', 'grupo': 'C'},
            {'equipo_id': 'seleccion-espanola', 'grupo': 'H'},
            {'equipo_id': 'seleccion-alemania', 'grupo': 'E'},
            {'equipo_id': 'seleccion-holanda', 'grupo': 'F'},
            {'equipo_id': 'seleccion-francia', 'grupo': 'I'},
            {'equipo_id': 'seleccion-argentina', 'grupo': 'J'},
            {'equipo_id': 'seleccion-portugal', 'grupo': 'K'},
            {'equipo_id': 'seleccion-inglaterra', 'grupo': 'L'},
            {'equipo_id': 'seleccion-belgica', 'grupo': 'G'}],),
        ([{'equipo_id': 'seleccion-brasil', 'grupo': 'C'},
            {'equipo_id': 'seleccion-brasil', 'grupo': 'C'},
            {'equipo_id': 'seleccion-brasil', 'grupo': 'C'},
            {'equipo_id': 'seleccion-brasil', 'grupo': 'C'},
            {'equipo_id': 'seleccion-brasil', 'grupo': 'C'},
            {'equipo_id': 'seleccion-brasil', 'grupo': 'C'},
            {'equipo_id': 'seleccion-brasil', 'grupo': 'C'},
            {'equipo_id': 'seleccion-brasil', 'grupo': 'C'}],),
        ([{'equipo_id': 'seleccion-brasil', 'grupo': 'C'},
            {'equipo_id': 'seleccion-espanola', 'grupo': 'H'},
            {'equipo_id': 'seleccion-alemania', 'grupo': 'E'},
            {'equipo_id': 'seleccion-holanda', 'grupo': 'F'},
            {'equipo_id': 'seleccion-francia', 'grupo': 'I'},
            {'equipo_id': 'seleccion-argentina', 'grupo': 'J'},
            {'equipo_id': 'seleccion-portugal', 'grupo': 'K'},
            {'equipo_id': 'seleccion-brasil', 'grupo': 'C'}],),
        ([{'equipo_id': 'seleccion-brasil', 'grupo': 'C'},
            {'equipo_id': 'seleccion-espanola', 'grupo': 'H'},
            {'equipo_id': 'seleccion-alemania', 'grupo': 'E'},
            {'equipo_id': 'seleccion-holanda', 'grupo': 'F'},
            {'equipo_id': 'seleccion-francia', 'grupo': 'I'},
            {'equipo_id': 'seleccion-argentina', 'grupo': 'J'},
            {'equipo_id': 'seleccion-portugal', 'grupo': 'K'},
            {'equipo_id': 'seleccion-brasil', 'grupo': 'L'}],),
        ([{'equipo_id': 'seleccion-brasil', 'grupo': 'C'},
            {'equipo_id': 'seleccion-espanola', 'grupo': 'H'},
            {'equipo_id': 'seleccion-alemania', 'grupo': 'E'},
            {'equipo_id': 'seleccion-holanda', 'grupo': 'F'},
            {'equipo_id': 'seleccion-francia', 'grupo': 'I'},
            {'equipo_id': 'seleccion-argentina', 'grupo': 'J'},
            {'equipo_id': 'seleccion-portugal', 'grupo': 'K'},
            {'equipo_id': 'seleccion-inglaterra', 'grupo': 'C'}],)
    ]
)
def test_pagina_porra_mejores_terceros_guardar_dimension_error(cliente, conexion_usuario, porra_grupos, porra_terceros):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra_grupos})

		respuesta=cliente_abierto.post("/porra/mejores_terceros/guardar", json={"equipos":porra_terceros})

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/porra/mejores_terceros"
		assert "<h1>Redirecting...</h1>" in contenido

@pytest.mark.parametrize(["porra_terceros"],
    [
        ([{'equipo_id': 'seleccion-brasil', 'grupo': 'A'},
            {'equipo_id': 'seleccion-espanola', 'grupo': 'H'},
            {'equipo_id': 'seleccion-alemania', 'grupo': 'E'},
            {'equipo_id': 'seleccion-holanda', 'grupo': 'F'},
            {'equipo_id': 'seleccion-francia', 'grupo': 'I'},
            {'equipo_id': 'seleccion-argentina', 'grupo': 'J'},
            {'equipo_id': 'seleccion-portugal', 'grupo': 'K'},
            {'equipo_id': 'seleccion-inglaterra', 'grupo': 'L'}],),
        ([{'equipo_id': 'seleccion-marruecos', 'grupo': 'C'},
            {'equipo_id': 'seleccion-espanola', 'grupo': 'H'},
            {'equipo_id': 'seleccion-alemania', 'grupo': 'E'},
            {'equipo_id': 'seleccion-holanda', 'grupo': 'F'},
            {'equipo_id': 'seleccion-francia', 'grupo': 'I'},
            {'equipo_id': 'seleccion-argentina', 'grupo': 'J'},
            {'equipo_id': 'seleccion-portugal', 'grupo': 'K'},
            {'equipo_id': 'seleccion-inglaterra', 'grupo': 'L'}],),
        ([{'equipo_id': 'seleccion-marruecos', 'grupo': 'C'},
            {'equipo_id': 'seleccion-espanola', 'grupo': 'H'},
            {'equipo_id': 'seleccion-alemania', 'grupo': 'E'},
            {'equipo_id': 'seleccion-holanda', 'grupo': 'F'},
            {'equipo_id': 'seleccion-francia', 'grupo': 'I'},
            {'equipo_id': 'seleccion-argentina', 'grupo': 'J'},
            {'equipo_id': 'seleccion-portugal', 'grupo': 'K'},
            {'equipo_id': 'seleccion-inglaterra', 'grupo': 'Z'}],)
    ]
)
def test_pagina_porra_mejores_terceros_guardar_equipos_error(cliente, conexion_usuario, porra_grupos, porra_terceros):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra_grupos})

		respuesta=cliente_abierto.post("/porra/mejores_terceros/guardar", json={"equipos":porra_terceros})

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/porra/mejores_terceros"
		assert "<h1>Redirecting...</h1>" in contenido

@pytest.mark.parametrize(["dias"],
	[(2,),(22,),(5,),(13,),(25,),(1,),(0,)]
)
def test_pagina_porra_mejores_terceros_guardar_porra_cerrada(cliente, conexion_usuario, porra_grupos, porra_mejores_terceros, dias):

	fecha_anterior=(datetime.now()-timedelta(days=dias)).strftime("%Y-%m-%d")

	conexion_usuario.insertarClaveValorMaestro("fecha_cierre_porra", fecha_anterior)

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra_grupos})

		respuesta=cliente_abierto.post("/porra/mejores_terceros/guardar", json={"equipos":porra_mejores_terceros})

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/porra"
		assert "<h1>Redirecting...</h1>" in contenido

@pytest.mark.parametrize(["dias"],
	[(2,),(22,),(5,),(13,),(25,),(1,)]
)
def test_pagina_porra_mejores_terceros_guardar_porra_abierta(cliente, conexion_usuario, porra_grupos, porra_mejores_terceros, dias):

	fecha_posterior=(datetime.now()+timedelta(days=dias)).strftime("%Y-%m-%d")

	conexion_usuario.insertarClaveValorMaestro("fecha_cierre_porra", fecha_posterior)

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra_grupos})

		respuesta=cliente_abierto.post("/porra/mejores_terceros/guardar", json={"equipos":porra_mejores_terceros})

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/porra/eliminatorias"
		assert "<h1>Redirecting...</h1>" in contenido

		conexion_usuario.c.execute("SELECT * FROM mejores_terceros_porra ORDER BY Orden ASC")

		equipos_mejores_terceros=conexion_usuario.c.fetchall()

		assert len(equipos_mejores_terceros)==8

		conexion_usuario.c.execute("SELECT Mejores_Terceros_Completados FROM estado_porra")

		assert conexion_usuario.c.fetchone()["mejores_terceros_completados"]

@pytest.mark.parametrize(["porra_terceros"],
    [
        ([{'equipo_id': 'seleccion-brasil', 'grupo': 'C'},
            {'equipo_id': 'seleccion-espanola', 'grupo': 'H'},
            {'equipo_id': 'seleccion-alemania', 'grupo': 'E'},
            {'equipo_id': 'seleccion-holanda', 'grupo': 'F'},
            {'equipo_id': 'seleccion-francia', 'grupo': 'I'},
            {'equipo_id': 'seleccion-argentina', 'grupo': 'J'},
            {'equipo_id': 'seleccion-portugal', 'grupo': 'K'},
            {'equipo_id': 'seleccion-inglaterra', 'grupo': 'L'}],),
        ([{'equipo_id': 'seleccion-mexico', 'grupo': 'A'},
            {'equipo_id': 'seleccion-espanola', 'grupo': 'H'},
            {'equipo_id': 'seleccion-alemania', 'grupo': 'E'},
            {'equipo_id': 'seleccion-holanda', 'grupo': 'F'},
            {'equipo_id': 'seleccion-francia', 'grupo': 'I'},
            {'equipo_id': 'seleccion-argentina', 'grupo': 'J'},
            {'equipo_id': 'seleccion-portugal', 'grupo': 'K'},
            {'equipo_id': 'seleccion-inglaterra', 'grupo': 'L'}],),
        ([{'equipo_id': 'seleccion-mexico', 'grupo': 'A'},
            {'equipo_id': 'seleccion-espanola', 'grupo': 'H'},
            {'equipo_id': 'seleccion-turquia', 'grupo': 'D'},
            {'equipo_id': 'seleccion-holanda', 'grupo': 'F'},
            {'equipo_id': 'seleccion-francia', 'grupo': 'I'},
            {'equipo_id': 'seleccion-argentina', 'grupo': 'J'},
            {'equipo_id': 'seleccion-portugal', 'grupo': 'K'},
            {'equipo_id': 'seleccion-inglaterra', 'grupo': 'L'}],),
        ([{'equipo_id': 'seleccion-mexico', 'grupo': 'A'},
            {'equipo_id': 'seleccion-espanola', 'grupo': 'H'},
            {'equipo_id': 'seleccion-turquia', 'grupo': 'D'},
            {'equipo_id': 'seleccion-holanda', 'grupo': 'F'},
            {'equipo_id': 'seleccion-francia', 'grupo': 'I'},
            {'equipo_id': 'seleccion-argentina', 'grupo': 'J'},
            {'equipo_id': 'seleccion-suiza', 'grupo': 'B'},
            {'equipo_id': 'seleccion-belgica', 'grupo': 'G'}],),
    ]
)
def test_pagina_porra_mejores_terceros_guardar_porra_correcto(cliente, conexion_usuario, porra_grupos, porra_terceros):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra_grupos})

		respuesta=cliente_abierto.post("/porra/mejores_terceros/guardar", json={"equipos":porra_terceros})

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/porra/eliminatorias"
		assert "<h1>Redirecting...</h1>" in contenido

		conexion_usuario.c.execute("SELECT * FROM mejores_terceros_porra ORDER BY Orden ASC")

		equipos_mejores_terceros=conexion_usuario.c.fetchall()

		assert len(equipos_mejores_terceros)==8

		conexion_usuario.c.execute("SELECT Mejores_Terceros_Completados FROM estado_porra")

		assert conexion_usuario.c.fetchone()["mejores_terceros_completados"]

def test_pagina_porra_mejores_terceros_guardar_porra_ya_hecha(cliente, conexion_usuario, porra_grupos, porra_mejores_terceros):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra_grupos})

		cliente_abierto.post("/porra/mejores_terceros/guardar", json={"equipos":porra_mejores_terceros})

		respuesta=cliente_abierto.post("/porra/mejores_terceros/guardar", json={"equipos":porra_mejores_terceros})

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/porra"
		assert "<h1>Redirecting...</h1>" in contenido

		conexion_usuario.c.execute("SELECT * FROM mejores_terceros_porra ORDER BY Orden ASC")

		equipos_mejores_terceros=conexion_usuario.c.fetchall()

		assert len(equipos_mejores_terceros)==8