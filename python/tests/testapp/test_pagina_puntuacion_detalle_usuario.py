import json
import pytest
import os
from datetime import datetime, timedelta

def test_pagina_puntuacion_detalle_usuario_sin_login(cliente, conexion):

	respuesta=cliente.get("/puntuacion/detalle/nacho98", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

def test_pagina_puntuacion_detalle_usuario_usuario_no_existe(cliente, conexion_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/puntuacion/detalle/no_existo")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/porra"
		assert "<h1>Redirecting...</h1>" in contenido

def test_pagina_puntuacion_detalle_usuario_usuario_distinto(cliente, conexion_usuario, password_hash):

	conexion_usuario.insertarUsuario("golden", "correo@correo.es", password_hash, "nacho", "dorado", "3YYZKP")

	conexion_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/puntuacion/detalle/golden")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/porra"
		assert "<h1>Redirecting...</h1>" in contenido

@pytest.mark.parametrize(["dias"],
	[(2,),(22,),(5,),(13,),(25,),(1,)]
)
def test_pagina_puntuacion_detalle_usuario_porra_abierta(cliente, conexion_usuario, dias):

	fecha_posterior=(datetime.now()+timedelta(days=dias)).strftime("%Y-%m-%d")

	conexion_usuario.insertarClaveValorMaestro("fecha_cierre_porra", fecha_posterior)

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/puntuacion/detalle/nacho98")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/porra"
		assert "<h1>Redirecting...</h1>" in contenido

@pytest.mark.parametrize(["dias"],
	[(2,),(22,),(5,),(13,),(25,),(1,),(0,)]
)
def test_pagina_puntuacion_detalle_usuario_porra_cerrada_no_completada(cliente, conexion_usuario, dias):

	fecha_anterior=(datetime.now()-timedelta(days=dias)).strftime("%Y-%m-%d")

	conexion_usuario.insertarClaveValorMaestro("fecha_cierre_porra", fecha_anterior)

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/puntuacion/detalle/nacho98")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/porra"
		assert "<h1>Redirecting...</h1>" in contenido

def test_pagina_puntuacion_detalle_usuario_porra_cerrada_completada_sin_datos_reales(cliente, conexion_usuario, porra_grupos, porra_mejores_terceros, partidos_bracket):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra_grupos})

		cliente_abierto.post("/porra/mejores_terceros/guardar", json={"equipos":porra_mejores_terceros})
		
		cliente_abierto.post("/porra/eliminatorias/guardar", data={"elecciones_eliminatorias":json.dumps(partidos_bracket)})

	fecha_anterior=(datetime.now()-timedelta(days=10)).strftime("%Y-%m-%d")

	conexion_usuario.insertarClaveValorMaestro("fecha_cierre_porra", fecha_anterior)

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/puntuacion/detalle/nacho98")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/porra"
		assert "<h1>Redirecting...</h1>" in contenido

def test_pagina_puntuacion_detalle_usuario_porra_cerrada_completada_con_datos_reales_un_grupo(cliente, conexion_usuario, porra_grupos, porra_mejores_terceros, partidos_bracket):

	conexion_usuario.c.execute("""INSERT INTO grupo_equipos_real
									VALUES ('A', 'seleccion-republica-corea', 1), ('A', 'seleccion-mexico', 2), ('A', 'republica-checa', 3), ('A', 'seleccion-sudafrica', 4)""")

	conexion_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra_grupos})

		cliente_abierto.post("/porra/mejores_terceros/guardar", json={"equipos":porra_mejores_terceros})
		
		cliente_abierto.post("/porra/eliminatorias/guardar", data={"elecciones_eliminatorias":json.dumps(partidos_bracket)})

	fecha_anterior=(datetime.now()-timedelta(days=10)).strftime("%Y-%m-%d")

	conexion_usuario.insertarClaveValorMaestro("fecha_cierre_porra", fecha_anterior)

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/puntuacion/detalle/nacho98")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<div class="detalle-wrapper">' in contenido
		assert '<div class="info-clasificacion">' in contenido
		assert '<section class="detalle-section">' in contenido
		assert "Puntuación de nacho98" in contenido
		assert "nacho98_perfil.jpeg" not in contenido
		assert '<div class="resumen-total-puntuacion">' in contenido
		assert '<div class="resumen-total-card' in contenido
		assert '<div class="detalle-section-header">' in contenido
		assert "<h2>Fase de grupos</h2>" in contenido
		assert '<h3>Grupo A<span class="grupo-puntos">' in contenido
		assert '<h3>Grupo B<span class="grupo-puntos">' not in contenido
		assert '<h3>Grupo C<span class="grupo-puntos">' not in contenido
		assert '<h3>Grupo L<span class="grupo-puntos">' not in contenido
		assert "<h2>Mejores terceros</h2>" in contenido
		assert '<div class="detalle-terceros-grid">' not in contenido
		assert "<h3>Aún no hay mejores terceros oficiales</h3>" in contenido

