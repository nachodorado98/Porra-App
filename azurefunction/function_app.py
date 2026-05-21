import azure.functions as func
import datetime
import json
import logging

app = func.FunctionApp()

@app.route(route="nachoporrafunc", auth_level=func.AuthLevel.ANONYMOUS)
def nachoporrafunc(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hola, {name}, bienvenido. Esto es una funcion de Azure.")
    else:
        return func.HttpResponse(
             "Introduce el parametro name (name=TU_NOMBRE) para darte la bienvenida.",
             status_code=200
        )