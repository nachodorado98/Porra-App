import pytest
import json
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

def test_pagina_calcular_puntuaciones_sin_login(cliente, conexion):

	respuesta=cliente.put("/puntuacion/calcular_puntuacion", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

def test_pagina_calcular_puntuaciones_no_admin(cliente, conexion_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.put("/puntuacion/calcular_puntuacion")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/porra"
		assert "<h1>Redirecting...</h1>" in contenido

def test_pagina_calcular_puntuaciones_sin_porra_completada(cliente, conexion_usuario):

	conexion_usuario.c.execute("UPDATE usuarios SET Admin=True")

	conexion_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.put("/puntuacion/calcular_puntuacion")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/settings"
		assert "<h1>Redirecting...</h1>" in contenido

		conexion_usuario.c.execute("SELECT Puntos_Grupos, Puntos_Mejores_Terceros, Puntos_Eliminatorias, Puntos_Total FROM puntuaciones")

		puntuacion=conexion_usuario.c.fetchone()

		assert puntuacion["puntos_grupos"]==0
		assert puntuacion["puntos_mejores_terceros"]==0
		assert puntuacion["puntos_eliminatorias"]==0
		assert puntuacion["puntos_total"]==0

def test_pagina_calcular_puntuaciones_sin_grupo_real_un_grupo_porra(cliente, conexion_usuario):

	conexion_usuario.actualizarEstadoPorraUsuario("nacho98")

	conexion_usuario.c.execute("UPDATE usuarios SET Admin=True")

	conexion_usuario.confirmar()

	conexion_usuario.insertarEquipoGruposPorraUsuario("nacho98", "A", ['seleccion-mexico', 'republica-checa', 'seleccion-republica-corea', 'seleccion-sudafrica'])

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.put("/puntuacion/calcular_puntuacion")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/settings"
		assert "<h1>Redirecting...</h1>" in contenido

		conexion_usuario.c.execute("SELECT Puntos_Grupos, Puntos_Mejores_Terceros, Puntos_Eliminatorias, Puntos_Total FROM puntuaciones")

		puntuacion=conexion_usuario.c.fetchone()

		assert puntuacion["puntos_grupos"]==0
		assert puntuacion["puntos_mejores_terceros"]==0
		assert puntuacion["puntos_eliminatorias"]==0
		assert puntuacion["puntos_total"]==0

def test_pagina_calcular_puntuaciones_un_grupo_real_un_grupo_porra(cliente, conexion_usuario):

	conexion_usuario.actualizarEstadoPorraUsuario("nacho98")

	conexion_usuario.c.execute("UPDATE usuarios SET Admin=True")

	conexion_usuario.c.execute("""INSERT INTO grupo_equipos_real
									VALUES ('A', 'seleccion-republica-corea', 1), ('A', 'seleccion-mexico', 2), ('A', 'republica-checa', 3), ('A', 'seleccion-sudafrica', 4)""")

	conexion_usuario.confirmar()

	conexion_usuario.insertarEquipoGruposPorraUsuario("nacho98", "A", ['seleccion-mexico', 'republica-checa', 'seleccion-republica-corea', 'seleccion-sudafrica'])

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.put("/puntuacion/calcular_puntuacion")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/settings"
		assert "<h1>Redirecting...</h1>" in contenido

		conexion_usuario.c.execute("SELECT Puntos_Grupos, Puntos_Mejores_Terceros, Puntos_Eliminatorias, Puntos_Total FROM puntuaciones")

		puntuacion=conexion_usuario.c.fetchone()

		assert puntuacion["puntos_grupos"]==8
		assert puntuacion["puntos_mejores_terceros"]==0
		assert puntuacion["puntos_eliminatorias"]==0
		assert puntuacion["puntos_total"]==8

def test_pagina_calcular_puntuaciones_un_grupo_real_dos_grupos_porra(cliente, conexion_usuario):

	conexion_usuario.actualizarEstadoPorraUsuario("nacho98")

	conexion_usuario.c.execute("UPDATE usuarios SET Admin=True")

	conexion_usuario.c.execute("""INSERT INTO grupo_equipos_real
									VALUES ('A', 'seleccion-republica-corea', 1), ('A', 'seleccion-mexico', 2), ('A', 'republica-checa', 3), ('A', 'seleccion-sudafrica', 4)""")

	conexion_usuario.confirmar()

	conexion_usuario.insertarEquipoGruposPorraUsuario("nacho98", "A", ['seleccion-mexico', 'republica-checa', 'seleccion-republica-corea', 'seleccion-sudafrica'])

	conexion_usuario.insertarEquipoGruposPorraUsuario("nacho98", "B", ['seleccion-suiza', 'canada', 'seleccion-bosnia-herzegovina', 'seleccion-qatar'])

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.put("/puntuacion/calcular_puntuacion")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/settings"
		assert "<h1>Redirecting...</h1>" in contenido

		conexion_usuario.c.execute("SELECT Puntos_Grupos, Puntos_Mejores_Terceros, Puntos_Eliminatorias, Puntos_Total FROM puntuaciones")

		puntuacion=conexion_usuario.c.fetchone()

		assert puntuacion["puntos_grupos"]==8
		assert puntuacion["puntos_mejores_terceros"]==0
		assert puntuacion["puntos_eliminatorias"]==0
		assert puntuacion["puntos_total"]==8

def test_pagina_calcular_puntuaciones_dos_grupos_real_dos_grupos_porra(cliente, conexion_usuario):

	conexion_usuario.actualizarEstadoPorraUsuario("nacho98")

	conexion_usuario.c.execute("UPDATE usuarios SET Admin=True")

	conexion_usuario.c.execute("""INSERT INTO grupo_equipos_real
									VALUES ('A', 'seleccion-republica-corea', 1), ('A', 'seleccion-mexico', 2), ('A', 'republica-checa', 3), ('A', 'seleccion-sudafrica', 4),
											('B', 'seleccion-bosnia-herzegovina', 1), ('B', 'canada', 2), ('B', 'seleccion-qatar', 3), ('B', 'seleccion-suiza', 4)""")

	conexion_usuario.confirmar()

	conexion_usuario.insertarEquipoGruposPorraUsuario("nacho98", "A", ['seleccion-mexico', 'republica-checa', 'seleccion-republica-corea', 'seleccion-sudafrica'])

	conexion_usuario.insertarEquipoGruposPorraUsuario("nacho98", "B", ['seleccion-suiza', 'canada', 'seleccion-bosnia-herzegovina', 'seleccion-qatar'])

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.put("/puntuacion/calcular_puntuacion")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/settings"
		assert "<h1>Redirecting...</h1>" in contenido

		conexion_usuario.c.execute("SELECT Puntos_Grupos, Puntos_Mejores_Terceros, Puntos_Eliminatorias, Puntos_Total FROM puntuaciones")

		puntuacion=conexion_usuario.c.fetchone()

		assert puntuacion["puntos_grupos"]==14
		assert puntuacion["puntos_mejores_terceros"]==0
		assert puntuacion["puntos_eliminatorias"]==0
		assert puntuacion["puntos_total"]==14

def test_pagina_calcular_puntuaciones_grupos_todos_real_dos_grupos_porra(cliente, conexion_usuario):

	conexion_usuario.actualizarEstadoPorraUsuario("nacho98")

	conexion_usuario.c.execute("UPDATE usuarios SET Admin=True")

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

	conexion_usuario.insertarEquipoGruposPorraUsuario("nacho98", "A", ['seleccion-mexico', 'republica-checa', 'seleccion-republica-corea', 'seleccion-sudafrica'])

	conexion_usuario.insertarEquipoGruposPorraUsuario("nacho98", "B", ['seleccion-suiza', 'canada', 'seleccion-bosnia-herzegovina', 'seleccion-qatar'])

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.put("/puntuacion/calcular_puntuacion")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/settings"
		assert "<h1>Redirecting...</h1>" in contenido

		conexion_usuario.c.execute("SELECT Puntos_Grupos, Puntos_Mejores_Terceros, Puntos_Eliminatorias, Puntos_Total FROM puntuaciones")

		puntuacion=conexion_usuario.c.fetchone()

		assert puntuacion["puntos_grupos"]==14
		assert puntuacion["puntos_mejores_terceros"]==0
		assert puntuacion["puntos_eliminatorias"]==0
		assert puntuacion["puntos_total"]==14

def test_pagina_calcular_puntuaciones_grupos_todos(cliente, conexion_usuario, porra_grupos):

	conexion_usuario.actualizarEstadoPorraUsuario("nacho98")

	conexion_usuario.c.execute("UPDATE usuarios SET Admin=True")

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

		respuesta=cliente_abierto.put("/puntuacion/calcular_puntuacion")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/settings"
		assert "<h1>Redirecting...</h1>" in contenido

		conexion_usuario.c.execute("SELECT Puntos_Grupos, Puntos_Mejores_Terceros, Puntos_Eliminatorias, Puntos_Total FROM puntuaciones")

		puntuacion=conexion_usuario.c.fetchone()

		assert puntuacion["puntos_grupos"]==92
		assert puntuacion["puntos_mejores_terceros"]==0
		assert puntuacion["puntos_eliminatorias"]==0
		assert puntuacion["puntos_total"]==92

def test_pagina_calcular_puntuaciones_sin_mejores_terceros_real(cliente, conexion_usuario, porra_grupos, porra_mejores_terceros):

	conexion_usuario.actualizarEstadoPorraUsuario("nacho98")

	conexion_usuario.c.execute("UPDATE usuarios SET Admin=True")

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

		respuesta=cliente_abierto.put("/puntuacion/calcular_puntuacion")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/settings"
		assert "<h1>Redirecting...</h1>" in contenido

		conexion_usuario.c.execute("SELECT Puntos_Grupos, Puntos_Mejores_Terceros, Puntos_Eliminatorias, Puntos_Total FROM puntuaciones")

		puntuacion=conexion_usuario.c.fetchone()

		assert puntuacion["puntos_grupos"]==92
		assert puntuacion["puntos_mejores_terceros"]==0
		assert puntuacion["puntos_eliminatorias"]==0
		assert puntuacion["puntos_total"]==92

def test_pagina_calcular_puntuaciones_con_mejores_terceros(cliente, conexion_usuario, porra_grupos, porra_mejores_terceros):

	conexion_usuario.actualizarEstadoPorraUsuario("nacho98")

	conexion_usuario.c.execute("UPDATE usuarios SET Admin=True")

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

		respuesta=cliente_abierto.put("/puntuacion/calcular_puntuacion")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/settings"
		assert "<h1>Redirecting...</h1>" in contenido

		conexion_usuario.c.execute("SELECT Puntos_Grupos, Puntos_Mejores_Terceros, Puntos_Eliminatorias, Puntos_Total FROM puntuaciones")

		puntuacion=conexion_usuario.c.fetchone()

		assert puntuacion["puntos_grupos"]==92
		assert puntuacion["puntos_mejores_terceros"]==12
		assert puntuacion["puntos_eliminatorias"]==0
		assert puntuacion["puntos_total"]==104

def test_pagina_calcular_puntuaciones_sin_eliminatorias_real(cliente, conexion_usuario, porra_grupos, porra_mejores_terceros, partidos_bracket):

	conexion_usuario.actualizarEstadoPorraUsuario("nacho98")

	conexion_usuario.c.execute("UPDATE usuarios SET Admin=True")

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

		respuesta=cliente_abierto.put("/puntuacion/calcular_puntuacion")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/settings"
		assert "<h1>Redirecting...</h1>" in contenido

		conexion_usuario.c.execute("SELECT Puntos_Grupos, Puntos_Mejores_Terceros, Puntos_Eliminatorias, Puntos_Total FROM puntuaciones")

		puntuacion=conexion_usuario.c.fetchone()

		assert puntuacion["puntos_grupos"]==92
		assert puntuacion["puntos_mejores_terceros"]==12
		assert puntuacion["puntos_eliminatorias"]==0
		assert puntuacion["puntos_total"]==104

def test_pagina_calcular_puntuaciones_un_partido_ronda_real(cliente, conexion_usuario, porra_grupos, porra_mejores_terceros, partidos_bracket):

	conexion_usuario.actualizarEstadoPorraUsuario("nacho98")

	conexion_usuario.c.execute("UPDATE usuarios SET Admin=True")

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

	conexion_usuario.c.execute("""INSERT INTO eliminatorias_real VALUES('dieciseisavos', 'M73', 'republica-checa', 'canada', 'republica-checa')""")

	conexion_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra_grupos})

		cliente_abierto.post("/porra/mejores_terceros/guardar", json={"equipos":porra_mejores_terceros})

		cliente_abierto.post("/porra/eliminatorias/guardar", data={"elecciones_eliminatorias":json.dumps(partidos_bracket)})

		respuesta=cliente_abierto.put("/puntuacion/calcular_puntuacion")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/settings"
		assert "<h1>Redirecting...</h1>" in contenido

		conexion_usuario.c.execute("SELECT Puntos_Grupos, Puntos_Mejores_Terceros, Puntos_Eliminatorias, Puntos_Total FROM puntuaciones")

		puntuacion=conexion_usuario.c.fetchone()

		assert puntuacion["puntos_grupos"]==92
		assert puntuacion["puntos_mejores_terceros"]==12
		assert puntuacion["puntos_eliminatorias"]==8
		assert puntuacion["puntos_total"]==112

