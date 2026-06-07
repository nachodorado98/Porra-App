def test_pagina_resultados_sin_login(cliente, conexion):

	respuesta=cliente.get("/resultados", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

def test_pagina_resultados_sin_empezar(cliente, conexion_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/resultados")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<h1 class="titulo-pagina">Resultados Oficiales' in contenido
		assert '<p class="descripcion-grupos">Aquí puedes ver la clasificación real del torneo conforme se vaya actualizando.</p>' in contenido
		assert '<h2 class="titulo-seccion">Fase de grupos' not in contenido
		assert '<div class="grupos-grid">' not in contenido
		assert '<div class="grupo-container">' not in contenido
		assert '<h2>Grupo A</h2>' not in contenido
		assert '<h2>Grupo B</h2>' not in contenido
		assert '<span class="nombre-equipo">Corea del Sur</span>' not in contenido
		assert '<span class="nombre-equipo">México</span>' not in contenido
		assert "<h3>La fase de grupos todavía no ha comenzado</h3>" in contenido
		assert '<h2 class="titulo-seccion">Mejores terceros' not in contenido
		assert '<div class="terceros-grid">' not in contenido
		assert '<div class="tercero-card">' not in contenido
		assert '<div class="grupo-badge">Grupo E</div>' not in contenido
		assert '<div class="grupo-badge">Grupo F</div>' not in contenido
		assert '<div class="tercero-nombre-equipo">Curazao</div>' not in contenido
		assert '<div class="tercero-nombre-equipo">Suecia</div>' not in contenido
		assert "<h3>Los mejores terceros todavía están por decidirse</h3>" in contenido
		assert '<h2 class="titulo-seccion">Fase eliminatoria' not in contenido
		assert '"M73": {"equipo_1":' not in contenido
		assert '"ganador": null'  not in contenido
		assert '"partido": "M73", "ronda": "dieciseisavos"' not in contenido
		assert '"ganador": {' not in contenido
		assert '"M101": {"equipo_1":' not in contenido
		assert '"M89": {"equipo_1":' not in contenido
		assert "<h3>La fase eliminatoria aún no ha comenzado</h3>" in contenido
		assert '<div class="mensaje-vacio">' in contenido
		assert '<div class="mensaje-vacio-icono">' in contenido

def test_pagina_resultados_solo_grupos_un_grupo_un_equipo(cliente, conexion_usuario):

	conexion_usuario.c.execute("INSERT INTO grupo_equipos_real VALUES ('A', 'seleccion-republica-corea', 1)")

	conexion_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/resultados")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<h1 class="titulo-pagina">Resultados Oficiales' in contenido
		assert '<p class="descripcion-grupos">Aquí puedes ver la clasificación real del torneo conforme se vaya actualizando.</p>' in contenido
		assert '<h2 class="titulo-seccion">Fase de grupos' in contenido
		assert '<div class="grupos-grid">' in contenido
		assert '<div class="grupo-container">' in contenido
		assert '<h2>Grupo A</h2>' in contenido
		assert '<h2>Grupo B</h2>' not in contenido
		assert '<span class="nombre-equipo">Corea del Sur</span>' in contenido
		assert '<span class="nombre-equipo">México</span>' not in contenido
		assert "<h3>La fase de grupos todavía no ha comenzado</h3>" not in contenido
		assert '<h2 class="titulo-seccion">Mejores terceros' not in contenido
		assert '<div class="terceros-grid">' not in contenido
		assert '<div class="tercero-card">' not in contenido
		assert '<div class="grupo-badge">Grupo E</div>' not in contenido
		assert '<div class="grupo-badge">Grupo F</div>' not in contenido
		assert '<div class="tercero-nombre-equipo">Curazao</div>' not in contenido
		assert '<div class="tercero-nombre-equipo">Suecia</div>' not in contenido
		assert "<h3>Los mejores terceros todavía están por decidirse</h3>" in contenido
		assert '<h2 class="titulo-seccion">Fase eliminatoria' not in contenido
		assert '"M73": {"equipo_1":' not in contenido
		assert '"ganador": null'  not in contenido
		assert '"partido": "M73", "ronda": "dieciseisavos"' not in contenido
		assert '"ganador": {' not in contenido
		assert '"M101": {"equipo_1":' not in contenido
		assert '"M89": {"equipo_1":' not in contenido
		assert "<h3>La fase eliminatoria aún no ha comenzado</h3>" in contenido
		assert '<div class="mensaje-vacio">' in contenido
		assert '<div class="mensaje-vacio-icono">' in contenido

def test_pagina_resultados_solo_grupos_un_grupo(cliente, conexion_usuario):

	conexion_usuario.c.execute("""INSERT INTO grupo_equipos_real
								VALUES ('A', 'seleccion-republica-corea', 1), ('A', 'seleccion-mexico', 2), ('A', 'republica-checa', 3), ('A', 'seleccion-sudafrica', 4)""")

	conexion_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/resultados")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<h1 class="titulo-pagina">Resultados Oficiales' in contenido
		assert '<p class="descripcion-grupos">Aquí puedes ver la clasificación real del torneo conforme se vaya actualizando.</p>' in contenido
		assert '<h2 class="titulo-seccion">Fase de grupos' in contenido
		assert '<div class="grupos-grid">' in contenido
		assert '<div class="grupo-container">' in contenido
		assert '<h2>Grupo A</h2>' in contenido
		assert '<h2>Grupo B</h2>' not in contenido
		assert '<span class="nombre-equipo">Corea del Sur</span>' in contenido
		assert '<span class="nombre-equipo">México</span>' in contenido
		assert "<h3>La fase de grupos todavía no ha comenzado</h3>" not in contenido
		assert '<h2 class="titulo-seccion">Mejores terceros' not in contenido
		assert '<div class="terceros-grid">' not in contenido
		assert '<div class="tercero-card">' not in contenido
		assert '<div class="grupo-badge">Grupo E</div>' not in contenido
		assert '<div class="grupo-badge">Grupo F</div>' not in contenido
		assert '<div class="tercero-nombre-equipo">Curazao</div>' not in contenido
		assert '<div class="tercero-nombre-equipo">Suecia</div>' not in contenido
		assert "<h3>Los mejores terceros todavía están por decidirse</h3>" in contenido
		assert '<h2 class="titulo-seccion">Fase eliminatoria' not in contenido
		assert '"M73": {"equipo_1":' not in contenido
		assert '"ganador": null'  not in contenido
		assert '"partido": "M73", "ronda": "dieciseisavos"' not in contenido
		assert '"ganador": {' not in contenido
		assert '"M101": {"equipo_1":' not in contenido
		assert '"M89": {"equipo_1":' not in contenido
		assert "<h3>La fase eliminatoria aún no ha comenzado</h3>" in contenido
		assert '<div class="mensaje-vacio">' in contenido
		assert '<div class="mensaje-vacio-icono">' in contenido

def test_pagina_resultados_solo_grupos_varios_grupos(cliente, conexion_usuario):

	conexion_usuario.c.execute("""INSERT INTO grupo_equipos_real
									VALUES ('A', 'seleccion-republica-corea', 1), ('A', 'seleccion-mexico', 2), ('A', 'republica-checa', 3), ('A', 'seleccion-sudafrica', 4),
											('B', 'seleccion-bosnia-herzegovina', 1), ('B', 'canada', 2), ('B', 'seleccion-qatar', 3), ('B', 'seleccion-suiza', 4)""")

	conexion_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/resultados")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<h1 class="titulo-pagina">Resultados Oficiales' in contenido
		assert '<p class="descripcion-grupos">Aquí puedes ver la clasificación real del torneo conforme se vaya actualizando.</p>' in contenido
		assert '<h2 class="titulo-seccion">Fase de grupos' in contenido
		assert '<div class="grupos-grid">' in contenido
		assert '<div class="grupo-container">' in contenido
		assert '<h2>Grupo A</h2>' in contenido
		assert '<h2>Grupo B</h2>' in contenido
		assert '<span class="nombre-equipo">Corea del Sur</span>' in contenido
		assert '<span class="nombre-equipo">México</span>' in contenido
		assert "<h3>La fase de grupos todavía no ha comenzado</h3>" not in contenido
		assert '<h2 class="titulo-seccion">Mejores terceros' not in contenido
		assert '<div class="terceros-grid">' not in contenido
		assert '<div class="tercero-card">' not in contenido
		assert '<div class="grupo-badge">Grupo E</div>' not in contenido
		assert '<div class="grupo-badge">Grupo F</div>' not in contenido
		assert '<div class="tercero-nombre-equipo">Curazao</div>' not in contenido
		assert '<div class="tercero-nombre-equipo">Suecia</div>' not in contenido
		assert "<h3>Los mejores terceros todavía están por decidirse</h3>" in contenido
		assert '<h2 class="titulo-seccion">Fase eliminatoria' not in contenido
		assert '"M73": {"equipo_1":' not in contenido
		assert '"ganador": null'  not in contenido
		assert '"partido": "M73", "ronda": "dieciseisavos"' not in contenido
		assert '"ganador": {' not in contenido
		assert '"M101": {"equipo_1":' not in contenido
		assert '"M89": {"equipo_1":' not in contenido
		assert "<h3>La fase eliminatoria aún no ha comenzado</h3>" in contenido
		assert '<div class="mensaje-vacio">' in contenido
		assert '<div class="mensaje-vacio-icono">' in contenido

def test_pagina_resultados_grupos_mejores_terceros_un_mejor_tercero(cliente, conexion_usuario):

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

	conexion_usuario.c.execute("""INSERT INTO mejores_terceros_real VALUES ('E', 'curazao', 1)""")

	conexion_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/resultados")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<h1 class="titulo-pagina">Resultados Oficiales' in contenido
		assert '<p class="descripcion-grupos">Aquí puedes ver la clasificación real del torneo conforme se vaya actualizando.</p>' in contenido
		assert '<h2 class="titulo-seccion">Fase de grupos' in contenido
		assert '<div class="grupos-grid">' in contenido
		assert '<div class="grupo-container">' in contenido
		assert '<h2>Grupo A</h2>' in contenido
		assert '<h2>Grupo B</h2>' in contenido
		assert '<span class="nombre-equipo">Corea del Sur</span>' in contenido
		assert '<span class="nombre-equipo">México</span>' in contenido
		assert "<h3>La fase de grupos todavía no ha comenzado</h3>" not in contenido
		assert '<h2 class="titulo-seccion">Mejores terceros' in contenido
		assert '<div class="terceros-grid">' in contenido
		assert '<div class="tercero-card">' in contenido
		assert '<div class="grupo-badge">Grupo E</div>' in contenido
		assert '<div class="grupo-badge">Grupo F</div>' not in contenido
		assert '<div class="tercero-nombre-equipo">Curazao</div>' in contenido
		assert '<div class="tercero-nombre-equipo">Suecia</div>' not in contenido
		assert "<h3>Los mejores terceros todavía están por decidirse</h3>" not in contenido
		assert '<h2 class="titulo-seccion">Fase eliminatoria' not in contenido
		assert '"M73": {"equipo_1":' not in contenido
		assert '"ganador": null'  not in contenido
		assert '"partido": "M73", "ronda": "dieciseisavos"' not in contenido
		assert '"ganador": {' not in contenido
		assert '"M101": {"equipo_1":' not in contenido
		assert '"M89": {"equipo_1":' not in contenido
		assert "<h3>La fase eliminatoria aún no ha comenzado</h3>" in contenido
		assert '<div class="mensaje-vacio">' in contenido
		assert '<div class="mensaje-vacio-icono">' in contenido

def test_pagina_resultados_grupos_mejores_terceros_varios_mejor_terceros(cliente, conexion_usuario):

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

	conexion_usuario.c.execute("""INSERT INTO mejores_terceros_real VALUES ('E', 'curazao', 1), ('F', 'seleccion-suecia', 2)""")

	conexion_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/resultados")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<h1 class="titulo-pagina">Resultados Oficiales' in contenido
		assert '<p class="descripcion-grupos">Aquí puedes ver la clasificación real del torneo conforme se vaya actualizando.</p>' in contenido
		assert '<h2 class="titulo-seccion">Fase de grupos' in contenido
		assert '<div class="grupos-grid">' in contenido
		assert '<div class="grupo-container">' in contenido
		assert '<h2>Grupo A</h2>' in contenido
		assert '<h2>Grupo B</h2>' in contenido
		assert '<span class="nombre-equipo">Corea del Sur</span>' in contenido
		assert '<span class="nombre-equipo">México</span>' in contenido
		assert "<h3>La fase de grupos todavía no ha comenzado</h3>" not in contenido
		assert '<h2 class="titulo-seccion">Mejores terceros' in contenido
		assert '<div class="terceros-grid">' in contenido
		assert '<div class="tercero-card">' in contenido
		assert '<div class="grupo-badge">Grupo E</div>' in contenido
		assert '<div class="grupo-badge">Grupo F</div>' in contenido
		assert '<div class="tercero-nombre-equipo">Curazao</div>' in contenido
		assert '<div class="tercero-nombre-equipo">Suecia</div>' in contenido
		assert "<h3>Los mejores terceros todavía están por decidirse</h3>" not in contenido
		assert '<h2 class="titulo-seccion">Fase eliminatoria' not in contenido
		assert '"M73": {"equipo_1":' not in contenido
		assert '"ganador": null'  not in contenido
		assert '"partido": "M73", "ronda": "dieciseisavos"' not in contenido
		assert '"ganador": {' not in contenido
		assert '"M101": {"equipo_1":' not in contenido
		assert '"M89": {"equipo_1":' not in contenido
		assert "<h3>La fase eliminatoria aún no ha comenzado</h3>" in contenido
		assert '<div class="mensaje-vacio">' in contenido
		assert '<div class="mensaje-vacio-icono">' in contenido

def test_pagina_resultados_grupos_mejores_terceros_eliminatorias_una_eliminatoria_sin_ganador(cliente, conexion_usuario):

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
																			('C', 'seleccion-escocia', 3),
																			('E', 'curazao', 4),
																			('F', 'seleccion-suecia', 5),
																			('K', 'rd-congo', 6),
																			('L', 'seleccion-ghana', 7),
																			('H', 'seleccion-arabia-saudi', 8);""")

	conexion_usuario.c.execute("""INSERT INTO eliminatorias_real VALUES('dieciseisavos', 'M73', 'republica-checa', 'canada', NULL)""")

	conexion_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/resultados")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<h1 class="titulo-pagina">Resultados Oficiales' in contenido
		assert '<p class="descripcion-grupos">Aquí puedes ver la clasificación real del torneo conforme se vaya actualizando.</p>' in contenido
		assert '<h2 class="titulo-seccion">Fase de grupos' in contenido
		assert '<div class="grupos-grid">' in contenido
		assert '<div class="grupo-container">' in contenido
		assert '<h2>Grupo A</h2>' in contenido
		assert '<h2>Grupo B</h2>' in contenido
		assert '<span class="nombre-equipo">Corea del Sur</span>' in contenido
		assert '<span class="nombre-equipo">México</span>' in contenido
		assert "<h3>La fase de grupos todavía no ha comenzado</h3>" not in contenido
		assert '<h2 class="titulo-seccion">Mejores terceros' in contenido
		assert '<div class="terceros-grid">' in contenido
		assert '<div class="tercero-card">' in contenido
		assert '<div class="grupo-badge">Grupo E</div>' in contenido
		assert '<div class="grupo-badge">Grupo F</div>' in contenido
		assert '<div class="tercero-nombre-equipo">Curazao</div>' in contenido
		assert '<div class="tercero-nombre-equipo">Suecia</div>' in contenido
		assert "<h3>Los mejores terceros todavía están por decidirse</h3>" not in contenido
		assert '<h2 class="titulo-seccion">Fase eliminatoria' in contenido
		assert '"M73": {"equipo_1":' in contenido
		assert '"ganador": null'  in contenido
		assert '"partido": "M73", "ronda": "dieciseisavos"' in contenido
		assert '"ganador": {' not in contenido
		assert '"M101": {"equipo_1":' not in contenido
		assert '"M89": {"equipo_1":' not in contenido
		assert "<h3>La fase eliminatoria aún no ha comenzado</h3>" not in contenido
		assert '<div class="mensaje-vacio">' not in contenido
		assert '<div class="mensaje-vacio-icono">' not in contenido

def test_pagina_resultados_grupos_mejores_terceros_eliminatorias_una_eliminatoria_con_ganador(cliente, conexion_usuario):

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
																			('C', 'seleccion-escocia', 3),
																			('E', 'curazao', 4),
																			('F', 'seleccion-suecia', 5),
																			('K', 'rd-congo', 6),
																			('L', 'seleccion-ghana', 7),
																			('H', 'seleccion-arabia-saudi', 8);""")

	conexion_usuario.c.execute("""INSERT INTO eliminatorias_real VALUES('dieciseisavos', 'M73', 'republica-checa', 'canada', 'republica-checa')""")

	conexion_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/resultados")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<h1 class="titulo-pagina">Resultados Oficiales' in contenido
		assert '<p class="descripcion-grupos">Aquí puedes ver la clasificación real del torneo conforme se vaya actualizando.</p>' in contenido
		assert '<h2 class="titulo-seccion">Fase de grupos' in contenido
		assert '<div class="grupos-grid">' in contenido
		assert '<div class="grupo-container">' in contenido
		assert '<h2>Grupo A</h2>' in contenido
		assert '<h2>Grupo B</h2>' in contenido
		assert '<span class="nombre-equipo">Corea del Sur</span>' in contenido
		assert '<span class="nombre-equipo">México</span>' in contenido
		assert "<h3>La fase de grupos todavía no ha comenzado</h3>" not in contenido
		assert '<h2 class="titulo-seccion">Mejores terceros' in contenido
		assert '<div class="terceros-grid">' in contenido
		assert '<div class="tercero-card">' in contenido
		assert '<div class="grupo-badge">Grupo E</div>' in contenido
		assert '<div class="grupo-badge">Grupo F</div>' in contenido
		assert '<div class="tercero-nombre-equipo">Curazao</div>' in contenido
		assert '<div class="tercero-nombre-equipo">Suecia</div>' in contenido
		assert "<h3>Los mejores terceros todavía están por decidirse</h3>" not in contenido
		assert '<h2 class="titulo-seccion">Fase eliminatoria' in contenido
		assert '"M73": {"equipo_1":' in contenido
		assert '"ganador": null' not  in contenido
		assert '"partido": "M73", "ronda": "dieciseisavos"' in contenido
		assert '"ganador": {' in contenido
		assert '"M101": {"equipo_1":' not in contenido
		assert '"M89": {"equipo_1":' not in contenido
		assert "<h3>La fase eliminatoria aún no ha comenzado</h3>" not in contenido
		assert '<div class="mensaje-vacio">' not in contenido
		assert '<div class="mensaje-vacio-icono">' not in contenido

def test_pagina_resultados_grupos_mejores_terceros_eliminatorias_varias_eliminatorias(cliente, conexion_usuario):

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
																			('C', 'seleccion-escocia', 3),
																			('E', 'curazao', 4),
																			('F', 'seleccion-suecia', 5),
																			('K', 'rd-congo', 6),
																			('L', 'seleccion-ghana', 7),
																			('H', 'seleccion-arabia-saudi', 8);""")

	conexion_usuario.c.execute("""INSERT INTO eliminatorias_real VALUES('dieciseisavos', 'M73', 'republica-checa', 'canada', 'republica-checa'),
																		('octavos', 'M89', 'seleccion-alemania', 'seleccion-francia', 'seleccion-francia'),
																		('semifinales', 'M101', 'seleccion-francia', 'seleccion-espanola', 'seleccion-espanola')""")

	conexion_usuario.confirmar()

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/resultados")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==200
		assert '<h1 class="titulo-pagina">Resultados Oficiales' in contenido
		assert '<p class="descripcion-grupos">Aquí puedes ver la clasificación real del torneo conforme se vaya actualizando.</p>' in contenido
		assert '<h2 class="titulo-seccion">Fase de grupos' in contenido
		assert '<div class="grupos-grid">' in contenido
		assert '<div class="grupo-container">' in contenido
		assert '<h2>Grupo A</h2>' in contenido
		assert '<h2>Grupo B</h2>' in contenido
		assert '<span class="nombre-equipo">Corea del Sur</span>' in contenido
		assert '<span class="nombre-equipo">México</span>' in contenido
		assert "<h3>La fase de grupos todavía no ha comenzado</h3>" not in contenido
		assert '<h2 class="titulo-seccion">Mejores terceros' in contenido
		assert '<div class="terceros-grid">' in contenido
		assert '<div class="tercero-card">' in contenido
		assert '<div class="grupo-badge">Grupo E</div>' in contenido
		assert '<div class="grupo-badge">Grupo F</div>' in contenido
		assert '<div class="tercero-nombre-equipo">Curazao</div>' in contenido
		assert '<div class="tercero-nombre-equipo">Suecia</div>' in contenido
		assert "<h3>Los mejores terceros todavía están por decidirse</h3>" not in contenido
		assert '<h2 class="titulo-seccion">Fase eliminatoria' in contenido
		assert '"M73": {"equipo_1":' in contenido
		assert '"ganador": null' not  in contenido
		assert '"partido": "M73", "ronda": "dieciseisavos"' in contenido
		assert '"ganador": {' in contenido
		assert '"M101": {"equipo_1":' in contenido
		assert '"M89": {"equipo_1":' in contenido
		assert "<h3>La fase eliminatoria aún no ha comenzado</h3>" not in contenido
		assert '<div class="mensaje-vacio">' not in contenido
		assert '<div class="mensaje-vacio-icono">' not in contenido