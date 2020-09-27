FROM timescale/timescaledb:latest-pg12
ENV POSTGRES_USER=docker
ENV POSTGRES_PASSWORD=docker
COPY cpu_usage.sql /docker-entrypoint-initdb.d/003-init.sql
COPY cpu_usage.csv /cpu_usage.csv
COPY copy-csv.sql /docker-entrypoint-initdb.d/004-init.sql