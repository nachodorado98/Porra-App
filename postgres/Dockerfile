FROM postgres:13

COPY init.sql /docker-entrypoint-initdb.d/

COPY data/mejores_terceros.csv /docker-entrypoint-initdb.d/mejores_terceros.csv

CMD ["postgres"]