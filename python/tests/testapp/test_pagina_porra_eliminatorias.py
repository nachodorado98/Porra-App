import json
import pytest
import copy
from datetime import datetime, timedelta

def test_pagina_porra_mejores_terceros_sin_login(cliente, conexion):

	respuesta=cliente.get("/porra/eliminatorias", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

def test_pagina_porra_eliminatorias_mejores_terceros_no_completados(cliente, conexion_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/porra/eliminatorias")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/porra/mejores_terceros"
		assert "<h1>Redirecting...</h1>" in contenido

@pytest.mark.parametrize(["dias"],
	[(2,),(22,),(5,),(13,),(25,),(1,),(0,)]
)
def test_pagina_porra_eliminatorias_porra_cerrada(cliente, conexion_usuario, porra_grupos, porra_mejores_terceros, dias):

	fecha_anterior=(datetime.now()-timedelta(days=dias)).strftime("%Y-%m-%d")

	conexion_usuario.insertarClaveValorMaestro("fecha_cierre_porra", fecha_anterior)

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra_grupos})

		cliente_abierto.post("/porra/mejores_terceros/guardar", json={"equipos":porra_mejores_terceros})

		respuesta=cliente_abierto.get("/porra/eliminatorias")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/porra"
		assert "<h1>Redirecting...</h1>" in contenido

@pytest.mark.parametrize(["dias"],
	[(2,),(22,),(5,),(13,),(25,),(1,)]
)
def test_pagina_porra_eliminatorias_abierta(cliente, conexion_usuario, porra_grupos, porra_mejores_terceros, dias):

	fecha_posterior=(datetime.now()+timedelta(days=dias)).strftime("%Y-%m-%d")

	conexion_usuario.insertarClaveValorMaestro("fecha_cierre_porra", fecha_posterior)

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra_grupos})

		cliente_abierto.post("/porra/mejores_terceros/guardar", json={"equipos":porra_mejores_terceros})

		respuesta=cliente_abierto.get("/porra/eliminatorias")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<div class="eliminatorias-wrapper">' in contenido
		assert '<div class="info-eliminatorias">' in contenido
		assert '<h1>Fase Eliminatoria' in contenido

def test_pagina_porra_eliminatorias(cliente, conexion_usuario, porra_grupos, porra_mejores_terceros):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra_grupos})

		cliente_abierto.post("/porra/mejores_terceros/guardar", json={"equipos":porra_mejores_terceros})

		respuesta=cliente_abierto.get("/porra/eliminatorias")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<div class="eliminatorias-wrapper">' in contenido
		assert '<div class="info-eliminatorias">' in contenido
		assert '<h1>Fase Eliminatoria' in contenido
		assert '<div class="bracket-scroll">' in contenido
		assert '<div class="tercer-puesto-wrapper">' in contenido
		assert '<div id="modalResumen" class="modal-overlay">' in contenido
		assert "<h2>Confirmar Eliminatorias</h2>" in contenido
		assert '<div id="modalCampeon" class="modal-campeon-overlay">' in contenido

def test_pagina_porra_eliminatorias_porra_ya_hecha(cliente, conexion_usuario, porra_grupos, porra_mejores_terceros, partidos_bracket):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra_grupos})

		cliente_abierto.post("/porra/mejores_terceros/guardar", json={"equipos":porra_mejores_terceros})

		cliente_abierto.post("/porra/eliminatorias/guardar", data={"elecciones_eliminatorias":json.dumps(partidos_bracket)})

		respuesta=cliente_abierto.get("/porra/eliminatorias")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/porra"
		assert "<h1>Redirecting...</h1>" in contenido

def test_pagina_porra_eliminatorias_guardar_sin_login(cliente, conexion):

	respuesta=cliente.post("/porra/eliminatorias/guardar", data={},  follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

def test_pagina_porra_eliminatorias_guardar_sin_porra_mejores_terceros(cliente, conexion_usuario, porra_grupos):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra_grupos})

		respuesta=cliente_abierto.post("/porra/eliminatorias/guardar", json={})

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/porra/mejores_terceros"
		assert "<h1>Redirecting...</h1>" in contenido