def test_pagina_calcular_puntuaciones_una_ronda_real(cliente, conexion_usuario, porra_grupos, porra_mejores_terceros, partidos_bracket):

	conexion_usuario.actualizarEstadoPorraUsuario("nacho98")

	conexion_usuario.c.execute("UPDATE usuarios SET Admin=True")

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
																		('dieciseisavos', 'M88', 'seleccion-estados-unidos', 'seleccion-egipto', 'seleccion-estados-unidos')""")

	conexion_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra_grupos})

		cliente_abierto.post("/porra/mejores_terceros/guardar", json={"equipos":porra_mejores_terceros})

		cliente_abierto.post("/porra/eliminatorias/guardar", data={"elecciones_eliminatorias":json.dumps(partidos_bracket)})

		respuesta=cliente_abierto.put("/puntuacion/calcular_puntuacion")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/settings"
		assert "<h1>Redirecting...</h1>" in contenido

		conexion_usuario.c.execute("SELECT Puntos_Grupos, Puntos_Mejores_Terceros, Puntos_Eliminatorias, Puntos_Total FROM puntuaciones")

		puntuacion=conexion_usuario.c.fetchone()

		assert puntuacion["puntos_grupos"]==92
		assert puntuacion["puntos_mejores_terceros"]==12
		assert puntuacion["puntos_eliminatorias"]==112
		assert puntuacion["puntos_total"]==216

def test_pagina_calcular_puntuaciones_un_partido_dos_rondas_real(cliente, conexion_usuario, porra_grupos, porra_mejores_terceros, partidos_bracket):

	conexion_usuario.actualizarEstadoPorraUsuario("nacho98")

	conexion_usuario.c.execute("UPDATE usuarios SET Admin=True")

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
										('octavos', 'M89', 'seleccion-alemania', 'seleccion-francia', 'seleccion-francia')""")

	conexion_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra_grupos})

		cliente_abierto.post("/porra/mejores_terceros/guardar", json={"equipos":porra_mejores_terceros})

		cliente_abierto.post("/porra/eliminatorias/guardar", data={"elecciones_eliminatorias":json.dumps(partidos_bracket)})

		respuesta=cliente_abierto.put("/puntuacion/calcular_puntuacion")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/settings"
		assert "<h1>Redirecting...</h1>" in contenido

		conexion_usuario.c.execute("SELECT Puntos_Grupos, Puntos_Mejores_Terceros, Puntos_Eliminatorias, Puntos_Total FROM puntuaciones")

		puntuacion=conexion_usuario.c.fetchone()

		assert puntuacion["puntos_grupos"]==92
		assert puntuacion["puntos_mejores_terceros"]==12
		assert puntuacion["puntos_eliminatorias"]==124
		assert puntuacion["puntos_total"]==228

