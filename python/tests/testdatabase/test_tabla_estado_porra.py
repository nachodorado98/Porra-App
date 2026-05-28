def test_tabla_estado_porra_vacia(conexion):

	conexion.c.execute("SELECT * FROM estado_porra")

	assert not conexion.c.fetchall()

def test_insertar_estado_porra(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	conexion.insertarEstadoPorraUsuario("nacho98")

	conexion.c.execute("SELECT * FROM estado_porra")

	estado_porras=conexion.c.fetchall()

	assert len(estado_porras)==1

def test_obtener_estado_porra_usuario_no_existe_usuario(conexion):

	assert not conexion.obtenerEstadoPorraUsuario("nacho98")

def test_obtener_estado_porra_usuario_otro_usuario(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	conexion.insertarEstadoPorraUsuario("nacho98")

	assert not conexion.obtenerEstadoPorraUsuario("nacho")

def test_obtener_estado_porra_usuario(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	conexion.insertarEstadoPorraUsuario("nacho98")

	estado_porra_usuario=conexion.obtenerEstadoPorraUsuario("nacho98")

	assert len(estado_porra_usuario)==2

def test_actualizar_estado_porra_grupos_no_existe_usuario(conexion):

	conexion.c.execute("SELECT * FROM estado_porra")

	assert not conexion.c.fetchall()

	conexion.actualizarEstadoPorraGruposUsuario("nacho98")

	conexion.c.execute("SELECT * FROM estado_porra WHERE usuario='nacho98'")

	assert not conexion.c.fetchall()

def test_actualizar_estado_porra_grupos_otro_usuario(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	conexion.insertarEstadoPorraUsuario("nacho98")

	conexion.c.execute("SELECT Grupos_Completados FROM estado_porra WHERE usuario='nacho98'")

	assert not conexion.c.fetchone()["grupos_completados"]

	conexion.actualizarEstadoPorraGruposUsuario("nacho")

	conexion.c.execute("SELECT Grupos_Completados FROM estado_porra WHERE usuario='nacho98'")

	assert not conexion.c.fetchone()["grupos_completados"]

def test_actualizar_estado_porra_grupos(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	conexion.insertarEstadoPorraUsuario("nacho98")

	conexion.c.execute("SELECT Grupos_Completados FROM estado_porra WHERE usuario='nacho98'")

	assert not conexion.c.fetchone()["grupos_completados"]

	conexion.actualizarEstadoPorraGruposUsuario("nacho98")

	conexion.c.execute("SELECT Grupos_Completados FROM estado_porra WHERE usuario='nacho98'")

	assert conexion.c.fetchone()["grupos_completados"]

def test_grupos_porra_completa_no_existe_usuario(conexion):

	assert not conexion.gruposPorraCompleto("nacho98")

def test_grupos_porra_completa_no_grupo_completado(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	conexion.insertarEstadoPorraUsuario("nacho98")

	assert not conexion.gruposPorraCompleto("nacho98")

def test_grupos_porra_completa_grupo_completado(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	conexion.insertarEstadoPorraUsuario("nacho98")

	conexion.actualizarEstadoPorraGruposUsuario("nacho98")

	assert conexion.gruposPorraCompleto("nacho98")

def test_puede_editar_grupos_porra_no_existe_usuario(conexion):

	assert conexion.puedeEditarGruposPorra("nacho98")

def test_puede_editar_grupos_porra_no_grupo_completado(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	conexion.insertarEstadoPorraUsuario("nacho98")

	assert conexion.puedeEditarGruposPorra("nacho98")

def test_puede_editar_grupos_porra_grupo_completado(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	conexion.insertarEstadoPorraUsuario("nacho98")

	conexion.actualizarEstadoPorraGruposUsuario("nacho98")

	assert not conexion.puedeEditarGruposPorra("nacho98")

def test_actualizar_estado_porra_mejores_terceros_no_existe_usuario(conexion):

	conexion.c.execute("SELECT * FROM estado_porra")

	assert not conexion.c.fetchall()

	conexion.actualizarEstadoPorraMejoresTercerosUsuario("nacho98")

	conexion.c.execute("SELECT * FROM estado_porra WHERE usuario='nacho98'")

	assert not conexion.c.fetchall()

def test_actualizar_estado_porra_mejores_terceros_otro_usuario(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	conexion.insertarEstadoPorraUsuario("nacho98")

	conexion.c.execute("SELECT Mejores_Terceros_Completados FROM estado_porra WHERE usuario='nacho98'")

	assert not conexion.c.fetchone()["mejores_terceros_completados"]

	conexion.actualizarEstadoPorraMejoresTercerosUsuario("nacho")

	conexion.c.execute("SELECT Mejores_Terceros_Completados FROM estado_porra WHERE usuario='nacho98'")

	assert not conexion.c.fetchone()["mejores_terceros_completados"]

def test_actualizar_estado_porra_mejores_terceros(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	conexion.insertarEstadoPorraUsuario("nacho98")

	conexion.c.execute("SELECT Mejores_Terceros_Completados FROM estado_porra WHERE usuario='nacho98'")

	assert not conexion.c.fetchone()["mejores_terceros_completados"]

	conexion.actualizarEstadoPorraMejoresTercerosUsuario("nacho98")

	conexion.c.execute("SELECT Mejores_Terceros_Completados FROM estado_porra WHERE usuario='nacho98'")

	assert conexion.c.fetchone()["mejores_terceros_completados"]

def test_mejores_terceros_porra_completa_no_existe_usuario(conexion):

	assert not conexion.mejoresTercerosPorraCompleto("nacho98")

def test_mejores_terceros_porra_completa_no_grupo_completado(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	conexion.insertarEstadoPorraUsuario("nacho98")

	assert not conexion.mejoresTercerosPorraCompleto("nacho98")

def test_mejores_terceros_porra_completa_grupo_completado(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	conexion.insertarEstadoPorraUsuario("nacho98")

	conexion.actualizarEstadoPorraMejoresTercerosUsuario("nacho98")

	assert conexion.mejoresTercerosPorraCompleto("nacho98")

def test_puede_editar_mejores_terceros_porra_no_existe_usuario(conexion):

	assert conexion.puedeEditarMejoresTercerosPorra("nacho98")

def test_puede_editar_mejores_terceros_porra_no_grupo_completado(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	conexion.insertarEstadoPorraUsuario("nacho98")

	assert conexion.puedeEditarMejoresTercerosPorra("nacho98")

def test_puede_editar_mejores_terceros_porra_grupo_completado(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	conexion.insertarEstadoPorraUsuario("nacho98")

	conexion.actualizarEstadoPorraMejoresTercerosUsuario("nacho98")

	assert not conexion.puedeEditarMejoresTercerosPorra("nacho98")

def test_reiniciar_estado_porra_usuario_usuario_no_existe(conexion):

	conexion.c.execute("SELECT * FROM estado_porra")

	assert not conexion.c.fetchone()

	conexion.reiniciarEstadoPorraUsuario("nacho98")

	conexion.c.execute("SELECT * FROM estado_porra")

	assert not conexion.c.fetchone()

def test_reiniciar_estado_porra_usuario_otro_usuario(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	conexion.insertarEstadoPorraUsuario("nacho98")

	conexion.actualizarEstadoPorraGruposUsuario("nacho98")

	conexion.actualizarEstadoPorraMejoresTercerosUsuario("nacho98")

	conexion.c.execute("SELECT grupos_completados, mejores_terceros_completados FROM estado_porra")

	estado=conexion.c.fetchone()

	assert estado["grupos_completados"]
	assert estado["mejores_terceros_completados"]

	conexion.reiniciarEstadoPorraUsuario("nacho")

	conexion.c.execute("SELECT grupos_completados, mejores_terceros_completados FROM estado_porra")

	estado=conexion.c.fetchone()

	assert estado["grupos_completados"]
	assert estado["mejores_terceros_completados"]

def test_reiniciar_estado_porra_usuario(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	conexion.insertarEstadoPorraUsuario("nacho98")

	conexion.actualizarEstadoPorraGruposUsuario("nacho98")

	conexion.actualizarEstadoPorraMejoresTercerosUsuario("nacho98")

	conexion.c.execute("SELECT grupos_completados, mejores_terceros_completados FROM estado_porra")

	estado=conexion.c.fetchone()

	assert estado["grupos_completados"]
	assert estado["mejores_terceros_completados"]

	conexion.reiniciarEstadoPorraUsuario("nacho98")

	conexion.c.execute("SELECT grupos_completados, mejores_terceros_completados FROM estado_porra")

	estado=conexion.c.fetchone()

	assert not estado["grupos_completados"]
	assert not estado["mejores_terceros_completados"]