def test_pagina_puntuacion_detalle_usuario_porra_cerrada_completada_con_datos_reales_dos_grupos(cliente, conexion_usuario, porra_grupos, porra_mejores_terceros, partidos_bracket):

	conexion_usuario.c.execute("""INSERT INTO grupo_equipos_real
									VALUES ('A', 'seleccion-republica-corea', 1), ('A', 'seleccion-mexico', 2), ('A', 'republica-checa', 3), ('A', 'seleccion-sudafrica', 4),
											('B', 'seleccion-bosnia-herzegovina', 1), ('B', 'canada', 2), ('B', 'seleccion-qatar', 3), ('B', 'seleccion-suiza', 4)""")

	conexion_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra_grupos})

		cliente_abierto.post("/porra/mejores_terceros/guardar", json={"equipos":porra_mejores_terceros})
		
		cliente_abierto.post("/porra/eliminatorias/guardar", data={"elecciones_eliminatorias":json.dumps(partidos_bracket)})

	fecha_anterior=(datetime.now()-timedelta(days=10)).strftime("%Y-%m-%d")

	conexion_usuario.insertarClaveValorMaestro("fecha_cierre_porra", fecha_anterior)

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/puntuacion/detalle/nacho98")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<div class="detalle-wrapper">' in contenido
		assert '<div class="info-clasificacion">' in contenido
		assert '<section class="detalle-section">' in contenido
		assert "Puntuación de nacho98" in contenido
		assert "nacho98_perfil.jpeg" not in contenido
		assert '<div class="resumen-total-puntuacion">' in contenido
		assert '<div class="resumen-total-card' in contenido
		assert '<div class="detalle-section-header">' in contenido
		assert "<h2>Fase de grupos</h2>" in contenido
		assert '<h3>Grupo A<span class="grupo-puntos">' in contenido
		assert '<h3>Grupo B<span class="grupo-puntos">' in contenido
		assert '<h3>Grupo C<span class="grupo-puntos">' not in contenido
		assert '<h3>Grupo L<span class="grupo-puntos">' not in contenido
		assert "<h2>Mejores terceros</h2>" in contenido
		assert '<div class="detalle-terceros-grid">' not in contenido
		assert "<h3>Aún no hay mejores terceros oficiales</h3>" in contenido