def test_pagina_calcular_puntuaciones_dos_rondas_real(cliente, conexion_usuario, porra_grupos, porra_mejores_terceros, partidos_bracket):

	conexion_usuario.actualizarEstadoPorraUsuario("nacho98")

	conexion_usuario.c.execute("UPDATE usuarios SET Admin=True")

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
										('octavos', 'M96', 'seleccion-suiza', 'seleccion-portugal', 'seleccion-portugal')""")

	conexion_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra_grupos})

		cliente_abierto.post("/porra/mejores_terceros/guardar", json={"equipos":porra_mejores_terceros})

		cliente_abierto.post("/porra/eliminatorias/guardar", data={"elecciones_eliminatorias":json.dumps(partidos_bracket)})

		respuesta=cliente_abierto.put("/puntuacion/calcular_puntuacion")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/settings"
		assert "<h1>Redirecting...</h1>" in contenido

		conexion_usuario.c.execute("SELECT Puntos_Grupos, Puntos_Mejores_Terceros, Puntos_Eliminatorias, Puntos_Total FROM puntuaciones")

		puntuacion=conexion_usuario.c.fetchone()

		assert puntuacion["puntos_grupos"]==92
		assert puntuacion["puntos_mejores_terceros"]==12
		assert puntuacion["puntos_eliminatorias"]==160
		assert puntuacion["puntos_total"]==264

def test_pagina_calcular_puntuaciones_un_partido_tres_rondas_real(cliente, conexion_usuario, porra_grupos, porra_mejores_terceros, partidos_bracket):

	conexion_usuario.actualizarEstadoPorraUsuario("nacho98")

	conexion_usuario.c.execute("UPDATE usuarios SET Admin=True")

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
										('cuartos', 'M97', 'seleccion-francia', 'seleccion-holanda', 'seleccion-francia')""")

	conexion_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra_grupos})

		cliente_abierto.post("/porra/mejores_terceros/guardar", json={"equipos":porra_mejores_terceros})

		cliente_abierto.post("/porra/eliminatorias/guardar", data={"elecciones_eliminatorias":json.dumps(partidos_bracket)})

		respuesta=cliente_abierto.put("/puntuacion/calcular_puntuacion")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/settings"
		assert "<h1>Redirecting...</h1>" in contenido

		conexion_usuario.c.execute("SELECT Puntos_Grupos, Puntos_Mejores_Terceros, Puntos_Eliminatorias, Puntos_Total FROM puntuaciones")

		puntuacion=conexion_usuario.c.fetchone()

		assert puntuacion["puntos_grupos"]==92
		assert puntuacion["puntos_mejores_terceros"]==12
		assert puntuacion["puntos_eliminatorias"]==160
		assert puntuacion["puntos_total"]==264

