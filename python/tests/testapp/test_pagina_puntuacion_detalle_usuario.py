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

		assert "<h2>Eliminatorias</h2>" in contenido
		assert '<div class="detalle-ronda">' not in contenido
		assert '<h3>Aún no hay eliminatorias oficiales</h3>' in contenido
		assert '<div class="bonus-eliminatorias">' not in contenido
		assert '<div class="bonus-card bonus-campeon">' not in contenido
		assert '<div class="bonus-card bonus-final">' not in contenido
		assert '<h3>Dieciseisavos</h3>' not in contenido
		assert '<div class="detalle-eliminatoria-card pendiente">' not in contenido
		assert '<div class="detalle-eliminatoria-card fallada">' not in contenido
		assert 'Clasificado para 16avos' not in contenido
		assert '<h3>Octavos</h3>' not in contenido
		assert 'Clasificado para Octavos' not in contenido

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

		assert "<h2>Eliminatorias</h2>" in contenido
		assert '<div class="detalle-ronda">' not in contenido
		assert '<h3>Aún no hay eliminatorias oficiales</h3>' in contenido
		assert '<div class="bonus-eliminatorias">' not in contenido
		assert '<div class="bonus-card bonus-campeon">' not in contenido
		assert '<div class="bonus-card bonus-final">' not in contenido
		assert '<h3>Dieciseisavos</h3>' not in contenido
		assert '<div class="detalle-eliminatoria-card pendiente">' not in contenido
		assert '<div class="detalle-eliminatoria-card fallada">' not in contenido
		assert 'Clasificado para 16avos' not in contenido
		assert '<h3>Octavos</h3>' not in contenido
		assert 'Clasificado para Octavos' not in contenido

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

		assert "<h2>Eliminatorias</h2>" in contenido
		assert '<div class="detalle-ronda">' not in contenido
		assert '<h3>Aún no hay eliminatorias oficiales</h3>' in contenido
		assert '<div class="bonus-eliminatorias">' not in contenido
		assert '<div class="bonus-card bonus-campeon">' not in contenido
		assert '<div class="bonus-card bonus-final">' not in contenido
		assert '<h3>Dieciseisavos</h3>' not in contenido
		assert '<div class="detalle-eliminatoria-card pendiente">' not in contenido
		assert '<div class="detalle-eliminatoria-card fallada">' not in contenido
		assert 'Clasificado para 16avos' not in contenido
		assert '<h3>Octavos</h3>' not in contenido
		assert 'Clasificado para Octavos' not in contenido

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

		assert "<h2>Eliminatorias</h2>" in contenido
		assert '<div class="detalle-ronda">' not in contenido
		assert '<h3>Aún no hay eliminatorias oficiales</h3>' in contenido
		assert '<div class="bonus-eliminatorias">' not in contenido
		assert '<div class="bonus-card bonus-campeon">' not in contenido
		assert '<div class="bonus-card bonus-final">' not in contenido
		assert '<h3>Dieciseisavos</h3>' not in contenido
		assert '<div class="detalle-eliminatoria-card pendiente">' not in contenido
		assert '<div class="detalle-eliminatoria-card fallada">' not in contenido
		assert 'Clasificado para 16avos' not in contenido
		assert '<h3>Octavos</h3>' not in contenido
		assert 'Clasificado para Octavos' not in contenido

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

		assert "<h2>Eliminatorias</h2>" in contenido
		assert '<div class="detalle-ronda">' not in contenido
		assert '<h3>Aún no hay eliminatorias oficiales</h3>' in contenido
		assert '<div class="bonus-eliminatorias">' not in contenido
		assert '<div class="bonus-card bonus-campeon">' not in contenido
		assert '<div class="bonus-card bonus-final">' not in contenido
		assert '<h3>Dieciseisavos</h3>' not in contenido
		assert '<div class="detalle-eliminatoria-card pendiente">' not in contenido
		assert '<div class="detalle-eliminatoria-card fallada">' not in contenido
		assert 'Clasificado para 16avos' not in contenido
		assert '<h3>Octavos</h3>' not in contenido
		assert 'Clasificado para Octavos' not in contenido

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

		assert "<h2>Eliminatorias</h2>" in contenido
		assert '<div class="detalle-ronda">' not in contenido
		assert '<h3>Aún no hay eliminatorias oficiales</h3>' in contenido
		assert '<div class="bonus-eliminatorias">' not in contenido
		assert '<div class="bonus-card bonus-campeon">' not in contenido
		assert '<div class="bonus-card bonus-final">' not in contenido
		assert '<h3>Dieciseisavos</h3>' not in contenido
		assert '<div class="detalle-eliminatoria-card pendiente">' not in contenido
		assert '<div class="detalle-eliminatoria-card fallada">' not in contenido
		assert 'Clasificado para 16avos' not in contenido
		assert '<h3>Octavos</h3>' not in contenido
		assert 'Clasificado para Octavos' not in contenido