def test_pagina_puntuacion_detalle_usuario_porra_cerrada_completada_con_datos_reales_todos_grupos(cliente, conexion_usuario, porra_grupos, porra_mejores_terceros, partidos_bracket):

	conexion_usuario.c.execute("""INSERT INTO grupo_equipos_real
								VALUES ('A', 'seleccion-republica-corea', 1), ('A', 'seleccion-mexico', 2), ('A', 'republica-checa', 3), ('A', 'seleccion-sudafrica', 4),
										('B', 'seleccion-bosnia-herzegovina', 1), ('B', 'canada', 2), ('B', 'seleccion-qatar', 3), ('B', 'seleccion-suiza', 4),
										('C', 'seleccion-brasil', 1), ('C', 'seleccion-escocia', 2), ('C', 'haiti', 3), ('C', 'seleccion-marruecos', 4),
										('D', 'seleccion-australia', 1), ('D', 'seleccion-estados-unidos', 2), ('D', 'seleccion-paraguay', 3), ('D', 'seleccion-turquia', 4),
										('E', 'seleccion-alemania', 1), ('E', 'seleccion-costa-marfil', 2), ('E', 'curazao', 3), ('E', 'seleccion-ecuador', 4),
										('F', 'seleccion-japon', 1), ('F', 'seleccion-holanda', 2), ('F', 'seleccion-suecia', 3), ('F', 'seleccion-tunez', 4),
										('G', 'seleccion-belgica', 1), ('G', 'seleccion-egipto', 2), ('G', 'seleccion-iran', 3), ('G', 'seleccion-nueva-zelanda', 4),
										('H', 'seleccion-arabia-saudi', 1), ('H', 'cabo-verde', 2), ('H', 'seleccion-espanola', 3), ('H', 'seleccion-uruguay', 4),
										('I', 'seleccion-francia', 1), ('I', 'seleccion-iraq', 2), ('I', 'seleccion-noruega', 3), ('I', 'senegal', 4),
										('J', 'seleccion-argelia', 1), ('J', 'seleccion-argentina', 2), ('J', 'seleccion-austria', 3), ('J', 'jordania', 4),
										('K', 'seleccion-colombia', 1), ('K', 'seleccion-portugal', 2), ('K', 'rd-congo', 3), ('K', 'seleccion-uzbekistan', 4),
										('L', 'seleccion-croacia', 1), ('L', 'seleccion-ghana', 2), ('L', 'seleccion-inglaterra', 3), ('L', 'panama-seleccion', 4);""")

	conexion_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra_grupos})

		cliente_abierto.post("/porra/mejores_terceros/guardar", json={"equipos":porra_mejores_terceros})
		
		cliente_abierto.post("/porra/eliminatorias/guardar", data={"elecciones_eliminatorias":json.dumps(partidos_bracket)})

	fecha_anterior=(datetime.now()-timedelta(days=10)).strftime("%Y-%m-%d")

	conexion_usuario.insertarClaveValorMaestro("fecha_cierre_porra", fecha_anterior)

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/puntuacion/detalle/nacho98")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<div class="detalle-wrapper">' in contenido
		assert '<div class="info-clasificacion">' in contenido
		assert '<section class="detalle-section">' in contenido
		assert "Puntuación de nacho98" in contenido
		assert "nacho98_perfil.jpeg" not in contenido
		assert '<div class="resumen-total-puntuacion">' in contenido
		assert '<div class="resumen-total-card' in contenido
		assert '<div class="detalle-section-header">' in contenido
		assert "<h2>Fase de grupos</h2>" in contenido
		assert '<h3>Grupo A<span class="grupo-puntos">' in contenido
		assert '<h3>Grupo B<span class="grupo-puntos">' in contenido
		assert '<h3>Grupo C<span class="grupo-puntos">' in contenido
		assert '<h3>Grupo L<span class="grupo-puntos">' in contenido
		assert "<h2>Mejores terceros</h2>" in contenido
		assert '<div class="detalle-terceros-grid">' not in contenido
		assert "<h3>Aún no hay mejores terceros oficiales</h3>" in contenido

