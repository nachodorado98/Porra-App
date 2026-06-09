from flask import Blueprint, render_template, redirect
from flask_login import login_required, current_user

from src.database.conexion import Conexion

from src.config import URL_DATALAKE_PERFIL

from src.utilidades.utils import calcularPuntosTotalesGrupos, compararGruposDisponiblesDataFrameDetalle, calcularPuntosTotalesGrupos


bp_puntuacion=Blueprint("puntuacion", __name__)

@bp_puntuacion.route("/puntuacion/calcular_puntuacion", methods=["PUT"])
@login_required
def pagina_puntuacion_calcular_puntuacion():

	usuario=current_user.id

	codigo_liga=current_user.codigo_liga

	imagen_perfil=current_user.imagen_perfil

	paso_porra=current_user.paso_porra

	try:

		con=Conexion()

		if not current_user.admin:

			con.cerrarConexion()

			return redirect("/porra")

		usuarios_porra_completada=con.obtenerDatosUsuariosPorraCompleta()

		grupos_real=con.obtenerGruposRealPuntuacion()

		for usuario_porra, nombre, correo, codigo_liga in usuarios_porra_completada:

			print(f"Calculando usuario: {usuario_porra}", flush=True)

			grupos_porra=con.obtenerGruposPorraUsuarioPuntuacion(usuario_porra)

			puntos_grupos=calcularPuntosTotalesGrupos(grupos_real, grupos_porra)

			con.actualizarPuntuacionUsuarioSinCommit(usuario_porra, puntos_grupos, 0, 0)

			print(f"{usuario_porra}: {puntos_grupos} puntos", flush=True)

		con.confirmar()

		con.cerrarConexion()

		print("Puntos calculados correctamente", flush=True)

		return redirect("/settings")

	except Exception as e:

		con.cerrarConexion()

		raise e

@bp_puntuacion.route("/puntuacion/detalle/<usuario_porra>")
@login_required
def pagina_puntuacion_detalle_usuario(usuario_porra:str):

	usuario=current_user.id

	codigo_liga=current_user.codigo_liga

	imagen_perfil=current_user.imagen_perfil

	paso_porra=current_user.paso_porra

	con=Conexion()

	if not con.existe_usuario(usuario_porra):

		con.cerrarConexion()

		return redirect("/porra")

	porra_abierta=con.porraAbierta()

	if porra_abierta:

		con.cerrarConexion()

		return redirect("/porra")

	puede_ver_porra=con.puedeVisualizarPorra(usuario_porra)

	if not puede_ver_porra:

		con.cerrarConexion()

		return redirect("/porra")

	grupos_real=con.obtenerGruposRealPuntuacion()

	if not grupos_real:

		con.cerrarConexion()

		return redirect("/porra")

	grupos_porra=con.obtenerGruposPorraUsuarioPuntuacion(usuario_porra)

	con.cerrarConexion()

	df_detalle_grupos=compararGruposDisponiblesDataFrameDetalle(grupos_real, grupos_porra)

	detalle_grupos={}

	for fila in df_detalle_grupos.to_dict("records"):

	    grupo=fila["grupo"]

	    if grupo not in detalle_grupos:

	        detalle_grupos[grupo]={
	            "puntos":0,
	            "filas":[]
	        }

	    detalle_grupos[grupo]["filas"].append(fila)
	    detalle_grupos[grupo]["puntos"]+=fila["puntos"]

	puntos_grupos=calcularPuntosTotalesGrupos(grupos_real, grupos_porra)

	return render_template("detalle_puntuacion.html",
							usuario=usuario,
							nombre=current_user.nombre,
							codigo_liga=codigo_liga,
							imagen_perfil=imagen_perfil,
							usuario_porra=usuario_porra,
							detalle_grupos=detalle_grupos,
							puntos_grupos=puntos_grupos,
							paso_porra=paso_porra,
							url_imagen_usuario_perfil=f"{URL_DATALAKE_PERFIL}")