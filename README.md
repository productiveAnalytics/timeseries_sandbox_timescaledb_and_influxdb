# timeseries_sandbox_timescaledb_and_influxdb
Sandbox for time series data

docker network create timeseries_network

1. Run timescaledb as docker container
```docker run -d --name timescaledb_pg14 -p127.0.0.1:5432:5432 -e POSTGRES_PASSWORD=postgres_local timescale/timescaledb:latest-pg14```
