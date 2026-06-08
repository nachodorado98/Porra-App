from flask import Blueprint, render_template, redirect
from flask_login import login_required, current_user

from src.database.conexion import Conexion

from src.config import URL_DATALAKE_PERFIL

from src.utilidades.utils import calcularPuntosTotalesGrupos


bp_puntuacion=Blueprint("puntuacion", __name__)

@bp_puntuacion.route("/calcular_puntuacion", methods=["PUT"])
@login_required
def pagina_calcular_puntuaciones():

	usuario=current_user.id

	codigo_liga=current_user.codigo_liga

	imagen_perfil=current_user.imagen_perfil

	paso_porra=current_user.paso_porra

	con=Conexion()

	if not current_user.admin:

		con.cerrarConexion()

		return redirect("/porra")

	usuarios_porra_completada=con.obtenerDatosUsuariosPorraCompleta()

	grupos_real=con.obtenerGruposRealPuntuacion()

	for usuario, nombre, correo, codigo_liga in usuarios_porra_completada:

		grupos_porra=con.obtenerGruposPorraUsuarioPuntuacion(usuario)

		puntos_grupos=calcularPuntosTotalesGrupos(grupos_real, grupos_porra)

		con.actualizarPuntuacionUsuario(usuario, puntos_grupos, 0, 0)

	con.cerrarConexion()

	return redirect("/settings")