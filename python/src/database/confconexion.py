import os

USUARIO=os.getenv("POSTGRES_USER", "app_user")
CONTRASENA=os.getenv("POSTGRES_PASSWORD", "supersecret")
DATABASE=os.getenv("POSTGRES_DB", "bbdd_porra")
HOST=os.getenv("POSTGRES_HOST", "bbdd")
PUERTO=os.getenv("POSTGRES_PORT", 5432)