def test_pagina_calcular_puntuaciones_tres_rondas_real(cliente, conexion_usuario, porra_grupos, porra_mejores_terceros, partidos_bracket):

	conexion_usuario.actualizarEstadoPorraUsuario("nacho98")

	conexion_usuario.c.execute("UPDATE usuarios SET Admin=True")

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
										('cuartos', 'M100', 'seleccion-portugal', 'seleccion-argentina', 'seleccion-argentina')""")

	conexion_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra_grupos})

		cliente_abierto.post("/porra/mejores_terceros/guardar", json={"equipos":porra_mejores_terceros})

		cliente_abierto.post("/porra/eliminatorias/guardar", data={"elecciones_eliminatorias":json.dumps(partidos_bracket)})

		respuesta=cliente_abierto.put("/puntuacion/calcular_puntuacion")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/settings"
		assert "<h1>Redirecting...</h1>" in contenido

		conexion_usuario.c.execute("SELECT Puntos_Grupos, Puntos_Mejores_Terceros, Puntos_Eliminatorias, Puntos_Total FROM puntuaciones")

		puntuacion=conexion_usuario.c.fetchone()

		assert puntuacion["puntos_grupos"]==92
		assert puntuacion["puntos_mejores_terceros"]==12
		assert puntuacion["puntos_eliminatorias"]==190
		assert puntuacion["puntos_total"]==294

def test_pagina_calcular_puntuaciones_un_partido_cuatro_rondas_real(cliente, conexion_usuario, porra_grupos, porra_mejores_terceros, partidos_bracket):

	conexion_usuario.actualizarEstadoPorraUsuario("nacho98")

	conexion_usuario.c.execute("UPDATE usuarios SET Admin=True")

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
										('semifinales', 'M101', 'seleccion-francia', 'seleccion-espanola', 'seleccion-espanola')""")

	conexion_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra_grupos})

		cliente_abierto.post("/porra/mejores_terceros/guardar", json={"equipos":porra_mejores_terceros})

		cliente_abierto.post("/porra/eliminatorias/guardar", data={"elecciones_eliminatorias":json.dumps(partidos_bracket)})

		respuesta=cliente_abierto.put("/puntuacion/calcular_puntuacion")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/settings"
		assert "<h1>Redirecting...</h1>" in contenido

		conexion_usuario.c.execute("SELECT Puntos_Grupos, Puntos_Mejores_Terceros, Puntos_Eliminatorias, Puntos_Total FROM puntuaciones")

		puntuacion=conexion_usuario.c.fetchone()

		assert puntuacion["puntos_grupos"]==92
		assert puntuacion["puntos_mejores_terceros"]==12
		assert puntuacion["puntos_eliminatorias"]==205
		assert puntuacion["puntos_total"]==309