def test_pagina_puntuacion_detalle_usuario_porra_cerrada_completada_sin_eliminatorias(cliente, conexion_usuario, porra_grupos, porra_mejores_terceros, partidos_bracket):

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

		assert "<h2>Eliminatorias</h2>" in contenido
		assert '<div class="detalle-ronda">' not in contenido
		assert '<h3>Aún no hay eliminatorias oficiales</h3>' in contenido
		assert '<div class="bonus-eliminatorias">' not in contenido
		assert '<div class="bonus-card bonus-campeon">' not in contenido
		assert '<div class="bonus-card bonus-final">' not in contenido
		assert '<h3>Dieciseisavos</h3>' not in contenido
		assert '<div class="detalle-eliminatoria-card acertada">' not in contenido
		assert '<div class="detalle-eliminatoria-card pendiente">' not in contenido
		assert '<div class="detalle-eliminatoria-card fallada">' not in contenido
		assert 'Clasificado para 16avos' not in contenido
		assert '<h3>Octavos</h3>' not in contenido
		assert 'Clasificado para Octavos' not in contenido
		assert '<h3>Cuartos</h3>' not in contenido
		assert 'Clasificado para Cuartos' not in contenido
		assert '<h3>Semifinales</h3>' not in contenido
		assert 'Clasificado para Semifinales' not in contenido
		assert '<h3>Tercer puesto</h3>' not in contenido
		assert 'Clasificado para Tercer_Puesto' not in contenido
		assert '<h3>Final</h3>' not in contenido
		assert 'Clasificado para Final' not in contenido

def test_pagina_puntuacion_detalle_usuario_porra_cerrada_completada_un_partido_una_ronda(cliente, conexion_usuario, porra_grupos, porra_mejores_terceros, partidos_bracket):

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

	conexion_usuario.c.execute("""INSERT INTO eliminatorias_real VALUES('dieciseisavos', 'M73', 'republica-checa', 'canada', 'republica-checa');""")

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
		assert "<h2>Eliminatorias</h2>" in contenido
		assert '<div class="detalle-ronda">' in contenido
		assert '<h3>Aún no hay eliminatorias oficiales</h3>' not in contenido
		assert '<div class="bonus-eliminatorias">' not in contenido
		assert '<div class="bonus-card bonus-campeon">' not in contenido
		assert '<div class="bonus-card bonus-final">' not in contenido
		assert '<h3>Dieciseisavos</h3>' in contenido
		assert '<div class="detalle-eliminatoria-card acertada">' in contenido
		assert '<div class="detalle-eliminatoria-card pendiente">' in contenido
		assert '<div class="detalle-eliminatoria-card fallada">' not in contenido
		assert 'Clasificado para 16avos' in contenido
		assert '<h3>Octavos</h3>' not in contenido
		assert 'Clasificado para Octavos' not in contenido
		assert '<h3>Cuartos</h3>' not in contenido
		assert 'Clasificado para Cuartos' not in contenido
		assert '<h3>Semifinales</h3>' not in contenido
		assert 'Clasificado para Semifinales' not in contenido
		assert '<h3>Tercer puesto</h3>' not in contenido
		assert 'Clasificado para Tercer_Puesto' not in contenido
		assert '<h3>Final</h3>' not in contenido
		assert 'Clasificado para Final' not in contenido

def test_pagina_puntuacion_detalle_usuario_porra_cerrada_completada_una_ronda(cliente, conexion_usuario, porra_grupos, porra_mejores_terceros, partidos_bracket):

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

	conexion_usuario.c.execute("""INSERT INTO eliminatorias_real VALUES('dieciseisavos', 'M73', 'republica-checa', 'canada', 'republica-checa'),
										('dieciseisavos', 'M74', 'seleccion-alemania', 'seleccion-paraguay', 'seleccion-alemania'),
										('dieciseisavos', 'M75', 'seleccion-holanda', 'seleccion-marruecos', 'seleccion-holanda'),
										('dieciseisavos', 'M76', 'seleccion-brasil', 'seleccion-japon', 'seleccion-brasil'),
										('dieciseisavos', 'M77', 'seleccion-francia', 'seleccion-suecia', 'seleccion-francia'),
										('dieciseisavos', 'M78', 'seleccion-ecuador', 'seleccion-noruega', 'seleccion-noruega'),
										('dieciseisavos', 'M79', 'seleccion-mexico', 'seleccion-arabia-saudi', 'seleccion-mexico'),
										('dieciseisavos', 'M80', 'seleccion-inglaterra', 'senegal', 'seleccion-inglaterra'),
										('dieciseisavos', 'M81', 'seleccion-turquia', 'seleccion-bosnia-herzegovina', 'seleccion-turquia'),
										('dieciseisavos', 'M82', 'seleccion-belgica', 'seleccion-republica-corea', 'seleccion-belgica'),
										('dieciseisavos', 'M83', 'seleccion-colombia', 'seleccion-croacia', 'seleccion-colombia'),
										('dieciseisavos', 'M84', 'seleccion-espanola', 'seleccion-austria', 'seleccion-espanola'),
										('dieciseisavos', 'M85', 'seleccion-suiza', 'seleccion-argelia', 'seleccion-suiza'),
										('dieciseisavos', 'M86', 'seleccion-argentina', 'seleccion-uruguay', 'seleccion-argentina'),
										('dieciseisavos', 'M87', 'seleccion-portugal', 'seleccion-ghana', 'seleccion-portugal'),
										('dieciseisavos', 'M88', 'seleccion-estados-unidos', 'seleccion-egipto', 'seleccion-estados-unidos');""")

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
		assert "<h2>Eliminatorias</h2>" in contenido
		assert '<div class="detalle-ronda">' in contenido
		assert '<h3>Aún no hay eliminatorias oficiales</h3>' not in contenido
		assert '<div class="bonus-eliminatorias">' not in contenido
		assert '<div class="bonus-card bonus-campeon">' not in contenido
		assert '<div class="bonus-card bonus-final">' not in contenido
		assert '<h3>Dieciseisavos</h3>' in contenido
		assert '<div class="detalle-eliminatoria-card acertada">' in contenido
		assert '<div class="detalle-eliminatoria-card pendiente">' in contenido
		assert '<div class="detalle-eliminatoria-card fallada">' not in contenido
		assert 'Clasificado para 16avos' in contenido
		assert '<h3>Octavos</h3>' not in contenido
		assert 'Clasificado para Octavos' not in contenido
		assert '<h3>Cuartos</h3>' not in contenido
		assert 'Clasificado para Cuartos' not in contenido
		assert '<h3>Semifinales</h3>' not in contenido
		assert 'Clasificado para Semifinales' not in contenido
		assert '<h3>Tercer puesto</h3>' not in contenido
		assert 'Clasificado para Tercer_Puesto' not in contenido
		assert '<h3>Final</h3>' not in contenido
		assert 'Clasificado para Final' not in contenido

