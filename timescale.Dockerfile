FROM timescale/timescaledb:latest-pg12
ENV POSTGRES_USER=docker
ENV POSTGRES_PASSWORD=docker
COPY ./setup-file/cpu_usage.sql /docker-entrypoint-initdb.d/003-init.sql
COPY ./setup-file/cpu_usage.csv /cpu_usage.csv
COPY ./setup-file/copy-csv.sql /docker-entrypoint-initdb.d/004-init.sql