def test_pagina_calcular_puntuaciones_cuatro_rondas_real(cliente, conexion_usuario, porra_grupos, porra_mejores_terceros, partidos_bracket):

	conexion_usuario.actualizarEstadoPorraUsuario("nacho98")

	conexion_usuario.c.execute("UPDATE usuarios SET Admin=True")

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
										('semifinales', 'M102', 'seleccion-brasil', 'seleccion-argentina', 'seleccion-argentina')""")

	conexion_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra_grupos})

		cliente_abierto.post("/porra/mejores_terceros/guardar", json={"equipos":porra_mejores_terceros})

		cliente_abierto.post("/porra/eliminatorias/guardar", data={"elecciones_eliminatorias":json.dumps(partidos_bracket)})

		respuesta=cliente_abierto.put("/puntuacion/calcular_puntuacion")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/settings"
		assert "<h1>Redirecting...</h1>" in contenido

		conexion_usuario.c.execute("SELECT Puntos_Grupos, Puntos_Mejores_Terceros, Puntos_Eliminatorias, Puntos_Total FROM puntuaciones")

		puntuacion=conexion_usuario.c.fetchone()

		assert puntuacion["puntos_grupos"]==92
		assert puntuacion["puntos_mejores_terceros"]==12
		assert puntuacion["puntos_eliminatorias"]==235
		assert puntuacion["puntos_total"]==339

def test_pagina_calcular_puntuaciones_cinco_rondas_real(cliente, conexion_usuario, porra_grupos, porra_mejores_terceros, partidos_bracket):

	conexion_usuario.actualizarEstadoPorraUsuario("nacho98")

	conexion_usuario.c.execute("UPDATE usuarios SET Admin=True")

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
										('tercer_puesto', 'M103', 'seleccion-francia', 'seleccion-brasil', 'seleccion-francia')""")

	conexion_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra_grupos})

		cliente_abierto.post("/porra/mejores_terceros/guardar", json={"equipos":porra_mejores_terceros})

		cliente_abierto.post("/porra/eliminatorias/guardar", data={"elecciones_eliminatorias":json.dumps(partidos_bracket)})

		respuesta=cliente_abierto.put("/puntuacion/calcular_puntuacion")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/settings"
		assert "<h1>Redirecting...</h1>" in contenido

		conexion_usuario.c.execute("SELECT Puntos_Grupos, Puntos_Mejores_Terceros, Puntos_Eliminatorias, Puntos_Total FROM puntuaciones")

		puntuacion=conexion_usuario.c.fetchone()

		assert puntuacion["puntos_grupos"]==92
		assert puntuacion["puntos_mejores_terceros"]==12
		assert puntuacion["puntos_eliminatorias"]==247
		assert puntuacion["puntos_total"]==351

