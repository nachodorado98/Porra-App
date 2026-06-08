import pytest
from datetime import datetime, timedelta

def test_tabla_usuarios_vacia(conexion):

	conexion.c.execute("SELECT * FROM usuarios")

	assert not conexion.c.fetchall()

@pytest.mark.parametrize(["usuario", "correo", "contrasena", "nombre", "apellido", "codigo_liga"],
	[
		("nacho98", "nacho@correo", "1234", "nacho", "dorado", "C4N5VT"),
		("nacho948", "correo", "12vvnvvb34", "naegcho", "dordado", "5BN52O"),
		("nacho", "micorreo@correo.es", "12vvn&fvvb34", "nachitoo", "dordado", "1985M9")
	]
)
def test_insertar_usuario(conexion, usuario, correo, contrasena, nombre, apellido, codigo_liga):

	conexion.insertarCodigoLiga(codigo_liga)

	conexion.insertarUsuario(usuario, correo, contrasena, nombre, apellido, codigo_liga)

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	assert len(usuarios)==1

@pytest.mark.parametrize(["numero_usuarios"],
	[(2,),(22,),(5,),(13,),(25,)]
)
def test_insertar_usuarios(conexion, numero_usuarios):

	conexion.insertarCodigoLiga("C4N5VT")

	for numero in range(numero_usuarios):

		conexion.insertarUsuario(f"nacho{numero}", f"micorreo{numero}@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	conexion.c.execute("SELECT * FROM usuarios")

	usuarios=conexion.c.fetchall()

	assert len(usuarios)==numero_usuarios

def test_existe_usuario_no_existen(conexion):

	assert not conexion.existe_usuario("nacho98")

def test_existe_usuario_existen_no_existente(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	assert not conexion.existe_usuario("nacho99")

def test_existe_usuario_existe(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	assert conexion.existe_usuario("nacho98")

def test_existe_corrreo_no_existen(conexion):

	assert not conexion.existe_correo("micorreo@correo.es")

def test_existe_correo_existen_no_existente(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	assert not conexion.existe_correo("micorreo1@correo.es")

def test_existe_correo_existe(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	assert conexion.existe_correo("micorreo@correo.es")

def test_obtener_contrasena_usuario_no_existe(conexion):

	assert conexion.obtenerContrasenaUsuario("nacho98") is None

def test_obtener_contrasena_usuario_existen(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	assert conexion.obtenerContrasenaUsuario("nacho98")=="1234"

def test_obtener_nombre_usuario_no_existe(conexion):

	assert conexion.obtenerNombre("nacho98") is None

def test_obtener_nombre_usuario_existen(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	assert conexion.obtenerNombre("nacho98")=="nacho"

def test_obtener_admin_usuario_no_existe(conexion):

	assert not conexion.obtenerAdmin("nacho98")

def test_obtener_admin_usuario_no_admin(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	assert not conexion.obtenerAdmin("nacho98")

def test_obtener_admin_usuario_si_admin(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	conexion.c.execute("UPDATE usuarios SET Admin=True")

	conexion.confirmar()

	assert conexion.obtenerAdmin("nacho98")

def test_obtener_codigo_liga_usuario_no_existe(conexion):

	assert conexion.obtenerCodigoLigaUsuario("nacho98") is None

def test_obtener_codigo_liga_usuario_existen(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	assert conexion.obtenerCodigoLigaUsuario("nacho98")=="C4N5VT"

def test_obtener_usuarios_codigo_liga_no_existen(conexion):

	assert not conexion.obtenerUsuariosCodigoLiga("C4N5VT")

def test_obtener_usuarios_codigo_liga_existen_distintos(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	assert not conexion.obtenerUsuariosCodigoLiga("123456")

def test_obtener_usuarios_codigo_liga_existen(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	usuarios=conexion.obtenerUsuariosCodigoLiga("C4N5VT")

	assert len(usuarios)==1

def test_obtener_usuarios_codigo_liga_existentes(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	for numero in range(1, 11):

		conexion.insertarUsuario(f"nacho98{numero}", f"micorreo{numero}@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	usuarios=conexion.obtenerUsuariosCodigoLiga("C4N5VT")

	assert len(usuarios)==10

def test_obtener_puntuaciones_usuarios_codigo_liga_no_existen(conexion):

	assert not conexion.obtenerPuntuacionesUsuariosCodigoLiga("C4N5VT")

def test_obtener_puntuaciones_usuarios_codigo_liga_existen_distintos(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	conexion.insertarPuntuacionUsuario("nacho98")

	assert not conexion.obtenerPuntuacionesUsuariosCodigoLiga("123456")

def test_obtener_puntuaciones_usuarios_codigo_liga_existen(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	conexion.insertarPuntuacionUsuario("nacho98")

	usuarios=conexion.obtenerPuntuacionesUsuariosCodigoLiga("C4N5VT")

	assert len(usuarios)==1

def test_obtener_puntuaciones_usuarios_codigo_liga_existentes(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	for numero in range(1, 11):

		conexion.insertarUsuario(f"nacho98{numero}", f"micorreo{numero}@correo.es", "1234", "nacho", "dorado", "C4N5VT")

		conexion.insertarPuntuacionUsuario(f"nacho98{numero}")

	usuarios=conexion.obtenerPuntuacionesUsuariosCodigoLiga("C4N5VT")

	assert len(usuarios)==10

def test_eliminar_usuario_no_existe_usuario(conexion):

	assert not conexion.existe_usuario("nacho98")

	conexion.eliminarUsuario("nacho98")

	assert not conexion.existe_usuario("nacho98")

def test_eliminar_usuario(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	assert conexion.existe_usuario("nacho98")

	conexion.eliminarUsuario("nacho98")

	assert not conexion.existe_usuario("nacho98")

def test_obtener_imagen_perfil_usuario_no_existe_usuario(conexion):

	assert not conexion.obtenerImagenPerfilUsuario("nacho98")

def test_obtener_imagen_perfil_usuario_no_existe_imagen(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	assert conexion.obtenerImagenPerfilUsuario("nacho98")=='-1'

def test_obtener_imagen_perfil_usuario(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	conexion.c.execute("UPDATE usuarios SET Imagen_Perfil='imagen_perfil.png'")

	conexion.confirmar()

	assert conexion.obtenerImagenPerfilUsuario("nacho98")=='imagen_perfil.png'

def test_actualizar_imagen_perfil_usuario_no_existe_usuario(conexion):

	assert not conexion.existe_usuario("nacho")

	conexion.actualizarImagenPerfilUsuario("nacho", "imagen.png")

	assert not conexion.existe_usuario("nacho")

def test_actualizar_imagen_perfil_usuario(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	conexion.c.execute("SELECT Imagen_Perfil FROM usuarios")

	imagen=conexion.c.fetchone()["imagen_perfil"]

	assert imagen==None

	conexion.actualizarImagenPerfilUsuario("nacho98", "imagen.png")

	conexion.c.execute("SELECT Imagen_Perfil FROM usuarios")

	imagen=conexion.c.fetchone()["imagen_perfil"]

	assert imagen=="imagen.png"

def test_obtener_datos_usuarios_no_existen(conexion):

	assert not conexion.obtenerDatosUsuarios()

@pytest.mark.parametrize(["numero_usuarios"],
	[(2,),(22,),(5,),(13,),(25,),(1,)]
)
def test_obtener_datos_usuarios_existen(conexion, numero_usuarios):

	conexion.insertarCodigoLiga("C4N5VT")

	for numero in range(numero_usuarios):

		conexion.insertarUsuario(f"nacho{numero}", f"micorreo{numero}@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	datos_usuarios=conexion.obtenerDatosUsuarios()

	assert len(datos_usuarios)==numero_usuarios

def test_obtener_datos_usuarios_porra_pendiente_no_existen(conexion):

	assert not conexion.obtenerDatosUsuariosPorraPendiente()

@pytest.mark.parametrize(["numero_usuarios"],
	[(2,),(22,),(5,),(13,),(25,),(1,)]
)
def test_obtener_datos_usuarios_porra_pendiente_porra_pendiente(conexion, numero_usuarios):

	conexion.insertarCodigoLiga("C4N5VT")

	for numero in range(numero_usuarios):

		conexion.insertarUsuario(f"nacho{numero}", f"micorreo{numero}@correo.es", "1234", "nacho", "dorado", "C4N5VT")

		conexion.insertarEstadoPorraUsuario(f"nacho{numero}")

	datos_usuarios=conexion.obtenerDatosUsuariosPorraPendiente()

	assert len(datos_usuarios)==numero_usuarios

@pytest.mark.parametrize(["numero_usuarios"],
	[(2,),(22,),(5,),(13,),(25,),(1,)]
)
def test_obtener_datos_usuarios_porra_pendiente_porra_completa(conexion, numero_usuarios):

	conexion.insertarCodigoLiga("C4N5VT")

	for numero in range(numero_usuarios):

		conexion.insertarUsuario(f"nacho{numero}", f"micorreo{numero}@correo.es", "1234", "nacho", "dorado", "C4N5VT")

		conexion.insertarEstadoPorraUsuario(f"nacho{numero}")

		conexion.actualizarEstadoPorraUsuario(f"nacho{numero}")

	assert not conexion.obtenerDatosUsuariosPorraPendiente()

def test_obtener_datos_usuarios_porra_completa_no_existen(conexion):

	assert not conexion.obtenerDatosUsuariosPorraCompleta()

@pytest.mark.parametrize(["numero_usuarios"],
	[(2,),(22,),(5,),(13,),(25,),(1,)]
)
def test_obtener_datos_usuarios_porra_completa_porra_pendiente(conexion, numero_usuarios):

	conexion.insertarCodigoLiga("C4N5VT")

	for numero in range(numero_usuarios):

		conexion.insertarUsuario(f"nacho{numero}", f"micorreo{numero}@correo.es", "1234", "nacho", "dorado", "C4N5VT")

		conexion.insertarEstadoPorraUsuario(f"nacho{numero}")

	assert not conexion.obtenerDatosUsuariosPorraCompleta()

@pytest.mark.parametrize(["numero_usuarios"],
	[(2,),(22,),(5,),(13,),(25,),(1,)]
)
def test_obtener_datos_usuarios_porra_completa_porra_completa(conexion, numero_usuarios):

	conexion.insertarCodigoLiga("C4N5VT")

	for numero in range(numero_usuarios):

		conexion.insertarUsuario(f"nacho{numero}", f"micorreo{numero}@correo.es", "1234", "nacho", "dorado", "C4N5VT")

		conexion.insertarEstadoPorraUsuario(f"nacho{numero}")

		conexion.actualizarEstadoPorraUsuario(f"nacho{numero}")

	datos_usuarios=conexion.obtenerDatosUsuariosPorraCompleta()

	assert len(datos_usuarios)==numero_usuarios

def test_obtener_datos_cambio_contrasena_usuario_usuario_no_existe(conexion):

	assert not conexion.obtenerDatosCambioContrasenaUsuario("nacho98")

def test_obtener_datos_cambio_contrasena_usuario_sin_cambios(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	datos_cambio_contrasena=conexion.obtenerDatosCambioContrasenaUsuario("nacho98")

	assert datos_cambio_contrasena[0]==0
	assert datos_cambio_contrasena[1]==None

def test_obtener_datos_cambio_contrasena_usuario_con_cambios(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	conexion.c.execute("UPDATE usuarios SET Cambios_Contrasena=1, Ultimo_Cambio_Contrasena='2026-06-22 19:40:36.361302'")

	conexion.confirmar()

	datos_cambio_contrasena=conexion.obtenerDatosCambioContrasenaUsuario("nacho98")

	assert datos_cambio_contrasena[0]==1
	assert datos_cambio_contrasena[1].strftime("%Y-%m-%d")=="2026-06-22"

def test_puede_cambiar_contrasena_no_existe_usuario(conexion):

	assert not conexion.puedeCambiarContrasena("nacho98")

def test_puede_cambiar_contrasena_nunca_cambio(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	assert conexion.puedeCambiarContrasena("nacho98")

def test_puede_cambiar_contrasena_no_existe_usuario(conexion):

	assert not conexion.puedeCambiarContrasena("nacho98")

def test_puede_cambiar_contrasena_nunca_cambio(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	assert conexion.puedeCambiarContrasena("nacho98")

@pytest.mark.parametrize(["cambios", "ultimo_cambio", "puede"],
	[
		(0, datetime.now()-timedelta(hours=23), False),
		(0, datetime.now()-timedelta(hours=48), True),
		(2, datetime.now()-timedelta(hours=48), True),
		(2, datetime.now()-timedelta(hours=24), True),
		(2, datetime.now()-timedelta(hours=12), False),
		(3, datetime.now()-timedelta(days=20), False),
		(4, datetime.now()-timedelta(days=100), False)
	]
)
def test_puede_cambiar_contrasena_varios_casos(conexion, cambios, ultimo_cambio, puede):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	conexion.c.execute(f"UPDATE usuarios SET Cambios_Contrasena={cambios}, Ultimo_Cambio_Contrasena='{ultimo_cambio}'")

	conexion.confirmar()

	assert conexion.puedeCambiarContrasena("nacho98")==puede

def test_actualizar_contrasena_usuario_no_existe_usuario(conexion):

	assert not conexion.existe_usuario("nacho")

	ultimo_cambio=datetime.now()

	conexion.actualizarContrasenaUsuario("nacho", "12345678", 1, ultimo_cambio)

	assert not conexion.existe_usuario("nacho")

def test_actualizar_contrasena_usuario(conexion):

	conexion.insertarCodigoLiga("C4N5VT")

	conexion.insertarUsuario("nacho98", "micorreo@correo.es", "1234", "nacho", "dorado", "C4N5VT")

	ultimo_cambio=datetime.now()

	conexion.actualizarContrasenaUsuario("nacho98", "12345678", 1, ultimo_cambio)

	datos_cambio_contrasena=conexion.obtenerDatosCambioContrasenaUsuario("nacho98")

	assert datos_cambio_contrasena[0]==1
	assert datos_cambio_contrasena[1].strftime("%Y-%m-%d")==ultimo_cambio.strftime("%Y-%m-%d")