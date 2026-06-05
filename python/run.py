import os
from src import crear_app
from confmain import config

entorno=os.getenv("ENTORNO", "DEV")

configuracion=config[entorno]

print(f"ENTORNO: {configuracion.ENVIROMENT}")
print(f"DEBUG: {configuracion.DEBUG}")
print(f"CONTENEDOR DATALAKE: {configuracion.CONTAINER_DL}")

app=crear_app(configuracion)

if __name__=="__main__":

	app.run()