def test_pagina_puntuacion_detalle_usuario_porra_cerrada_completada_un_partido_dos_rondas(cliente, conexion_usuario, porra_grupos, porra_mejores_terceros, partidos_bracket):

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

	conexion_usuario.c.execute("""INSERT INTO eliminatorias_real VALUES('dieciseisavos', 'M73', 'republica-checa', 'canada', 'republica-checa'),
										('dieciseisavos', 'M74', 'seleccion-alemania', 'seleccion-paraguay', 'seleccion-alemania'),
										('dieciseisavos', 'M75', 'seleccion-holanda', 'seleccion-marruecos', 'seleccion-holanda'),
										('dieciseisavos', 'M76', 'seleccion-brasil', 'seleccion-japon', 'seleccion-brasil'),
										('dieciseisavos', 'M77', 'seleccion-francia', 'seleccion-suecia', 'seleccion-francia'),
										('dieciseisavos', 'M78', 'seleccion-ecuador', 'seleccion-noruega', 'seleccion-noruega'),
										('dieciseisavos', 'M79', 'seleccion-mexico', 'seleccion-arabia-saudi', 'seleccion-mexico'),
										('dieciseisavos', 'M80', 'seleccion-inglaterra', 'senegal', 'seleccion-inglaterra'),
										('dieciseisavos', 'M81', 'seleccion-turquia', 'seleccion-bosnia-herzegovina', 'seleccion-turquia'),
										('dieciseisavos', 'M82', 'seleccion-belgica', 'seleccion-republica-corea', 'seleccion-belgica'),
										('dieciseisavos', 'M83', 'seleccion-colombia', 'seleccion-croacia', 'seleccion-colombia'),
										('dieciseisavos', 'M84', 'seleccion-espanola', 'seleccion-austria', 'seleccion-espanola'),
										('dieciseisavos', 'M85', 'seleccion-suiza', 'seleccion-argelia', 'seleccion-suiza'),
										('dieciseisavos', 'M86', 'seleccion-argentina', 'seleccion-uruguay', 'seleccion-argentina'),
										('dieciseisavos', 'M87', 'seleccion-portugal', 'seleccion-ghana', 'seleccion-portugal'),
										('dieciseisavos', 'M88', 'seleccion-estados-unidos', 'seleccion-egipto', 'seleccion-estados-unidos'),
										('octavos', 'M89', 'seleccion-alemania', 'seleccion-francia', 'seleccion-francia');""")

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
		assert "<h2>Eliminatorias</h2>" in contenido
		assert '<div class="detalle-ronda">' in contenido
		assert '<h3>Aún no hay eliminatorias oficiales</h3>' not in contenido
		assert '<div class="bonus-eliminatorias">' not in contenido
		assert '<div class="bonus-card bonus-campeon">' not in contenido
		assert '<div class="bonus-card bonus-final">' not in contenido
		assert '<h3>Dieciseisavos</h3>' in contenido
		assert '<div class="detalle-eliminatoria-card acertada">' in contenido
		assert '<div class="detalle-eliminatoria-card pendiente">' in contenido
		assert '<div class="detalle-eliminatoria-card fallada">' in contenido
		assert 'Clasificado para 16avos' in contenido
		assert '<h3>Octavos</h3>' in contenido
		assert 'Clasificado para Octavos' in contenido
		assert '<h3>Cuartos</h3>' not in contenido
		assert 'Clasificado para Cuartos' not in contenido
		assert '<h3>Semifinales</h3>' not in contenido
		assert 'Clasificado para Semifinales' not in contenido
		assert '<h3>Tercer puesto</h3>' not in contenido
		assert 'Clasificado para Tercer_Puesto' not in contenido
		assert '<h3>Final</h3>' not in contenido
		assert 'Clasificado para Final' not in contenido

