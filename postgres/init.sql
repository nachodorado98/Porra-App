CREATE TABLE codigos (Codigo_Liga VARCHAR(6) PRIMARY KEY);

CREATE TABLE usuarios (Usuario VARCHAR(255) PRIMARY KEY,
						Correo VARCHAR(255),
						Contrasena VARCHAR(255),
						Nombre VARCHAR(255),
						Apellido VARCHAR(255),
						Codigo_Liga VARCHAR(6),
						Admin BOOl DEFAULT FALSE,
						FOREIGN KEY (Codigo_Liga) REFERENCES codigos (Codigo_Liga) ON DELETE CASCADE);

CREATE TABLE equipos (Equipo_Id VARCHAR(255) PRIMARY KEY,
						Nombre VARCHAR(255),
						Escudo INTEGER,
						Bandera CHAR(3),
						Grupo CHAR(1),
						Posicion INTEGER);

INSERT INTO equipos VALUES ('seleccion-republica-corea', 'Corea del Sur', 3804, 'KOR', 'A', 1),
							('seleccion-mexico', 'México', 3811, 'MEX', 'A', 2),
							('republica-checa', 'República Checa', 6188, 'CZE', 'A', 3),
							('seleccion-sudafrica', 'Sudáfrica', 3815, 'ZAF', 'A', 4);