def test_pagina_puntuacion_detalle_usuario_con_imagen(cliente, conexion_usuario, porra_grupos, porra_mejores_terceros, partidos_bracket):

	conexion_usuario.c.execute("""INSERT INTO grupo_equipos_real
								VALUES ('A', 'seleccion-republica-corea', 1), ('A', 'seleccion-mexico', 2), ('A', 'republica-checa', 3), ('A', 'seleccion-sudafrica', 4),
										('B', 'seleccion-bosnia-herzegovina', 1), ('B', 'canada', 2), ('B', 'seleccion-qatar', 3), ('B', 'seleccion-suiza', 4),
										('C', 'seleccion-brasil', 1), ('C', 'seleccion-escocia', 2), ('C', 'haiti', 3), ('C', 'seleccion-marruecos', 4),
										('D', 'seleccion-australia', 1), ('D', 'seleccion-estados-unidos', 2), ('D', 'seleccion-paraguay', 3), ('D', 'seleccion-turquia', 4),
										('E', 'seleccion-alemania', 1), ('E', 'seleccion-costa-marfil', 2), ('E', 'curazao', 3), ('E', 'seleccion-ecuador', 4),
										('F', 'seleccion-japon', 1), ('F', 'seleccion-holanda', 2), ('F', 'seleccion-suecia', 3), ('F', 'seleccion-tunez', 4),
										('G', 'seleccion-belgica', 1), ('G', 'seleccion-egipto', 2), ('G', 'seleccion-iran', 3), ('G', 'seleccion-nueva-zelanda', 4),
										('H', 'seleccion-arabia-saudi', 1), ('H', 'cabo-verde', 2), ('H', 'seleccion-espanola', 3), ('H', 'seleccion-uruguay', 4),
										('I', 'seleccion-francia', 1), ('I', 'seleccion-iraq', 2), ('I', 'seleccion-noruega', 3), ('I', 'senegal', 4),
										('J', 'seleccion-argelia', 1), ('J', 'seleccion-argentina', 2), ('J', 'seleccion-austria', 3), ('J', 'jordania', 4),
										('K', 'seleccion-colombia', 1), ('K', 'seleccion-portugal', 2), ('K', 'rd-congo', 3), ('K', 'seleccion-uzbekistan', 4),
										('L', 'seleccion-croacia', 1), ('L', 'seleccion-ghana', 2), ('L', 'seleccion-inglaterra', 3), ('L', 'panama-seleccion', 4);""")

	conexion_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra_grupos})

		cliente_abierto.post("/porra/mejores_terceros/guardar", json={"equipos":porra_mejores_terceros})
		
		cliente_abierto.post("/porra/eliminatorias/guardar", data={"elecciones_eliminatorias":json.dumps(partidos_bracket)})

		ruta_imagen_test=os.path.join(os.getcwd(), "testapp", "imagenes_tests", "imagen_tests.jpeg")

		data={}

		with open(ruta_imagen_test, "rb") as imagen_file:
			
			data["imagen"]=(imagen_file, "imagen_tests.jpeg")

			cliente_abierto.post("/settings/actualizar_imagen_perfil", data=data, buffered=True, content_type="multipart/form-data")

	fecha_anterior=(datetime.now()-timedelta(days=10)).strftime("%Y-%m-%d")

	conexion_usuario.insertarClaveValorMaestro("fecha_cierre_porra", fecha_anterior)

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/puntuacion/detalle/nacho98")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<div class="detalle-wrapper">' in contenido
		assert '<div class="info-clasificacion">' in contenido
		assert '<section class="detalle-section">' in contenido
		assert "Puntuación de nacho98" in contenido
		assert "nacho98_perfil.jpeg" in contenido
		assert '<div class="resumen-total-puntuacion">' in contenido
		assert '<div class="resumen-total-card' in contenido
		assert '<div class="detalle-section-header">' in contenido
		assert "<h2>Fase de grupos</h2>" in contenido
		assert '<h3>Grupo A<span class="grupo-puntos">' in contenido
		assert '<h3>Grupo B<span class="grupo-puntos">' in contenido
		assert '<h3>Grupo C<span class="grupo-puntos">' in contenido
		assert '<h3>Grupo L<span class="grupo-puntos">' in contenido
		assert "<h2>Mejores terceros</h2>" in contenido
		assert '<div class="detalle-terceros-grid">' not in contenido