def test_pagina_puntuacion_detalle_usuario_porra_cerrada_completada_dos_rondas(cliente, conexion_usuario, porra_grupos, porra_mejores_terceros, partidos_bracket):

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

	conexion_usuario.c.execute("""INSERT INTO eliminatorias_real VALUES('dieciseisavos', 'M73', 'republica-checa', 'canada', 'republica-checa'),
										('dieciseisavos', 'M74', 'seleccion-alemania', 'seleccion-paraguay', 'seleccion-alemania'),
										('dieciseisavos', 'M75', 'seleccion-holanda', 'seleccion-marruecos', 'seleccion-holanda'),
										('dieciseisavos', 'M76', 'seleccion-brasil', 'seleccion-japon', 'seleccion-brasil'),
										('dieciseisavos', 'M77', 'seleccion-francia', 'seleccion-suecia', 'seleccion-francia'),
										('dieciseisavos', 'M78', 'seleccion-ecuador', 'seleccion-noruega', 'seleccion-noruega'),
										('dieciseisavos', 'M79', 'seleccion-mexico', 'seleccion-arabia-saudi', 'seleccion-mexico'),
										('dieciseisavos', 'M80', 'seleccion-inglaterra', 'senegal', 'seleccion-inglaterra'),
										('dieciseisavos', 'M81', 'seleccion-turquia', 'seleccion-bosnia-herzegovina', 'seleccion-turquia'),
										('dieciseisavos', 'M82', 'seleccion-belgica', 'seleccion-republica-corea', 'seleccion-belgica'),
										('dieciseisavos', 'M83', 'seleccion-colombia', 'seleccion-croacia', 'seleccion-colombia'),
										('dieciseisavos', 'M84', 'seleccion-espanola', 'seleccion-austria', 'seleccion-espanola'),
										('dieciseisavos', 'M85', 'seleccion-suiza', 'seleccion-argelia', 'seleccion-suiza'),
										('dieciseisavos', 'M86', 'seleccion-argentina', 'seleccion-uruguay', 'seleccion-argentina'),
										('dieciseisavos', 'M87', 'seleccion-portugal', 'seleccion-ghana', 'seleccion-portugal'),
										('dieciseisavos', 'M88', 'seleccion-estados-unidos', 'seleccion-egipto', 'seleccion-estados-unidos'),
										('octavos', 'M89', 'seleccion-alemania', 'seleccion-francia', 'seleccion-francia'),
										('octavos', 'M90', 'republica-checa', 'seleccion-holanda', 'seleccion-holanda'),
										('octavos', 'M91', 'seleccion-brasil', 'seleccion-noruega', 'seleccion-brasil'),
										('octavos', 'M92', 'seleccion-mexico', 'seleccion-inglaterra', 'seleccion-inglaterra'),
										('octavos', 'M93', 'seleccion-colombia', 'seleccion-espanola', 'seleccion-espanola'),
										('octavos', 'M94', 'seleccion-turquia', 'seleccion-belgica', 'seleccion-belgica'),
										('octavos', 'M95', 'seleccion-argentina', 'seleccion-estados-unidos', 'seleccion-argentina'),
										('octavos', 'M96', 'seleccion-suiza', 'seleccion-portugal', 'seleccion-portugal');""")

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
		assert "<h2>Eliminatorias</h2>" in contenido
		assert '<div class="detalle-ronda">' in contenido
		assert '<h3>Aún no hay eliminatorias oficiales</h3>' not in contenido
		assert '<div class="bonus-eliminatorias">' not in contenido
		assert '<div class="bonus-card bonus-campeon">' not in contenido
		assert '<div class="bonus-card bonus-final">' not in contenido
		assert '<h3>Dieciseisavos</h3>' in contenido
		assert '<div class="detalle-eliminatoria-card acertada">' in contenido
		assert '<div class="detalle-eliminatoria-card pendiente">' in contenido
		assert '<div class="detalle-eliminatoria-card fallada">' in contenido
		assert 'Clasificado para 16avos' in contenido
		assert '<h3>Octavos</h3>' in contenido
		assert 'Clasificado para Octavos' in contenido
		assert '<h3>Cuartos</h3>' not in contenido
		assert 'Clasificado para Cuartos' not in contenido
		assert '<h3>Semifinales</h3>' not in contenido
		assert 'Clasificado para Semifinales' not in contenido
		assert '<h3>Tercer puesto</h3>' not in contenido
		assert 'Clasificado para Tercer_Puesto' not in contenido
		assert '<h3>Final</h3>' not in contenido
		assert 'Clasificado para Final' not in contenido

