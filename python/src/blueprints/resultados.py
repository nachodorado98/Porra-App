from flask import Blueprint, render_template, redirect
from flask_login import login_required, current_user

from src.database.conexion import Conexion

from src.config import URL_DATALAKE_PERFIL

from src.utilidades.utils import obtenerGruposEquiposLimpios, obtenerTercerosGruposEquiposLimpios, obtenerEliminatoriasRealLimpias


bp_resultados=Blueprint("resultados", __name__)

@bp_resultados.route("/resultados")
@login_required
def pagina_resultados():

	usuario=current_user.id

	codigo_liga=current_user.codigo_liga

	imagen_perfil=current_user.imagen_perfil

	paso_porra=current_user.paso_porra

	con=Conexion()

	grupos_resultados_real=con.obtenerGruposReal()

	mejores_terceros_resultados_real=con.obtenerMejoresTercerosReal()

	eliminatorias_resultados_real=con.obtenerEliminatoriasReal()

	con.cerrarConexion()

	grupos_resultados_real_limpios=obtenerGruposEquiposLimpios(grupos_resultados_real)

	mejores_terceros_resultados_real_limpios=obtenerTercerosGruposEquiposLimpios(mejores_terceros_resultados_real)

	eliminatorias_resultados_real_limpias=obtenerEliminatoriasRealLimpias(eliminatorias_resultados_real)

	return render_template("resultados.html",
							usuario=usuario,
							nombre=current_user.nombre,
							codigo_liga=codigo_liga,
							imagen_perfil=imagen_perfil,
							grupos=grupos_resultados_real_limpios,
							mejores_terceros=mejores_terceros_resultados_real_limpios,
							eliminatorias=eliminatorias_resultados_real_limpias,
							paso_porra=paso_porra,
							url_imagen_usuario_perfil=f"{URL_DATALAKE_PERFIL}")