def test_pagina_puntuacion_detalle_usuario_porra_cerrada_completada_sin_mejores_terceros(cliente, conexion_usuario, porra_grupos, porra_mejores_terceros, partidos_bracket):

	conexion_usuario.c.execute("""INSERT INTO grupo_equipos_real
								VALUES ('A', 'seleccion-republica-corea', 1), ('A', 'seleccion-mexico', 2), ('A', 'republica-checa', 3), ('A', 'seleccion-sudafrica', 4),
										('B', 'seleccion-bosnia-herzegovina', 1), ('B', 'canada', 2), ('B', 'seleccion-qatar', 3), ('B', 'seleccion-suiza', 4),
										('C', 'seleccion-brasil', 1), ('C', 'seleccion-escocia', 2), ('C', 'haiti', 3), ('C', 'seleccion-marruecos', 4),
										('D', 'seleccion-australia', 1), ('D', 'seleccion-estados-unidos', 2), ('D', 'seleccion-paraguay', 3), ('D', 'seleccion-turquia', 4),
										('E', 'seleccion-alemania', 1), ('E', 'seleccion-costa-marfil', 2), ('E', 'curazao', 3), ('E', 'seleccion-ecuador', 4),
										('F', 'seleccion-japon', 1), ('F', 'seleccion-holanda', 2), ('F', 'seleccion-suecia', 3), ('F', 'seleccion-tunez', 4),
										('G', 'seleccion-belgica', 1), ('G', 'seleccion-egipto', 2), ('G', 'seleccion-iran', 3), ('G', 'seleccion-nueva-zelanda', 4),
										('H', 'seleccion-arabia-saudi', 1), ('H', 'cabo-verde', 2), ('H', 'seleccion-espanola', 3), ('H', 'seleccion-uruguay', 4),
										('I', 'seleccion-francia', 1), ('I', 'seleccion-iraq', 2), ('I', 'seleccion-noruega', 3), ('I', 'senegal', 4),
										('J', 'seleccion-argelia', 1), ('J', 'seleccion-argentina', 2), ('J', 'seleccion-austria', 3), ('J', 'jordania', 4),
										('K', 'seleccion-colombia', 1), ('K', 'seleccion-portugal', 2), ('K', 'rd-congo', 3), ('K', 'seleccion-uzbekistan', 4),
										('L', 'seleccion-croacia', 1), ('L', 'seleccion-ghana', 2), ('L', 'seleccion-inglaterra', 3), ('L', 'panama-seleccion', 4);""")

	conexion_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra_grupos})

		cliente_abierto.post("/porra/mejores_terceros/guardar", json={"equipos":porra_mejores_terceros})
		
		cliente_abierto.post("/porra/eliminatorias/guardar", data={"elecciones_eliminatorias":json.dumps(partidos_bracket)})

	fecha_anterior=(datetime.now()-timedelta(days=10)).strftime("%Y-%m-%d")

	conexion_usuario.insertarClaveValorMaestro("fecha_cierre_porra", fecha_anterior)

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/puntuacion/detalle/nacho98")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<div class="detalle-wrapper">' in contenido
		assert '<div class="info-clasificacion">' in contenido
		assert '<section class="detalle-section">' in contenido
		assert "Puntuación de nacho98" in contenido
		assert "nacho98_perfil.jpeg" not in contenido
		assert '<div class="resumen-total-puntuacion">' in contenido
		assert '<div class="resumen-total-card' in contenido
		assert '<div class="detalle-section-header">' in contenido
		assert "<h2>Fase de grupos</h2>" in contenido
		assert '<h3>Grupo A<span class="grupo-puntos">' in contenido
		assert '<h3>Grupo B<span class="grupo-puntos">' in contenido
		assert '<h3>Grupo C<span class="grupo-puntos">' in contenido
		assert '<h3>Grupo L<span class="grupo-puntos">' in contenido
		assert "<h2>Mejores terceros</h2>" in contenido
		assert '<div class="detalle-terceros-grid">' not in contenido
		assert "<h3>Aún no hay mejores terceros oficiales</h3>" in contenido

