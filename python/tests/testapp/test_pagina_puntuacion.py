import pytest

def test_pagina_calcular_puntuaciones_sin_login(cliente, conexion):

	respuesta=cliente.put("/calcular_puntuacion", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

def test_pagina_calcular_puntuaciones_no_admin(cliente, conexion_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.put("/calcular_puntuacion")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/porra"
		assert "<h1>Redirecting...</h1>" in contenido

def test_pagina_calcular_puntuaciones_sin_porra_completada(cliente, conexion_usuario):

	conexion_usuario.c.execute("UPDATE usuarios SET Admin=True")

	conexion_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.put("/calcular_puntuacion")

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

		respuesta=cliente_abierto.put("/calcular_puntuacion")

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

		respuesta=cliente_abierto.put("/calcular_puntuacion")

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

		respuesta=cliente_abierto.put("/calcular_puntuacion")

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

		respuesta=cliente_abierto.put("/calcular_puntuacion")

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

		respuesta=cliente_abierto.put("/calcular_puntuacion")

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

		respuesta=cliente_abierto.put("/calcular_puntuacion")

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