def test_pagina_puntuacion_detalle_usuario_porra_cerrada_completada_tercer_puesto(cliente, conexion_usuario, porra_grupos, porra_mejores_terceros, partidos_bracket):

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

	conexion_usuario.c.execute("""INSERT INTO eliminatorias_real VALUES('dieciseisavos', 'M73', 'republica-checa', 'canada', 'republica-checa'),
										('dieciseisavos', 'M74', 'seleccion-alemania', 'seleccion-paraguay', 'seleccion-alemania'),
										('dieciseisavos', 'M75', 'seleccion-holanda', 'seleccion-marruecos', 'seleccion-holanda'),
										('dieciseisavos', 'M76', 'seleccion-brasil', 'seleccion-japon', 'seleccion-brasil'),
										('dieciseisavos', 'M77', 'seleccion-francia', 'seleccion-suecia', 'seleccion-francia'),
										('dieciseisavos', 'M78', 'seleccion-ecuador', 'seleccion-noruega', 'seleccion-noruega'),
										('dieciseisavos', 'M79', 'seleccion-mexico', 'seleccion-arabia-saudi', 'seleccion-mexico'),
										('dieciseisavos', 'M80', 'seleccion-inglaterra', 'senegal', 'seleccion-inglaterra'),
										('dieciseisavos', 'M81', 'seleccion-turquia', 'seleccion-bosnia-herzegovina', 'seleccion-turquia'),
										('dieciseisavos', 'M82', 'seleccion-belgica', 'seleccion-republica-corea', 'seleccion-belgica'),
										('dieciseisavos', 'M83', 'seleccion-colombia', 'seleccion-croacia', 'seleccion-colombia'),
										('dieciseisavos', 'M84', 'seleccion-espanola', 'seleccion-austria', 'seleccion-espanola'),
										('dieciseisavos', 'M85', 'seleccion-suiza', 'seleccion-argelia', 'seleccion-suiza'),
										('dieciseisavos', 'M86', 'seleccion-argentina', 'seleccion-uruguay', 'seleccion-argentina'),
										('dieciseisavos', 'M87', 'seleccion-portugal', 'seleccion-ghana', 'seleccion-portugal'),
										('dieciseisavos', 'M88', 'seleccion-estados-unidos', 'seleccion-egipto', 'seleccion-estados-unidos'),
										('octavos', 'M89', 'seleccion-alemania', 'seleccion-francia', 'seleccion-francia'),
										('octavos', 'M90', 'republica-checa', 'seleccion-holanda', 'seleccion-holanda'),
										('octavos', 'M91', 'seleccion-brasil', 'seleccion-noruega', 'seleccion-brasil'),
										('octavos', 'M92', 'seleccion-mexico', 'seleccion-inglaterra', 'seleccion-inglaterra'),
										('octavos', 'M93', 'seleccion-colombia', 'seleccion-espanola', 'seleccion-espanola'),
										('octavos', 'M94', 'seleccion-turquia', 'seleccion-belgica', 'seleccion-belgica'),
										('octavos', 'M95', 'seleccion-argentina', 'seleccion-estados-unidos', 'seleccion-argentina'),
										('octavos', 'M96', 'seleccion-suiza', 'seleccion-portugal', 'seleccion-portugal'),
										('cuartos', 'M97', 'seleccion-francia', 'seleccion-holanda', 'seleccion-francia'),
										('cuartos', 'M98', 'seleccion-espanola', 'seleccion-belgica', 'seleccion-espanola'),
										('cuartos', 'M99', 'seleccion-inglaterra', 'seleccion-brasil', 'seleccion-brasil'),
										('cuartos', 'M100', 'seleccion-portugal', 'seleccion-argentina', 'seleccion-argentina'),
										('semifinales', 'M101', 'seleccion-francia', 'seleccion-espanola', 'seleccion-espanola'),
										('semifinales', 'M102', 'seleccion-brasil', 'seleccion-argentina', 'seleccion-argentina'),
										('tercer_puesto', 'M103', 'seleccion-francia', 'seleccion-brasil', 'seleccion-francia');""")

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
		assert "<h2>Eliminatorias</h2>" in contenido
		assert '<div class="detalle-ronda">' in contenido
		assert '<h3>Aún no hay eliminatorias oficiales</h3>' not in contenido
		assert '<div class="bonus-eliminatorias">' not in contenido
		assert '<div class="bonus-card bonus-campeon">' not in contenido
		assert '<div class="bonus-card bonus-final">' not in contenido
		assert '<h3>Dieciseisavos</h3>' in contenido
		assert '<div class="detalle-eliminatoria-card acertada">' in contenido
		assert '<div class="detalle-eliminatoria-card pendiente">' in contenido
		assert '<div class="detalle-eliminatoria-card fallada">' in contenido
		assert 'Clasificado para 16avos' in contenido
		assert '<h3>Octavos</h3>' in contenido
		assert 'Clasificado para Octavos' in contenido
		assert '<h3>Cuartos</h3>' in contenido
		assert 'Clasificado para Cuartos' in contenido
		assert '<h3>Semifinales</h3>' in contenido
		assert 'Clasificado para Semifinales' in contenido
		assert '<h3>Tercer puesto</h3>' in contenido
		assert 'Clasificado para Tercer_Puesto' in contenido
		assert '<h3>Final</h3>' not in contenido
		assert 'Clasificado para Final' not in contenido

