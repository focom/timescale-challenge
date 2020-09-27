\c homework
COPY cpu_usage(ts, host, usage)
FROM '/cpu_usage.csv'
DELIMITER ','
CSV HEADER;