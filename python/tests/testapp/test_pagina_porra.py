import pytest
from datetime import datetime, timedelta

def test_pagina_porra_sin_login(cliente, conexion):

	respuesta=cliente.get("/porra", follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert "<h1>Iniciar Sesión</h1>" in contenido

@pytest.mark.parametrize(["dias"],
	[(2,),(22,),(5,),(13,),(25,),(1,),(0,)]
)
def test_pagina_porra_porra_cerrada_porra_no_realizada(cliente, conexion_usuario, dias):

	fecha_anterior=(datetime.now()-timedelta(days=dias)).strftime("%Y-%m-%d")

	conexion_usuario.insertarClaveValorMaestro("fecha_cierre_porra", fecha_anterior)

	respuesta=cliente.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert '<main class="main-content">' in contenido
	assert "<h1>Tu porra del Mundial</h1>" in contenido
	assert '<p class="descripcion-pregunta">Ordena las selecciones de cada grupo según cómo crees que terminará la fase inicial.</p>' not in contenido
	assert '<p class="descripcion-pregunta secundaria">Después podrás elegir los mejores terceros y completar todo el cuadro eliminatorio hasta la final.</p>' not in contenido
	assert '<a href="/porra/grupos" class="btn-empezar" data-loading="true">Empezar porra →</a>' not in contenido
	assert '<a href="/porra/reiniciar" class="btn-reiniciar" data-loading="true">Reiniciar porra ⟳</a>' not in contenido
	assert '<p class="descripcion-pregunta">¡Gracias por completar la porra del Mundial!</p>' not in contenido
	assert '<p class="descripcion-pregunta secundaria">Puedes rehacer la porra definitiva hasta el dia previo al comienzo del evento (10/06/2026).</p>' not in contenido
	assert '<a href="/porra/mi_porra" class="btn-empezar" data-loading="true">Ver mi porra</a>' not in contenido
	assert '<a href="/porra/reiniciar" class="btn-reiniciar" data-loading="true">Rehacer porra desde el inicio ⟳</a>' not in contenido
	assert '<li><a href="/porra/mi_porra">Mi Porra</a></li>'not in contenido
	assert '<p class="descripcion-pregunta">La porra esta actualmente cerrada y no se permite crear ni modificar ninguna porra existente.</p>' in contenido

@pytest.mark.parametrize(["dias"],
	[(2,),(22,),(5,),(13,),(25,),(1,),(0,)]
)
def test_pagina_porra_porra_cerrada_porra_realizada(cliente, conexion_usuario, dias):

	fecha_anterior=(datetime.now()-timedelta(days=dias)).strftime("%Y-%m-%d")

	conexion_usuario.insertarClaveValorMaestro("fecha_cierre_porra", fecha_anterior)

	conexion_usuario.actualizarEstadoPorraGruposUsuario("nacho98")

	conexion_usuario.actualizarEstadoPorraMejoresTercerosUsuario("nacho98")

	conexion_usuario.actualizarEstadoPorraEliminatoriasUsuario("nacho98")

	conexion_usuario.actualizarEstadoPorraUsuario("nacho98")

	respuesta=cliente.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert '<main class="main-content">' in contenido
	assert "<h1>Tu porra del Mundial</h1>" in contenido
	assert '<p class="descripcion-pregunta">Ordena las selecciones de cada grupo según cómo crees que terminará la fase inicial.</p>' not in contenido
	assert '<p class="descripcion-pregunta secundaria">Después podrás elegir los mejores terceros y completar todo el cuadro eliminatorio hasta la final.</p>' not in contenido
	assert '<a href="/porra/grupos" class="btn-empezar" data-loading="true">Empezar porra →</a>' not in contenido
	assert '<a href="/porra/reiniciar" class="btn-reiniciar" data-loading="true">Reiniciar porra ⟳</a>' not in contenido
	assert '<p class="descripcion-pregunta">¡Gracias por completar la porra del Mundial!</p>' not in contenido
	assert '<p class="descripcion-pregunta secundaria">Puedes rehacer la porra definitiva hasta el dia previo al comienzo del evento (10/06/2026).</p>' not in contenido
	assert '<a href="/porra/mi_porra" class="btn-empezar" data-loading="true">Ver mi porra</a>' in contenido
	assert '<a href="/porra/reiniciar" class="btn-reiniciar" data-loading="true">Rehacer porra desde el inicio ⟳</a>' not in contenido
	assert '<li><a href="/porra/mi_porra">Mi Porra</a></li>' in contenido
	assert '<p class="descripcion-pregunta">La porra esta actualmente cerrada y no se permite crear ni modificar ninguna porra existente.</p>' in contenido

@pytest.mark.parametrize(["dias"],
	[(2,),(22,),(5,),(13,),(25,),(1,)]
)
def test_pagina_porra_porra_abierta(cliente, conexion_usuario, dias):

	fecha_posterior=(datetime.now()+timedelta(days=dias)).strftime("%Y-%m-%d")

	conexion_usuario.insertarClaveValorMaestro("fecha_cierre_porra", fecha_posterior)

	respuesta=cliente.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert '<main class="main-content">' in contenido
	assert "<h1>Tu porra del Mundial</h1>" in contenido
	assert '<p class="descripcion-pregunta">Ordena las selecciones de cada grupo según cómo crees que terminará la fase inicial.</p>' in contenido
	assert '<p class="descripcion-pregunta secundaria">Después podrás elegir los mejores terceros y completar todo el cuadro eliminatorio hasta la final.</p>' in contenido
	assert '<a href="/porra/grupos" class="btn-empezar" data-loading="true">Empezar porra →</a>' in contenido
	assert '<a href="/porra/reiniciar" class="btn-reiniciar" data-loading="true">Reiniciar porra ⟳</a>' not in contenido
	assert '<p class="descripcion-pregunta">¡Gracias por completar la porra del Mundial!</p>' not in contenido
	assert '<p class="descripcion-pregunta secundaria">Puedes rehacer la porra definitiva hasta el dia previo al comienzo del evento (10/06/2026).</p>' not in contenido
	assert '<a href="/porra/mi_porra" class="btn-empezar" data-loading="true">Ver mi porra</a>' not in contenido
	assert '<a href="/porra/reiniciar" class="btn-reiniciar" data-loading="true">Rehacer porra desde el inicio ⟳</a>' not in contenido
	assert '<li><a href="/porra/mi_porra">Mi Porra</a></li>' not in contenido
	assert '<p class="descripcion-pregunta">La porra esta actualmente cerrada y no se permite crear ni modificar ninguna porra existente.</p>' not in contenido

def test_pagina_porra(cliente, conexion_usuario):

	respuesta=cliente.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert '<main class="main-content">' in contenido
	assert "<h1>Tu porra del Mundial</h1>" in contenido
	assert '<p class="descripcion-pregunta">Ordena las selecciones de cada grupo según cómo crees que terminará la fase inicial.</p>' in contenido
	assert '<p class="descripcion-pregunta secundaria">Después podrás elegir los mejores terceros y completar todo el cuadro eliminatorio hasta la final.</p>' in contenido
	assert '<a href="/porra/grupos" class="btn-empezar" data-loading="true">Empezar porra →</a>' in contenido
	assert '<a href="/porra/reiniciar" class="btn-reiniciar" data-loading="true">Reiniciar porra ⟳</a>' not in contenido
	assert '<p class="descripcion-pregunta">¡Gracias por completar la porra del Mundial!</p>' not in contenido
	assert '<p class="descripcion-pregunta secundaria">Puedes rehacer la porra definitiva hasta el dia previo al comienzo del evento (10/06/2026).</p>' not in contenido
	assert '<a href="/porra/mi_porra" class="btn-empezar" data-loading="true">Ver mi porra</a>' not in contenido
	assert '<a href="/porra/reiniciar" class="btn-reiniciar" data-loading="true">Rehacer porra desde el inicio ⟳</a>' not in contenido
	assert '<li><a href="/porra/mi_porra">Mi Porra</a></li>' not in contenido

def test_pagina_porra_grupos_completos(cliente, conexion_usuario):

	conexion_usuario.actualizarEstadoPorraGruposUsuario("nacho98")

	respuesta=cliente.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert '<main class="main-content">' in contenido
	assert "<h1>Tu porra del Mundial</h1>" in contenido
	assert '<p class="descripcion-pregunta">Ordena las selecciones de cada grupo según cómo crees que terminará la fase inicial.</p>' in contenido
	assert '<p class="descripcion-pregunta secundaria">Después podrás elegir los mejores terceros y completar todo el cuadro eliminatorio hasta la final.</p>' in contenido
	assert '<a href="/porra/mejores_terceros" class="btn-empezar" data-loading="true">Continuar porra →</a>' in contenido
	assert '<a href="/porra/reiniciar" class="btn-reiniciar" data-loading="true">Reiniciar porra ⟳</a>' in contenido
	assert '<p class="descripcion-pregunta">¡Gracias por completar la porra del Mundial!</p>' not in contenido
	assert '<p class="descripcion-pregunta secundaria">Puedes rehacer la porra definitiva hasta el dia previo al comienzo del evento (10/06/2026).</p>' not in contenido
	assert '<a href="/porra/reiniciar" class="btn-reiniciar" data-loading="true">Rehacer porra desde el inicio ⟳</a>' not in contenido
	assert '<li><a href="/porra/mi_porra">Mi Porra</a></li>' not in contenido

def test_pagina_porra_mejores_terceros_completos(cliente, conexion_usuario):

	conexion_usuario.actualizarEstadoPorraGruposUsuario("nacho98")

	conexion_usuario.actualizarEstadoPorraMejoresTercerosUsuario("nacho98")

	respuesta=cliente.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert '<main class="main-content">' in contenido
	assert "<h1>Tu porra del Mundial</h1>" in contenido
	assert '<p class="descripcion-pregunta">Ordena las selecciones de cada grupo según cómo crees que terminará la fase inicial.</p>' in contenido
	assert '<p class="descripcion-pregunta secundaria">Después podrás elegir los mejores terceros y completar todo el cuadro eliminatorio hasta la final.</p>' in contenido
	assert '<a href="/porra/eliminatorias" class="btn-empezar" data-loading="true">Continuar porra →</a>' in contenido
	assert '<a href="/porra/reiniciar" class="btn-reiniciar" data-loading="true">Reiniciar porra ⟳</a>' in contenido
	assert '<p class="descripcion-pregunta">¡Gracias por completar la porra del Mundial!</p>' not in contenido
	assert '<p class="descripcion-pregunta secundaria">Puedes rehacer la porra definitiva hasta el dia previo al comienzo del evento (10/06/2026).</p>' not in contenido
	assert '<a href="/porra/mi_porra" class="btn-empezar" data-loading="true">Ver mi porra</a>' not in contenido
	assert '<a href="/porra/reiniciar" class="btn-reiniciar" data-loading="true">Rehacer porra desde el inicio ⟳</a>' not in contenido
	assert '<li><a href="/porra/mi_porra">Mi Porra</a></li>' not in contenido

def test_pagina_porra_eliminatorias_completas(cliente, conexion_usuario):

	conexion_usuario.actualizarEstadoPorraGruposUsuario("nacho98")

	conexion_usuario.actualizarEstadoPorraMejoresTercerosUsuario("nacho98")

	conexion_usuario.actualizarEstadoPorraEliminatoriasUsuario("nacho98")

	conexion_usuario.actualizarEstadoPorraUsuario("nacho98")

	respuesta=cliente.post("/login", data={"usuario": "nacho98", "contrasena": "Ab!CdEfGhIJK3LMN"}, follow_redirects=True)

	contenido=respuesta.data.decode()

	assert respuesta.status_code==200
	assert '<main class="main-content">' in contenido
	assert "<h1>Tu porra del Mundial</h1>" in contenido
	assert '<p class="descripcion-pregunta">Ordena las selecciones de cada grupo según cómo crees que terminará la fase inicial.</p>' not in contenido
	assert '<p class="descripcion-pregunta secundaria">Después podrás elegir los mejores terceros y completar todo el cuadro eliminatorio hasta la final.</p>' not in contenido
	assert '<a href="/porra/eliminatorias" class="btn-empezar" data-loading="true">Continuar porra →</a>' not in contenido
	assert '<a href="/porra/reiniciar" class="btn-reiniciar" data-loading="true">Reiniciar porra ⟳</a>' not in contenido
	assert '<p class="descripcion-pregunta">¡Gracias por completar la porra del Mundial!</p>' in contenido
	assert '<p class="descripcion-pregunta secundaria">Puedes rehacer la porra definitiva hasta el dia previo al comienzo del evento (10/06/2026).</p>' in contenido
	assert '<a href="/porra/mi_porra" class="btn-empezar" data-loading="true">Ver mi porra</a>' in contenido
	assert '<a href="/porra/reiniciar" class="btn-reiniciar" data-loading="true">Rehacer porra desde el inicio ⟳</a>' in contenido
	assert '<li><a href="/porra/mi_porra">Mi Porra</a></li>' in contenido