def test_pagina_puntuacion_detalle_usuario_porra_cerrada_completada_final_sin_campeon_sin_final_exacta(cliente, conexion_usuario, porra_grupos, porra_mejores_terceros, partidos_bracket):

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

	conexion_usuario.c.execute("""INSERT INTO eliminatorias_real VALUES('dieciseisavos', 'M73', 'republica-checa', 'canada', 'republica-checa'),
										('dieciseisavos', 'M74', 'seleccion-alemania', 'seleccion-paraguay', 'seleccion-alemania'),
										('dieciseisavos', 'M75', 'seleccion-holanda', 'seleccion-marruecos', 'seleccion-holanda'),
										('dieciseisavos', 'M76', 'seleccion-brasil', 'seleccion-japon', 'seleccion-brasil'),
										('dieciseisavos', 'M77', 'seleccion-francia', 'seleccion-suecia', 'seleccion-francia'),
										('dieciseisavos', 'M78', 'seleccion-ecuador', 'seleccion-noruega', 'seleccion-noruega'),
										('dieciseisavos', 'M79', 'seleccion-mexico', 'seleccion-arabia-saudi', 'seleccion-mexico'),
										('dieciseisavos', 'M80', 'seleccion-inglaterra', 'senegal', 'seleccion-inglaterra'),
										('dieciseisavos', 'M81', 'seleccion-turquia', 'seleccion-bosnia-herzegovina', 'seleccion-turquia'),
										('dieciseisavos', 'M82', 'seleccion-belgica', 'seleccion-republica-corea', 'seleccion-belgica'),
										('dieciseisavos', 'M83', 'seleccion-colombia', 'seleccion-croacia', 'seleccion-colombia'),
										('dieciseisavos', 'M84', 'seleccion-espanola', 'seleccion-austria', 'seleccion-espanola'),
										('dieciseisavos', 'M85', 'seleccion-suiza', 'seleccion-argelia', 'seleccion-suiza'),
										('dieciseisavos', 'M86', 'seleccion-argentina', 'seleccion-uruguay', 'seleccion-argentina'),
										('dieciseisavos', 'M87', 'seleccion-portugal', 'seleccion-ghana', 'seleccion-portugal'),
										('dieciseisavos', 'M88', 'seleccion-estados-unidos', 'seleccion-egipto', 'seleccion-estados-unidos'),
										('octavos', 'M89', 'seleccion-alemania', 'seleccion-francia', 'seleccion-francia'),
										('octavos', 'M90', 'republica-checa', 'seleccion-holanda', 'seleccion-holanda'),
										('octavos', 'M91', 'seleccion-brasil', 'seleccion-noruega', 'seleccion-brasil'),
										('octavos', 'M92', 'seleccion-mexico', 'seleccion-inglaterra', 'seleccion-inglaterra'),
										('octavos', 'M93', 'seleccion-colombia', 'seleccion-espanola', 'seleccion-espanola'),
										('octavos', 'M94', 'seleccion-turquia', 'seleccion-belgica', 'seleccion-belgica'),
										('octavos', 'M95', 'seleccion-argentina', 'seleccion-estados-unidos', 'seleccion-argentina'),
										('octavos', 'M96', 'seleccion-suiza', 'seleccion-portugal', 'seleccion-portugal'),
										('cuartos', 'M97', 'seleccion-francia', 'seleccion-holanda', 'seleccion-francia'),
										('cuartos', 'M98', 'seleccion-espanola', 'seleccion-belgica', 'seleccion-espanola'),
										('cuartos', 'M99', 'seleccion-inglaterra', 'seleccion-brasil', 'seleccion-brasil'),
										('cuartos', 'M100', 'seleccion-portugal', 'seleccion-argentina', 'seleccion-argentina'),
										('semifinales', 'M101', 'seleccion-francia', 'seleccion-espanola', 'seleccion-espanola'),
										('semifinales', 'M102', 'seleccion-brasil', 'seleccion-argentina', 'seleccion-argentina'),
										('tercer_puesto', 'M103', 'seleccion-francia', 'seleccion-brasil', 'seleccion-francia'),
										('final', 'M104', 'seleccion-belgica', 'seleccion-argentina', 'seleccion-belgica');""")

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
		assert "<h2>Eliminatorias</h2>" in contenido
		assert '<div class="detalle-ronda">' in contenido
		assert '<h3>Aún no hay eliminatorias oficiales</h3>' not in contenido
		assert '<div class="bonus-eliminatorias">' not in contenido
		assert '<div class="bonus-card bonus-campeon">' not in contenido
		assert '<div class="bonus-card bonus-final">' not in contenido
		assert '<h3>Dieciseisavos</h3>' in contenido
		assert '<div class="detalle-eliminatoria-card acertada">' in contenido
		assert '<div class="detalle-eliminatoria-card pendiente">' not in contenido
		assert '<div class="detalle-eliminatoria-card fallada">' in contenido
		assert 'Clasificado para 16avos' in contenido
		assert '<h3>Octavos</h3>' in contenido
		assert 'Clasificado para Octavos' in contenido
		assert '<h3>Cuartos</h3>' in contenido
		assert 'Clasificado para Cuartos' in contenido
		assert '<h3>Semifinales</h3>' in contenido
		assert 'Clasificado para Semifinales' in contenido
		assert '<h3>Tercer puesto</h3>' in contenido
		assert 'Clasificado para Tercer_Puesto' in contenido
		assert '<h3>Final</h3>' in contenido
		assert 'Clasificado para Final' in contenido