def test_pagina_calcular_puntuaciones_seis_rondas_real(cliente, conexion_usuario, porra_grupos, porra_mejores_terceros, partidos_bracket):

	conexion_usuario.actualizarEstadoPorraUsuario("nacho98")

	conexion_usuario.c.execute("UPDATE usuarios SET Admin=True")

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
										('final', 'M104', 'seleccion-espanola', 'seleccion-brasil', 'seleccion-brasil')""")

	conexion_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra_grupos})

		cliente_abierto.post("/porra/mejores_terceros/guardar", json={"equipos":porra_mejores_terceros})

		cliente_abierto.post("/porra/eliminatorias/guardar", data={"elecciones_eliminatorias":json.dumps(partidos_bracket)})

		respuesta=cliente_abierto.put("/puntuacion/calcular_puntuacion")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/settings"
		assert "<h1>Redirecting...</h1>" in contenido

		conexion_usuario.c.execute("SELECT Puntos_Grupos, Puntos_Mejores_Terceros, Puntos_Eliminatorias, Puntos_Total FROM puntuaciones")

		puntuacion=conexion_usuario.c.fetchone()

		assert puntuacion["puntos_grupos"]==92
		assert puntuacion["puntos_mejores_terceros"]==12
		assert puntuacion["puntos_eliminatorias"]==267
		assert puntuacion["puntos_total"]==371

def test_pagina_calcular_puntuaciones_bonus_campeon(cliente, conexion_usuario, porra_grupos, porra_mejores_terceros, partidos_bracket):

	conexion_usuario.actualizarEstadoPorraUsuario("nacho98")

	conexion_usuario.c.execute("UPDATE usuarios SET Admin=True")

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
										('final', 'M104', 'seleccion-espanola', 'seleccion-brasil', 'seleccion-espanola')""")

	conexion_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra_grupos})

		cliente_abierto.post("/porra/mejores_terceros/guardar", json={"equipos":porra_mejores_terceros})

		cliente_abierto.post("/porra/eliminatorias/guardar", data={"elecciones_eliminatorias":json.dumps(partidos_bracket)})

		respuesta=cliente_abierto.put("/puntuacion/calcular_puntuacion")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/settings"
		assert "<h1>Redirecting...</h1>" in contenido

		conexion_usuario.c.execute("SELECT Puntos_Grupos, Puntos_Mejores_Terceros, Puntos_Eliminatorias, Puntos_Total FROM puntuaciones")

		puntuacion=conexion_usuario.c.fetchone()

		assert puntuacion["puntos_grupos"]==92
		assert puntuacion["puntos_mejores_terceros"]==12
		assert puntuacion["puntos_eliminatorias"]==302
		assert puntuacion["puntos_total"]==406