def test_pagina_porra_eliminatorias_guardar_sin_data(cliente, conexion_usuario, porra_grupos, porra_mejores_terceros):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra_grupos})

		cliente_abierto.post("/porra/mejores_terceros/guardar", json={"equipos":porra_mejores_terceros})

		respuesta=cliente_abierto.post("/porra/eliminatorias/guardar", data={})

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/porra/eliminatorias"
		assert "<h1>Redirecting...</h1>" in contenido

def test_pagina_porra_eliminatorias_guardar_data_erronea(cliente, conexion_usuario, porra_grupos, porra_mejores_terceros):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra_grupos})

		cliente_abierto.post("/porra/mejores_terceros/guardar", json={"equipos":porra_mejores_terceros})

		respuesta=cliente_abierto.post("/porra/eliminatorias/guardar", data={"elecciones_eliminatorias":"data"})

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/porra/eliminatorias"
		assert "<h1>Redirecting...</h1>" in contenido

@pytest.mark.parametrize(["partido"],
	[("M104",), ("M102",), ("M99",), ("M88",)]
)
def test_pagina_porra_eliminatorias_guardar_porra_falta_un_partido(cliente, conexion_usuario, porra_grupos, porra_mejores_terceros, partidos_bracket, partido):

	bracket=copy.deepcopy(partidos_bracket)

	bracket=[p for p in partidos_bracket if p["partido"]!=partido]

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra_grupos})

		cliente_abierto.post("/porra/mejores_terceros/guardar", json={"equipos":porra_mejores_terceros})
		
		respuesta=cliente_abierto.post("/porra/eliminatorias/guardar", data={"elecciones_eliminatorias":json.dumps(bracket)})

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/porra/eliminatorias"
		assert "<h1>Redirecting...</h1>" in contenido

def test_pagina_porra_eliminatorias_guardar_porra_partido_duplicado(cliente, conexion_usuario, porra_grupos, porra_mejores_terceros, partidos_bracket):

	bracket=copy.deepcopy(partidos_bracket)

	bracket.append(copy.deepcopy(bracket[0]))

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra_grupos})

		cliente_abierto.post("/porra/mejores_terceros/guardar", json={"equipos":porra_mejores_terceros})
		
		respuesta=cliente_abierto.post("/porra/eliminatorias/guardar", data={"elecciones_eliminatorias":json.dumps(bracket)})

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/porra/eliminatorias"
		assert "<h1>Redirecting...</h1>" in contenido

def test_pagina_porra_eliminatorias_guardar_porra_partido_no_valido(cliente, conexion_usuario, porra_grupos, porra_mejores_terceros, partidos_bracket):

	bracket=copy.deepcopy(partidos_bracket)

	bracket[0]["partido"]="M999"

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra_grupos})

		cliente_abierto.post("/porra/mejores_terceros/guardar", json={"equipos":porra_mejores_terceros})
		
		respuesta=cliente_abierto.post("/porra/eliminatorias/guardar", data={"elecciones_eliminatorias":json.dumps(bracket)})

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/porra/eliminatorias"
		assert "<h1>Redirecting...</h1>" in contenido

def test_pagina_porra_eliminatorias_guardar_porra_ronda_incorrecta(cliente, conexion_usuario, porra_grupos, porra_mejores_terceros, partidos_bracket):

	bracket=copy.deepcopy(partidos_bracket)

	partido=next(p for p in bracket if p["partido"]=="M89")

	partido["ronda"]="cuartos"

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra_grupos})

		cliente_abierto.post("/porra/mejores_terceros/guardar", json={"equipos":porra_mejores_terceros})
		
		respuesta=cliente_abierto.post("/porra/eliminatorias/guardar", data={"elecciones_eliminatorias":json.dumps(bracket)})

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/porra/eliminatorias"
		assert "<h1>Redirecting...</h1>" in contenido