def test_pagina_puntuacion_detalle_usuario_porra_cerrada_completada_final_sin_campeon_con_final_exacta(cliente, conexion_usuario, porra_grupos, porra_mejores_terceros, partidos_bracket):

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

	conexion_usuario.c.execute("""INSERT INTO eliminatorias_real VALUES('dieciseisavos', 'M73', 'republica-checa', 'canada', 'republica-checa'),
										('dieciseisavos', 'M74', 'seleccion-alemania', 'seleccion-paraguay', 'seleccion-alemania'),
										('dieciseisavos', 'M75', 'seleccion-holanda', 'seleccion-marruecos', 'seleccion-holanda'),
										('dieciseisavos', 'M76', 'seleccion-brasil', 'seleccion-japon', 'seleccion-brasil'),
										('dieciseisavos', 'M77', 'seleccion-francia', 'seleccion-suecia', 'seleccion-francia'),
										('dieciseisavos', 'M78', 'seleccion-ecuador', 'seleccion-noruega', 'seleccion-noruega'),
										('dieciseisavos', 'M79', 'seleccion-mexico', 'seleccion-arabia-saudi', 'seleccion-mexico'),
										('dieciseisavos', 'M80', 'seleccion-inglaterra', 'senegal', 'seleccion-inglaterra'),
										('dieciseisavos', 'M81', 'seleccion-turquia', 'seleccion-bosnia-herzegovina', 'seleccion-turquia'),
										('dieciseisavos', 'M82', 'seleccion-belgica', 'seleccion-republica-corea', 'seleccion-belgica'),
										('dieciseisavos', 'M83', 'seleccion-colombia', 'seleccion-croacia', 'seleccion-colombia'),
										('dieciseisavos', 'M84', 'seleccion-espanola', 'seleccion-austria', 'seleccion-espanola'),
										('dieciseisavos', 'M85', 'seleccion-suiza', 'seleccion-argelia', 'seleccion-suiza'),
										('dieciseisavos', 'M86', 'seleccion-argentina', 'seleccion-uruguay', 'seleccion-argentina'),
										('dieciseisavos', 'M87', 'seleccion-portugal', 'seleccion-ghana', 'seleccion-portugal'),
										('dieciseisavos', 'M88', 'seleccion-estados-unidos', 'seleccion-egipto', 'seleccion-estados-unidos'),
										('octavos', 'M89', 'seleccion-alemania', 'seleccion-francia', 'seleccion-francia'),
										('octavos', 'M90', 'republica-checa', 'seleccion-holanda', 'seleccion-holanda'),
										('octavos', 'M91', 'seleccion-brasil', 'seleccion-noruega', 'seleccion-brasil'),
										('octavos', 'M92', 'seleccion-mexico', 'seleccion-inglaterra', 'seleccion-inglaterra'),
										('octavos', 'M93', 'seleccion-colombia', 'seleccion-espanola', 'seleccion-espanola'),
										('octavos', 'M94', 'seleccion-turquia', 'seleccion-belgica', 'seleccion-belgica'),
										('octavos', 'M95', 'seleccion-argentina', 'seleccion-estados-unidos', 'seleccion-argentina'),
										('octavos', 'M96', 'seleccion-suiza', 'seleccion-portugal', 'seleccion-portugal'),
										('cuartos', 'M97', 'seleccion-francia', 'seleccion-holanda', 'seleccion-francia'),
										('cuartos', 'M98', 'seleccion-espanola', 'seleccion-belgica', 'seleccion-espanola'),
										('cuartos', 'M99', 'seleccion-inglaterra', 'seleccion-brasil', 'seleccion-brasil'),
										('cuartos', 'M100', 'seleccion-portugal', 'seleccion-argentina', 'seleccion-argentina'),
										('semifinales', 'M101', 'seleccion-francia', 'seleccion-espanola', 'seleccion-espanola'),
										('semifinales', 'M102', 'seleccion-brasil', 'seleccion-argentina', 'seleccion-argentina'),
										('tercer_puesto', 'M103', 'seleccion-francia', 'seleccion-brasil', 'seleccion-francia'),
										('final', 'M104', 'seleccion-espanola', 'seleccion-argentina', 'seleccion-argentina');""")

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
		assert "<h2>Eliminatorias</h2>" in contenido
		assert '<div class="detalle-ronda">' in contenido
		assert '<h3>Aún no hay eliminatorias oficiales</h3>' not in contenido
		assert '<div class="bonus-eliminatorias">' in contenido
		assert '<div class="bonus-card bonus-campeon">' not in contenido
		assert '<div class="bonus-card bonus-final">' in contenido
		assert '<h3>Dieciseisavos</h3>' in contenido
		assert '<div class="detalle-eliminatoria-card acertada">' in contenido
		assert '<div class="detalle-eliminatoria-card pendiente">' not in contenido
		assert '<div class="detalle-eliminatoria-card fallada">' in contenido
		assert 'Clasificado para 16avos' in contenido
		assert '<h3>Octavos</h3>' in contenido
		assert 'Clasificado para Octavos' in contenido
		assert '<h3>Cuartos</h3>' in contenido
		assert 'Clasificado para Cuartos' in contenido
		assert '<h3>Semifinales</h3>' in contenido
		assert 'Clasificado para Semifinales' in contenido
		assert '<h3>Tercer puesto</h3>' in contenido
		assert 'Clasificado para Tercer_Puesto' in contenido
		assert '<h3>Final</h3>' in contenido
		assert 'Clasificado para Final' in contenido

