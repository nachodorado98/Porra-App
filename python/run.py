from src import crear_app
from confmain import config

configuracion=config["DEV"]

app=crear_app(configuracion)

if __name__=="__main__":

	app.run()