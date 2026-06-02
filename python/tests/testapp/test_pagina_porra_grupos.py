import json
import pytest

def test_pagina_porra_grupos_sin_login(cliente, conexion):

	respuesta=cliente.get("/porra/grupos", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

def test_pagina_porra_grupos(cliente, conexion_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/porra/grupos")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<div class="porra-grupos-wrapper">' in contenido
		assert '<div class="info-clasificacion">' in contenido
		assert '<h1 class="titulo-pagina">Fase de Grupos' in contenido
		assert '<div class="grupo-container">' in contenido

		for grupo in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']:

			assert f"<h2>Grupo {grupo}</h2>" in contenido
			assert f'<div class="grupo-lista" data-grupo="{grupo}">' in contenido

		assert '<div id="modalResumen" class="modal-overlay">' in contenido
		assert "<h2> Confirmar Clasificación Grupos </h2>" in contenido

def test_pagina_porra_grupos_porra_ya_hecha(cliente, conexion_usuario, porra_grupos):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra_grupos})

		respuesta=cliente_abierto.get("/porra/grupos")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/porra"
		assert "<h1>Redirecting...</h1>" in contenido

def test_pagina_porra_grupos_guardar_sin_login(cliente, conexion):

	respuesta=cliente.post("/porra/grupos/guardar", data={},  follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

def test_pagina_porra_grupos_guardar_sin_data(cliente, conexion_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.post("/porra/grupos/guardar", json={})

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/porra/grupos"
		assert "<h1>Redirecting...</h1>" in contenido

def test_pagina_porra_grupos_guardar_data_erronea(cliente, conexion_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.post("/porra/grupos/guardar", json={"data":"data"})

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/porra/grupos"
		assert "<h1>Redirecting...</h1>" in contenido

def test_pagina_porra_grupos_guardar_porra_error_grupo_faltante(cliente, conexion_usuario):

	porra={'A': ['seleccion-mexico', 'republica-checa', 'seleccion-republica-corea', 'seleccion-sudafrica'],
			'B': ['seleccion-suiza', 'canada', 'seleccion-bosnia-herzegovina', 'seleccion-qatar'],
			'C': ['seleccion-brasil', 'seleccion-marruecos', 'seleccion-escocia', 'haiti'],
			'D': ['seleccion-estados-unidos', 'seleccion-turquia', 'seleccion-paraguay', 'seleccion-australia'],
			'E': ['seleccion-alemania', 'seleccion-ecuador', 'seleccion-costa-marfil', 'curazao'],
			'F': ['seleccion-holanda', 'seleccion-japon', 'seleccion-suecia', 'seleccion-tunez'],
			'G': ['seleccion-belgica', 'seleccion-egipto', 'seleccion-iran', 'seleccion-nueva-zelanda'],
			'I': ['seleccion-francia', 'seleccion-noruega', 'senegal', 'seleccion-iraq'],
			'J': ['seleccion-argentina', 'seleccion-austria', 'seleccion-argelia', 'jordania'],
			'K': ['seleccion-portugal', 'seleccion-colombia', 'rd-congo', 'seleccion-uzbekistan'],
			'L': ['seleccion-inglaterra', 'seleccion-croacia', 'seleccion-ghana', 'panama-seleccion']}

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra})

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/porra/grupos"
		assert "<h1>Redirecting...</h1>" in contenido

@pytest.mark.parametrize(["porra_grupo"],
	[
		(['seleccion-espanola', 'seleccion-uruguay', 'seleccion-arabia-saudi'],),
		(['seleccion-espanola', 'seleccion-uruguay', 'seleccion-arabia-saudi', 'cabo-verde', 'seleccion-suiza', 'canada'],),
		(['seleccion-espanola'],),
		([],)
	]
)
def test_pagina_porra_grupos_guardar_porra_error_dimension_error(cliente, conexion_usuario, porra_grupo):

	porra={'A': ['seleccion-mexico', 'republica-checa', 'seleccion-republica-corea', 'seleccion-sudafrica'],
			'B': ['seleccion-suiza', 'canada', 'seleccion-bosnia-herzegovina', 'seleccion-qatar'],
			'C': ['seleccion-brasil', 'seleccion-marruecos', 'seleccion-escocia', 'haiti'],
			'D': ['seleccion-estados-unidos', 'seleccion-turquia', 'seleccion-paraguay', 'seleccion-australia'],
			'E': ['seleccion-alemania', 'seleccion-ecuador', 'seleccion-costa-marfil', 'curazao'],
			'F': ['seleccion-holanda', 'seleccion-japon', 'seleccion-suecia', 'seleccion-tunez'],
			'G': ['seleccion-belgica', 'seleccion-egipto', 'seleccion-iran', 'seleccion-nueva-zelanda'],
			'H': porra_grupo,
			'I': ['seleccion-francia', 'seleccion-noruega', 'senegal', 'seleccion-iraq'],
			'J': ['seleccion-argentina', 'seleccion-austria', 'seleccion-argelia', 'jordania'],
			'K': ['seleccion-portugal', 'seleccion-colombia', 'rd-congo', 'seleccion-uzbekistan'],
			'L': ['seleccion-inglaterra', 'seleccion-croacia', 'seleccion-ghana', 'panama-seleccion']}

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra})

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/porra/grupos"
		assert "<h1>Redirecting...</h1>" in contenido