def test_pagina_porra_eliminatorias_guardar_porra_ganador_no_juega_el_partido(cliente, conexion_usuario, porra_grupos, porra_mejores_terceros, partidos_bracket):

	bracket=copy.deepcopy(partidos_bracket)

	partido=next(p for p in bracket if p["partido"]=="M73")

	partido["ganador_id"]="seleccion-falsa"

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra_grupos})

		cliente_abierto.post("/porra/mejores_terceros/guardar", json={"equipos":porra_mejores_terceros})
		
		respuesta=cliente_abierto.post("/porra/eliminatorias/guardar", data={"elecciones_eliminatorias":json.dumps(bracket)})

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/porra/eliminatorias"
		assert "<h1>Redirecting...</h1>" in contenido

def test_pagina_porra_eliminatorias_guardar_porra_equipo_repetido_en_mismo_partido(cliente, conexion_usuario, porra_grupos, porra_mejores_terceros, partidos_bracket):

	bracket=copy.deepcopy(partidos_bracket)

	partido=next(p for p in bracket if p["partido"]=="M73")

	partido["equipo_2_id"]=partido["equipo_1_id"]

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra_grupos})

		cliente_abierto.post("/porra/mejores_terceros/guardar", json={"equipos":porra_mejores_terceros})
		
		respuesta=cliente_abierto.post("/porra/eliminatorias/guardar", data={"elecciones_eliminatorias":json.dumps(bracket)})

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/porra/eliminatorias"
		assert "<h1>Redirecting...</h1>" in contenido

def test_pagina_porra_eliminatorias_guardar_porra_campo_vacio(cliente, conexion_usuario, porra_grupos, porra_mejores_terceros, partidos_bracket):

	bracket=copy.deepcopy(partidos_bracket)

	partido=next(p for p in bracket if p["partido"]=="M73")

	partido["ganador_id"]=""

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra_grupos})

		cliente_abierto.post("/porra/mejores_terceros/guardar", json={"equipos":porra_mejores_terceros})
		
		respuesta=cliente_abierto.post("/porra/eliminatorias/guardar", data={"elecciones_eliminatorias":json.dumps(bracket)})

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/porra/eliminatorias"
		assert "<h1>Redirecting...</h1>" in contenido

def test_pagina_porra_eliminatorias_guardar_porra_16avos_no_coinciden_con_backend(cliente, conexion_usuario, porra_grupos, porra_mejores_terceros, partidos_bracket):

	bracket=copy.deepcopy(partidos_bracket)

	partido=next(p for p in bracket if p["partido"]=="M73")

	partido["equipo_1_id"]="seleccion-falsa"

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra_grupos})

		cliente_abierto.post("/porra/mejores_terceros/guardar", json={"equipos":porra_mejores_terceros})
		
		respuesta=cliente_abierto.post("/porra/eliminatorias/guardar", data={"elecciones_eliminatorias":json.dumps(bracket)})

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/porra/eliminatorias"
		assert "<h1>Redirecting...</h1>" in contenido

def test_pagina_porra_eliminatorias_guardar_porra_octavos_no_salen_de_los_ganadores_de_16avos(cliente, conexion_usuario, porra_grupos, porra_mejores_terceros, partidos_bracket):

	bracket=copy.deepcopy(partidos_bracket)

	partido=next(p for p in bracket if p["partido"]=="M89")

	partido["equipo_1_id"]="seleccion-falsa"

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra_grupos})

		cliente_abierto.post("/porra/mejores_terceros/guardar", json={"equipos":porra_mejores_terceros})
		
		respuesta=cliente_abierto.post("/porra/eliminatorias/guardar", data={"elecciones_eliminatorias":json.dumps(bracket)})

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/porra/eliminatorias"
		assert "<h1>Redirecting...</h1>" in contenido

def test_pagina_porra_eliminatorias_guardar_porra_cuartos_no_salen_de_los_ganadores_de_octavos(cliente, conexion_usuario, porra_grupos, porra_mejores_terceros, partidos_bracket):

	bracket=copy.deepcopy(partidos_bracket)

	partido=next(p for p in bracket if p["partido"]=="M97")

	partido["equipo_2_id"]="seleccion-falsa"

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra_grupos})

		cliente_abierto.post("/porra/mejores_terceros/guardar", json={"equipos":porra_mejores_terceros})
		
		respuesta=cliente_abierto.post("/porra/eliminatorias/guardar", data={"elecciones_eliminatorias":json.dumps(bracket)})

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/porra/eliminatorias"
		assert "<h1>Redirecting...</h1>" in contenido