def test_pagina_calcular_puntuaciones_bonus_final_exacta(cliente, conexion_usuario, porra_grupos, porra_mejores_terceros, partidos_bracket):

	conexion_usuario.actualizarEstadoPorraUsuario("nacho98")

	conexion_usuario.c.execute("UPDATE usuarios SET Admin=True")

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
										('final', 'M104', 'seleccion-espanola', 'seleccion-argentina', 'seleccion-argentina')""")

	conexion_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra_grupos})

		cliente_abierto.post("/porra/mejores_terceros/guardar", json={"equipos":porra_mejores_terceros})

		cliente_abierto.post("/porra/eliminatorias/guardar", data={"elecciones_eliminatorias":json.dumps(partidos_bracket)})

		respuesta=cliente_abierto.put("/puntuacion/calcular_puntuacion")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/settings"
		assert "<h1>Redirecting...</h1>" in contenido

		conexion_usuario.c.execute("SELECT Puntos_Grupos, Puntos_Mejores_Terceros, Puntos_Eliminatorias, Puntos_Total FROM puntuaciones")

		puntuacion=conexion_usuario.c.fetchone()

		assert puntuacion["puntos_grupos"]==92
		assert puntuacion["puntos_mejores_terceros"]==12
		assert puntuacion["puntos_eliminatorias"]==302
		assert puntuacion["puntos_total"]==406

def test_pagina_calcular_puntuaciones_bonus_campeon_final_exacta(cliente, conexion_usuario, porra_grupos, porra_mejores_terceros, partidos_bracket):

	conexion_usuario.actualizarEstadoPorraUsuario("nacho98")

	conexion_usuario.c.execute("UPDATE usuarios SET Admin=True")

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
										('final', 'M104', 'seleccion-espanola', 'seleccion-argentina', 'seleccion-espanola')""")

	conexion_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra_grupos})

		cliente_abierto.post("/porra/mejores_terceros/guardar", json={"equipos":porra_mejores_terceros})

		cliente_abierto.post("/porra/eliminatorias/guardar", data={"elecciones_eliminatorias":json.dumps(partidos_bracket)})

		respuesta=cliente_abierto.put("/puntuacion/calcular_puntuacion")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/settings"
		assert "<h1>Redirecting...</h1>" in contenido

		conexion_usuario.c.execute("SELECT Puntos_Grupos, Puntos_Mejores_Terceros, Puntos_Eliminatorias, Puntos_Total FROM puntuaciones")

		puntuacion=conexion_usuario.c.fetchone()

		assert puntuacion["puntos_grupos"]==92
		assert puntuacion["puntos_mejores_terceros"]==12
		assert puntuacion["puntos_eliminatorias"]==337
		assert puntuacion["puntos_total"]==441