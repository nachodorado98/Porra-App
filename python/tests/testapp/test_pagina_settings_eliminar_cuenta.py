def test_pagina_settings_eliminar_cuenta_sin_login(cliente, conexion):

	respuesta=cliente.get("/settings", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

def test_pagina_settings_eliminar_cuenta(cliente, conexion_usuario):

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		respuesta=cliente_abierto.get("/settings/eliminar_cuenta")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/"
		assert "<h1>Redirecting...</h1>" in contenido

		conexion_usuario.c.execute("SELECT * FROM usuarios")

		assert not conexion_usuario.c.fetchall()

def test_pagina_settings_eliminar_cuenta_porra_hecha(cliente, conexion_usuario):

	porra={'A': ['republica-checa', 'seleccion-republica-corea', 'seleccion-mexico', 'seleccion-sudafrica'],
			'B': ['canada', 'seleccion-bosnia-herzegovina', 'seleccion-suiza', 'seleccion-qatar'],
			'C': ['seleccion-marruecos', 'seleccion-escocia', 'seleccion-brasil', 'haiti'],
			'D': ['seleccion-estados-unidos', 'seleccion-paraguay', 'seleccion-turquia', 'seleccion-australia'],
			'E': ['seleccion-ecuador', 'seleccion-costa-marfil', 'seleccion-alemania', 'curazao'],
			'F': ['seleccion-japon', 'seleccion-suecia', 'seleccion-holanda', 'seleccion-tunez'],
			'G': ['seleccion-egipto', 'seleccion-iran', 'seleccion-belgica', 'seleccion-nueva-zelanda'],
			'H': ['seleccion-uruguay', 'seleccion-arabia-saudi', 'seleccion-espanola', 'cabo-verde'],
			'I': ['seleccion-noruega', 'senegal', 'seleccion-francia', 'seleccion-iraq'],
			'J': ['seleccion-austria', 'seleccion-argelia', 'seleccion-argentina', 'jordania'],
			'K': ['seleccion-colombia', 'rd-congo', 'seleccion-portugal', 'seleccion-uzbekistan'],
			'L': ['seleccion-croacia', 'seleccion-ghana', 'seleccion-inglaterra', 'panama-seleccion']}

	porra_mejores_terceros=[{'equipo_id': 'seleccion-brasil', 'grupo': 'C'},
				            {'equipo_id': 'seleccion-espanola', 'grupo': 'H'},
				            {'equipo_id': 'seleccion-alemania', 'grupo': 'E'},
				            {'equipo_id': 'seleccion-holanda', 'grupo': 'F'},
				            {'equipo_id': 'seleccion-francia', 'grupo': 'I'},
				            {'equipo_id': 'seleccion-argentina', 'grupo': 'J'},
				            {'equipo_id': 'seleccion-portugal', 'grupo': 'K'},
				            {'equipo_id': 'seleccion-inglaterra', 'grupo': 'L'}]

	with cliente as cliente_abierto:

		cliente_abierto.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

		cliente_abierto.post("/porra/grupos/guardar", json={"grupos":porra})

		cliente_abierto.post("/porra/mejores_terceros/guardar", json={"equipos":porra_mejores_terceros})

		conexion_usuario.c.execute("SELECT * FROM grupo_equipos_porra")

		assert conexion_usuario.c.fetchall()

		conexion_usuario.c.execute("SELECT * FROM mejores_terceros_porra")

		assert conexion_usuario.c.fetchall()

		conexion_usuario.c.execute("SELECT grupos_completados, mejores_terceros_completados FROM estado_porra")

		estado=conexion_usuario.c.fetchone()

		assert estado["grupos_completados"]
		assert estado["mejores_terceros_completados"]

		respuesta=cliente_abierto.get("/settings/eliminar_cuenta")

		contenido=respuesta.data.decode()

		assert respuesta.status_code==302
		assert respuesta.location=="/"
		assert "<h1>Redirecting...</h1>" in contenido

		conexion_usuario.c.execute("SELECT * FROM usuarios")

		assert not conexion_usuario.c.fetchall()

		conexion_usuario.c.execute("SELECT * FROM grupo_equipos_porra")

		assert not conexion_usuario.c.fetchall()

		conexion_usuario.c.execute("SELECT * FROM mejores_terceros_porra")

		assert not conexion_usuario.c.fetchall()

		conexion_usuario.c.execute("SELECT * FROM estado_porra")

		assert not conexion_usuario.c.fetchone()