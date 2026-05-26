import json
import pytest

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

def test_pagina_porra_mejores_terceros(cliente, conexion_usuario):

	porra={'A': ['seleccion-mexico', 'republica-checa', 'seleccion-republica-corea', 'seleccion-sudafrica'],
			'B': ['seleccion-suiza', 'canada', 'seleccion-bosnia-herzegovina', 'seleccion-qatar'],
			'C': ['seleccion-brasil', 'seleccion-marruecos', 'seleccion-escocia', 'haiti'],
			'D': ['seleccion-estados-unidos', 'seleccion-turquia', 'seleccion-paraguay', 'seleccion-australia'],
			'E': ['seleccion-alemania', 'seleccion-ecuador', 'seleccion-costa-marfil', 'curazao'],
			'F': ['seleccion-holanda', 'seleccion-japon', 'seleccion-suecia', 'seleccion-tunez'],
			'G': ['seleccion-belgica', 'seleccion-egipto', 'seleccion-iran', 'seleccion-nueva-zelanda'],
			'H': ['seleccion-espanola', 'seleccion-uruguay', 'seleccion-arabia-saudi', 'cabo-verde'],
			'I': ['seleccion-francia', 'seleccion-noruega', 'senegal', 'seleccion-iraq'],
			'J': ['seleccion-argentina', 'seleccion-austria', 'seleccion-argelia', 'jordania'],
			'K': ['seleccion-portugal', 'seleccion-colombia', 'rd-congo', 'seleccion-uzbekistan'],
			'L': ['seleccion-inglaterra', 'seleccion-croacia', 'seleccion-ghana', 'panama-seleccion']}

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra})

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