def test_pagina_porra_eliminatorias_guardar_porra_semis_no_salen_de_los_ganadores_de_cuartos(cliente, conexion_usuario, porra_grupos, porra_mejores_terceros, partidos_bracket):

	bracket=copy.deepcopy(partidos_bracket)

	partido=next(p for p in bracket if p["partido"]=="M101")

	partido["equipo_1_id"]="seleccion-falsa"

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra_grupos})

		cliente_abierto.post("/porra/mejores_terceros/guardar", json={"equipos":porra_mejores_terceros})
		
		respuesta=cliente_abierto.post("/porra/eliminatorias/guardar", data={"elecciones_eliminatorias":json.dumps(bracket)})

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/porra/eliminatorias"
		assert "<h1>Redirecting...</h1>" in contenido

def test_pagina_porra_eliminatorias_guardar_porra_final_no_tiene_ganadores_de_semis(cliente, conexion_usuario, porra_grupos, porra_mejores_terceros, partidos_bracket):

	bracket=copy.deepcopy(partidos_bracket)

	partido=next(p for p in bracket if p["partido"]=="M104")

	partido["equipo_1_id"]="seleccion-falsa"

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra_grupos})

		cliente_abierto.post("/porra/mejores_terceros/guardar", json={"equipos":porra_mejores_terceros})
		
		respuesta=cliente_abierto.post("/porra/eliminatorias/guardar", data={"elecciones_eliminatorias":json.dumps(bracket)})

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/porra/eliminatorias"
		assert "<h1>Redirecting...</h1>" in contenido

def test_pagina_porra_eliminatorias_guardar_porra_tercer_puesto_no_tiene_perdedores_de_semis(cliente, conexion_usuario, porra_grupos, porra_mejores_terceros, partidos_bracket):

	bracket=copy.deepcopy(partidos_bracket)

	partido=next(p for p in bracket if p["partido"]=="M103")

	partido["equipo_1_id"]="seleccion-falsa"

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra_grupos})

		cliente_abierto.post("/porra/mejores_terceros/guardar", json={"equipos":porra_mejores_terceros})
		
		respuesta=cliente_abierto.post("/porra/eliminatorias/guardar", data={"elecciones_eliminatorias":json.dumps(bracket)})

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/porra/eliminatorias"
		assert "<h1>Redirecting...</h1>" in contenido

def test_pagina_porra_eliminatorias_guardar_porra_ganador_de_tercer_puesto_no_juega(cliente, conexion_usuario, porra_grupos, porra_mejores_terceros, partidos_bracket):

	bracket=copy.deepcopy(partidos_bracket)

	partido=next(p for p in bracket if p["partido"]=="M103")

	partido["ganador_id"]="seleccion-falsa"

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra_grupos})

		cliente_abierto.post("/porra/mejores_terceros/guardar", json={"equipos":porra_mejores_terceros})
		
		respuesta=cliente_abierto.post("/porra/eliminatorias/guardar", data={"elecciones_eliminatorias":json.dumps(bracket)})

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/porra/eliminatorias"
		assert "<h1>Redirecting...</h1>" in contenido

def test_pagina_porra_eliminatorias_guardar_porra_ganador_de_final_no_juega(cliente, conexion_usuario, porra_grupos, porra_mejores_terceros, partidos_bracket):

	bracket=copy.deepcopy(partidos_bracket)

	partido=next(p for p in bracket if p["partido"]=="M104")

	partido["ganador_id"]="seleccion-falsa"

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra_grupos})

		cliente_abierto.post("/porra/mejores_terceros/guardar", json={"equipos":porra_mejores_terceros})
		
		respuesta=cliente_abierto.post("/porra/eliminatorias/guardar", data={"elecciones_eliminatorias":json.dumps(bracket)})

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/porra/eliminatorias"
		assert "<h1>Redirecting...</h1>" in contenido

