import pytest

def test_conexion(conexion):

	conexion.c.execute("SELECT current_database();")

	assert conexion.c.fetchone()["current_database"]=="bbdd_porra"

	conexion.c.execute("select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';")

	tablas=[tabla["relname"] for tabla in conexion.c.fetchall()]

	assert "usuarios" in tablas 
	assert "codigos" in tablas
	assert "estado_porra" in tablas
	assert "puntuaciones" in tablas
	assert "equipos" in tablas
	assert "grupos" in tablas
	assert "grupo_equipos" in tablas
	assert "grupo_equipos_real" in tablas
	assert "grupo_equipos_porra" in tablas
	assert "mejores_terceros_porra" in tablas
	assert "mejores_terceros_real" in tablas
	assert "lookup_bracket_mejores_terceros" in tablas
	assert "eliminatorias_porra" in tablas
	assert "eliminatorias_real" in tablas
	assert "maestro" in tablas
		
def test_cerrar_conexion(conexion):

	assert not conexion.bbdd.closed

	conexion.cerrarConexion()

	assert conexion.bbdd.closed

def test_vaciar_bbdd(conexion_usuario):

	tablas=["codigos", "usuarios", "estado_porra"]

	for tabla in tablas:

		conexion_usuario.c.execute(f"SELECT * FROM {tabla}")

		assert conexion_usuario.c.fetchall()

	conexion_usuario.vaciarBBDD()

	for tabla in tablas:

		conexion_usuario.c.execute(f"SELECT * FROM {tabla}")

		assert not conexion_usuario.c.fetchall()