@pytest.mark.parametrize(["porra_grupo"],
	[
		(['seleccion-espanola', 'seleccion-uruguay', 'seleccion-arabia-saudi', 'seleccion-suiza'],),
		(['seleccion-espanola', 'canada', 'seleccion-arabia-saudi', 'seleccion-suiza'],),
		(['seleccion-espanola', 'seleccion-uruguay', 'seleccion-arabia-saudi', 'equipo'],),
		(['equipo', 'seleccion-uruguay', 'seleccion-arabia-saudi', 'seleccion-suiza'],),
		(['seleccion-brasil', 'seleccion-marruecos', 'seleccion-escocia', 'haiti'],)
	]
)
def test_pagina_porra_grupos_guardar_porra_error_equipos_error(cliente, conexion_usuario, porra_grupo):

	porra={'A': ['seleccion-mexico', 'republica-checa', 'seleccion-republica-corea', 'seleccion-sudafrica'],
			'B': ['seleccion-suiza', 'canada', 'seleccion-bosnia-herzegovina', 'seleccion-qatar'],
			'C': ['seleccion-brasil', 'seleccion-marruecos', 'seleccion-escocia', 'haiti'],
			'D': ['seleccion-estados-unidos', 'seleccion-turquia', 'seleccion-paraguay', 'seleccion-australia'],
			'E': ['seleccion-alemania', 'seleccion-ecuador', 'seleccion-costa-marfil', 'curazao'],
			'F': ['seleccion-holanda', 'seleccion-japon', 'seleccion-suecia', 'seleccion-tunez'],
			'G': ['seleccion-belgica', 'seleccion-egipto', 'seleccion-iran', 'seleccion-nueva-zelanda'],
			'H': porra_grupo,
			'I': ['seleccion-francia', 'seleccion-noruega', 'senegal', 'seleccion-iraq'],
			'J': ['seleccion-argentina', 'seleccion-austria', 'seleccion-argelia', 'jordania'],
			'K': ['seleccion-portugal', 'seleccion-colombia', 'rd-congo', 'seleccion-uzbekistan'],
			'L': ['seleccion-inglaterra', 'seleccion-croacia', 'seleccion-ghana', 'panama-seleccion']}

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra})

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/porra/grupos"
		assert "<h1>Redirecting...</h1>" in contenido

def test_pagina_porra_grupos_guardar_porra_correcto(cliente, conexion_usuario, porra_grupos):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra_grupos})

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/porra/mejores_terceros"
		assert "<h1>Redirecting...</h1>" in contenido

		conexion_usuario.c.execute("SELECT * FROM grupo_equipos_porra ORDER BY Posicion ASC")

		equipos_grupos=conexion_usuario.c.fetchall()

		assert len(equipos_grupos)==48

		conexion_usuario.c.execute("SELECT Grupos_Completados FROM estado_porra")

		assert conexion_usuario.c.fetchone()["grupos_completados"]

def test_pagina_porra_grupos_guardar_porra_porra_ya_hecha(cliente, conexion_usuario, porra_grupos):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra_grupos})

		respuesta=cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra_grupos})

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/porra"
		assert "<h1>Redirecting...</h1>" in contenido

		conexion_usuario.c.execute("SELECT * FROM grupo_equipos_porra ORDER BY Posicion ASC")

		equipos_grupos=conexion_usuario.c.fetchall()

		assert len(equipos_grupos)==48