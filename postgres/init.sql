CREATE TABLE codigos (Codigo_Liga VARCHAR(6) PRIMARY KEY);

CREATE TABLE usuarios (Usuario VARCHAR(255) PRIMARY KEY,
						Correo VARCHAR(255),
						Contrasena VARCHAR(255),
						Nombre VARCHAR(255),
						Apellido VARCHAR(255),
						Codigo_Liga VARCHAR(6),
						Admin BOOl DEFAULT FALSE,
						FOREIGN KEY (Codigo_Liga) REFERENCES codigos (Codigo_Liga) ON DELETE CASCADE);