from flask import Flask
import os

from .blueprints.inicio import bp_inicio
from .blueprints.registro import bp_registro
from .blueprints.login import bp_login
from .blueprints.porra import bp_porra
from .blueprints.clasificacion import bp_clasificacion
from .blueprints.settings import bp_settings
from .blueprints.resultados import bp_resultados

from .extensiones.manager import login_manager

from .utilidades.utils import crearCarpeta

# Funcion para crear la instancia de la aplicacion
def crear_app(configuracion:object)->Flask:

	ruta=os.path.dirname(os.path.join(os.path.dirname(__file__)))

	crearCarpeta(os.path.join(ruta, "src", "static", "imagenes", "perfil"))

	app=Flask(__name__, template_folder="templates")

	app.config.from_object(configuracion)

	login_manager.init_app(app)
	login_manager.login_view="login.login"

	app.register_blueprint(bp_inicio)
	app.register_blueprint(bp_registro)
	app.register_blueprint(bp_login)
	app.register_blueprint(bp_porra)
	app.register_blueprint(bp_clasificacion)
	app.register_blueprint(bp_settings)
	app.register_blueprint(bp_resultados)

	return app