@pytest.mark.parametrize(["dias"],
	[(2,),(22,),(5,),(13,),(25,),(1,),(0,)]
)
def test_pagina_porra_eliminatorias_guardar_porra_cerrada(cliente, conexion_usuario, porra_grupos, porra_mejores_terceros, partidos_bracket, dias):

	fecha_anterior=(datetime.now()-timedelta(days=dias)).strftime("%Y-%m-%d")

	conexion_usuario.insertarClaveValorMaestro("fecha_cierre_porra", fecha_anterior)

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra_grupos})

		cliente_abierto.post("/porra/mejores_terceros/guardar", json={"equipos":porra_mejores_terceros})
		
		respuesta=cliente_abierto.post("/porra/eliminatorias/guardar", data={"elecciones_eliminatorias":json.dumps(partidos_bracket)})

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/porra"
		assert "<h1>Redirecting...</h1>" in contenido

@pytest.mark.parametrize(["dias"],
	[(2,),(22,),(5,),(13,),(25,),(1,)]
)
def test_pagina_porra_eliminatorias_guardar_porra_abierta(cliente, conexion_usuario, porra_grupos, porra_mejores_terceros, partidos_bracket, dias):

	fecha_posterior=(datetime.now()+timedelta(days=dias)).strftime("%Y-%m-%d")

	conexion_usuario.insertarClaveValorMaestro("fecha_cierre_porra", fecha_posterior)

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra_grupos})

		cliente_abierto.post("/porra/mejores_terceros/guardar", json={"equipos":porra_mejores_terceros})
		
		respuesta=cliente_abierto.post("/porra/eliminatorias/guardar", data={"elecciones_eliminatorias":json.dumps(partidos_bracket)})

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/porra/mi_porra"
		assert "<h1>Redirecting...</h1>" in contenido

		conexion_usuario.c.execute("SELECT * FROM eliminatorias_porra")

		partidos_eliminatorias=conexion_usuario.c.fetchall()

		assert len(partidos_eliminatorias)==32

		conexion_usuario.c.execute("SELECT Eliminatorias_Completadas, Porra_Completada FROM estado_porra")

		estado_porra=conexion_usuario.c.fetchone()

		assert estado_porra["eliminatorias_completadas"]
		assert estado_porra["porra_completada"]

def test_pagina_porra_eliminatorias_guardar_porra_correcto(cliente, conexion_usuario, porra_grupos, porra_mejores_terceros, partidos_bracket):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra_grupos})

		cliente_abierto.post("/porra/mejores_terceros/guardar", json={"equipos":porra_mejores_terceros})
		
		respuesta=cliente_abierto.post("/porra/eliminatorias/guardar", data={"elecciones_eliminatorias":json.dumps(partidos_bracket)})

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/porra/mi_porra"
		assert "<h1>Redirecting...</h1>" in contenido

		conexion_usuario.c.execute("SELECT * FROM eliminatorias_porra")

		partidos_eliminatorias=conexion_usuario.c.fetchall()

		assert len(partidos_eliminatorias)==32

		conexion_usuario.c.execute("SELECT Eliminatorias_Completadas, Porra_Completada FROM estado_porra")

		estado_porra=conexion_usuario.c.fetchone()

		assert estado_porra["eliminatorias_completadas"]
		assert estado_porra["porra_completada"]

def test_pagina_porra_eliminatorias_guardar_porra_ya_hecha(cliente, conexion_usuario, porra_grupos, porra_mejores_terceros, partidos_bracket):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra_grupos})

		cliente_abierto.post("/porra/mejores_terceros/guardar", json={"equipos":porra_mejores_terceros})

		cliente_abierto.post("/porra/eliminatorias/guardar", data={"elecciones_eliminatorias":json.dumps(partidos_bracket)})
		
		respuesta=cliente_abierto.post("/porra/eliminatorias/guardar", data={"elecciones_eliminatorias":json.dumps(partidos_bracket)})

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/porra"
		assert "<h1>Redirecting...</h1>" in contenido

		conexion_usuario.c.execute("SELECT * FROM eliminatorias_porra")

		partidos_eliminatorias=conexion_usuario.c.fetchall()

		assert len(partidos_eliminatorias)==32