def test_pagina_puntuacion_detalle_usuario_porra_cerrada_completada_con_mejores_terceros(cliente, conexion_usuario, porra_grupos, porra_mejores_terceros, partidos_bracket):

	conexion_usuario.c.execute("""INSERT INTO grupo_equipos_real
								VALUES ('A', 'seleccion-republica-corea', 1), ('A', 'seleccion-mexico', 2), ('A', 'republica-checa', 3), ('A', 'seleccion-sudafrica', 4),
										('B', 'seleccion-bosnia-herzegovina', 1), ('B', 'canada', 2), ('B', 'seleccion-qatar', 3), ('B', 'seleccion-suiza', 4),
										('C', 'seleccion-brasil', 1), ('C', 'seleccion-escocia', 2), ('C', 'haiti', 3), ('C', 'seleccion-marruecos', 4),
										('D', 'seleccion-australia', 1), ('D', 'seleccion-estados-unidos', 2), ('D', 'seleccion-paraguay', 3), ('D', 'seleccion-turquia', 4),
										('E', 'seleccion-alemania', 1), ('E', 'seleccion-costa-marfil', 2), ('E', 'curazao', 3), ('E', 'seleccion-ecuador', 4),
										('F', 'seleccion-japon', 1), ('F', 'seleccion-holanda', 2), ('F', 'seleccion-suecia', 3), ('F', 'seleccion-tunez', 4),
										('G', 'seleccion-belgica', 1), ('G', 'seleccion-egipto', 2), ('G', 'seleccion-iran', 3), ('G', 'seleccion-nueva-zelanda', 4),
										('H', 'seleccion-arabia-saudi', 1), ('H', 'cabo-verde', 2), ('H', 'seleccion-espanola', 3), ('H', 'seleccion-uruguay', 4),
										('I', 'seleccion-francia', 1), ('I', 'seleccion-iraq', 2), ('I', 'seleccion-noruega', 3), ('I', 'senegal', 4),
										('J', 'seleccion-argelia', 1), ('J', 'seleccion-argentina', 2), ('J', 'seleccion-austria', 3), ('J', 'jordania', 4),
										('K', 'seleccion-colombia', 1), ('K', 'seleccion-portugal', 2), ('K', 'rd-congo', 3), ('K', 'seleccion-uzbekistan', 4),
										('L', 'seleccion-croacia', 1), ('L', 'seleccion-ghana', 2), ('L', 'seleccion-inglaterra', 3), ('L', 'panama-seleccion', 4);""")

	conexion_usuario.c.execute("""INSERT INTO mejores_terceros_real VALUES ('A', 'seleccion-republica-corea', 1),
																			('B', 'seleccion-bosnia-herzegovina', 2),
																			('C', 'seleccion-brasil', 3),
																			('D', 'seleccion-paraguay', 4),
																			('G', 'seleccion-iran', 5),
																			('K', 'seleccion-portugal', 6),
																			('L', 'seleccion-inglaterra', 7),
																			('H', 'seleccion-arabia-saudi', 8);""")
	conexion_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra_grupos})

		cliente_abierto.post("/porra/mejores_terceros/guardar", json={"equipos":porra_mejores_terceros})
		
		cliente_abierto.post("/porra/eliminatorias/guardar", data={"elecciones_eliminatorias":json.dumps(partidos_bracket)})

	fecha_anterior=(datetime.now()-timedelta(days=10)).strftime("%Y-%m-%d")

	conexion_usuario.insertarClaveValorMaestro("fecha_cierre_porra", fecha_anterior)

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/puntuacion/detalle/nacho98")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<div class="detalle-wrapper">' in contenido
		assert '<div class="info-clasificacion">' in contenido
		assert '<section class="detalle-section">' in contenido
		assert "Puntuación de nacho98" in contenido
		assert "nacho98_perfil.jpeg" not in contenido
		assert '<div class="resumen-total-puntuacion">' in contenido
		assert '<div class="resumen-total-card' in contenido
		assert '<div class="detalle-section-header">' in contenido
		assert "<h2>Fase de grupos</h2>" in contenido
		assert '<h3>Grupo A<span class="grupo-puntos">' in contenido
		assert '<h3>Grupo B<span class="grupo-puntos">' in contenido
		assert '<h3>Grupo C<span class="grupo-puntos">' in contenido
		assert '<h3>Grupo L<span class="grupo-puntos">' in contenido
		assert "<h2>Mejores terceros</h2>" in contenido
		assert '<div class="detalle-terceros-grid">' in contenido
		assert "<h3>Aún no hay mejores terceros oficiales</h3>" not in contenido