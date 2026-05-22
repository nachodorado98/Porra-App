import pytest

def test_conexion(conexion):

	conexion.c.execute("SELECT current_database();")

	assert conexion.c.fetchone()["current_database"]=="bbdd_porra"

	conexion.c.execute("select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';")

	tablas=[tabla["relname"] for tabla in conexion.c.fetchall()]

	assert "usuarios" in tablas 
	assert "codigos" in tablas
	assert "equipos" in tablas
	
def test_cerrar_conexion(conexion):

	assert not conexion.bbdd.closed

	conexion.cerrarConexion()

	assert conexion.bbdd.closed

def test_vaciar_bbdd(conexion_usuario):

	tablas=["codigos", "usuarios"]

	for tabla in tablas:

		conexion_usuario.c.execute(f"SELECT * FROM {tabla}")

		assert conexion_usuario.c.fetchall()

	conexion_usuario.vaciarBBDD()

	for tabla in tablas:

		conexion_usuario.c.execute(f"SELECT * FROM {tabla}")

		assert not conexion_usuario.c.fetchall()