FROM postgres:16

COPY init-data.sh /docker-entrypoint-initdb.d/init-data.sh

RUN chmod +x /docker-entrypoint-initdb.d/init-data.sh