def test_pagina_puntuacion_detalle_usuario_porra_cerrada_completada_final_sin_campeon_con_final_exacta(cliente, conexion_usuario, porra_grupos, porra_mejores_terceros, partidos_bracket):

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

	conexion_usuario.c.execute("""INSERT INTO eliminatorias_real VALUES('dieciseisavos', 'M73', 'republica-checa', 'canada', 'republica-checa'),
										('dieciseisavos', 'M74', 'seleccion-alemania', 'seleccion-paraguay', 'seleccion-alemania'),
										('dieciseisavos', 'M75', 'seleccion-holanda', 'seleccion-marruecos', 'seleccion-holanda'),
										('dieciseisavos', 'M76', 'seleccion-brasil', 'seleccion-japon', 'seleccion-brasil'),
										('dieciseisavos', 'M77', 'seleccion-francia', 'seleccion-suecia', 'seleccion-francia'),
										('dieciseisavos', 'M78', 'seleccion-ecuador', 'seleccion-noruega', 'seleccion-noruega'),
										('dieciseisavos', 'M79', 'seleccion-mexico', 'seleccion-arabia-saudi', 'seleccion-mexico'),
										('dieciseisavos', 'M80', 'seleccion-inglaterra', 'senegal', 'seleccion-inglaterra'),
										('dieciseisavos', 'M81', 'seleccion-turquia', 'seleccion-bosnia-herzegovina', 'seleccion-turquia'),
										('dieciseisavos', 'M82', 'seleccion-belgica', 'seleccion-republica-corea', 'seleccion-belgica'),
										('dieciseisavos', 'M83', 'seleccion-colombia', 'seleccion-croacia', 'seleccion-colombia'),
										('dieciseisavos', 'M84', 'seleccion-espanola', 'seleccion-austria', 'seleccion-espanola'),
										('dieciseisavos', 'M85', 'seleccion-suiza', 'seleccion-argelia', 'seleccion-suiza'),
										('dieciseisavos', 'M86', 'seleccion-argentina', 'seleccion-uruguay', 'seleccion-argentina'),
										('dieciseisavos', 'M87', 'seleccion-portugal', 'seleccion-ghana', 'seleccion-portugal'),
										('dieciseisavos', 'M88', 'seleccion-estados-unidos', 'seleccion-egipto', 'seleccion-estados-unidos'),
										('octavos', 'M89', 'seleccion-alemania', 'seleccion-francia', 'seleccion-francia'),
										('octavos', 'M90', 'republica-checa', 'seleccion-holanda', 'seleccion-holanda'),
										('octavos', 'M91', 'seleccion-brasil', 'seleccion-noruega', 'seleccion-brasil'),
										('octavos', 'M92', 'seleccion-mexico', 'seleccion-inglaterra', 'seleccion-inglaterra'),
										('octavos', 'M93', 'seleccion-colombia', 'seleccion-espanola', 'seleccion-espanola'),
										('octavos', 'M94', 'seleccion-turquia', 'seleccion-belgica', 'seleccion-belgica'),
										('octavos', 'M95', 'seleccion-argentina', 'seleccion-estados-unidos', 'seleccion-argentina'),
										('octavos', 'M96', 'seleccion-suiza', 'seleccion-portugal', 'seleccion-portugal'),
										('cuartos', 'M97', 'seleccion-francia', 'seleccion-holanda', 'seleccion-francia'),
										('cuartos', 'M98', 'seleccion-espanola', 'seleccion-belgica', 'seleccion-espanola'),
										('cuartos', 'M99', 'seleccion-inglaterra', 'seleccion-brasil', 'seleccion-brasil'),
										('cuartos', 'M100', 'seleccion-portugal', 'seleccion-argentina', 'seleccion-argentina'),
										('semifinales', 'M101', 'seleccion-francia', 'seleccion-espanola', 'seleccion-espanola'),
										('semifinales', 'M102', 'seleccion-brasil', 'seleccion-argentina', 'seleccion-argentina'),
										('tercer_puesto', 'M103', 'seleccion-francia', 'seleccion-brasil', 'seleccion-francia'),
										('final', 'M104', 'seleccion-espanola', 'seleccion-argentina', 'seleccion-espanola');""")

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
		assert "<h2>Eliminatorias</h2>" in contenido
		assert '<div class="detalle-ronda">' in contenido
		assert '<h3>Aún no hay eliminatorias oficiales</h3>' not in contenido
		assert '<div class="bonus-eliminatorias">' in contenido
		assert '<div class="bonus-card bonus-campeon">' in contenido
		assert '<div class="bonus-card bonus-final">' in contenido
		assert '<h3>Dieciseisavos</h3>' in contenido
		assert '<div class="detalle-eliminatoria-card acertada">' in contenido
		assert '<div class="detalle-eliminatoria-card pendiente">' not in contenido
		assert '<div class="detalle-eliminatoria-card fallada">' in contenido
		assert 'Clasificado para 16avos' in contenido
		assert '<h3>Octavos</h3>' in contenido
		assert 'Clasificado para Octavos' in contenido
		assert '<h3>Cuartos</h3>' in contenido
		assert 'Clasificado para Cuartos' in contenido
		assert '<h3>Semifinales</h3>' in contenido
		assert 'Clasificado para Semifinales' in contenido
		assert '<h3>Tercer puesto</h3>' in contenido
		assert 'Clasificado para Tercer_Puesto' in contenido
		assert '<h3>Final</h3>' in contenido
		assert 'Clasificado para Final' in contenido