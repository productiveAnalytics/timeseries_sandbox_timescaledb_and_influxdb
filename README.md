# timeseries_sandbox_timescaledb_and_influxdb
Sandbox for time series data

Create Python 3 virtual environment
1. python3 -m pip install --upgrade pip
2. python3 -m pip install --upgrade virtualenv
3. python3 -m virtualenv .venv
4. source .venv/bin/activate
5. python3 -m pip install -r ./requirements.txt


## Run Portainer (http://localhost:9000)
```
docker run -d -p 8000:8000 -p 9000:9000 --name=portainer --restart=always -v /var/run/docker.sock:/var/run/docker.sock  portainer/portainer-ce
```

## Create Docker Network
```
docker network create --driver bridge timeseries_bridge_network
```

Confirm the network and network interace
```
docker network ls
docker network inspect timeseries_bridge_network
Check the network interface for the docker-network id from "docker network ps": ```ip a | grep <id-of-the-bridge-network>
```

## Confirm no PostgreSQL running on local port: 5432
```
systemctl status postgresql
```

If Postgres is running, stop and disable:
```
systemctl stop postgresql
systemctl disable postgresql
```

## Run timescaleDB in local docker
1. Run timescaledb as docker container
```docker run -d --rm --net timeseries_bridge_network --name timescaledb_pg14 -p 0.0.0.0:5432:5432 -e POSTGRES_PASSWORD=postgres_local timescale/timescaledb:latest-pg14```
Or to use local data directory, use with volume: 
```
docker run -d --net timeseries_bridge_network --name timescaledb_pg14 -p 0.0.0.0:5432:5432 -v /Dev/docker_volumes/timescaledb_pg14/data:/home/postgres/pgdata/data -e POSTGRES_PASSWORD=postgres_local timescale/timescaledb:latest-pg14
```
2. Confirm that the timescaleDB server can be connected using name resolution
```docker run --rm --net timeseries_bridge_network alpine ping timescaledb_pg14```


## Load sample data into timescaleDB (Refer: https://docs.timescale.com/getting-started/latest/add-data/)
1. Download sample data and unzip: ```unzip data/real_time_stock_data.zip```
2. Copy ticks data file to Docker: ```docker cp test_data/tutorial_sample_tick.csv timescaledb_pg14:/tutorial_sample_tick.csv```
3. Copy company data file to Docker: ```docker cp test_data/tutorial_sample_company.csv timescaledb_pg14:/tutorial_sample_company.csv```
4. Confirm the files in Docker: ```docker exec -it timescaledb_pg14 ls -larth```
5. Connect to timescaledb's Postgres server
```docker exec -it timescaledb_pg14 psql -U postgres```
Confirm that the tables exist (or run DDL: timescaledb_hypertable_DDL.sql thru DBeaver)
On psql prompt, list tables: ```\dt```
6. Copy data into tables
```
\COPY stocks_real_time from './tutorial_sample_tick.csv' DELIMITER ',' CSV HEADER;
\COPY company from './tutorial_sample_company.csv' DELIMITER ',' CSV HEADER;
```
7. Confirm the tables get loaded using 
```SELECT count(*) from <table-name>```

## Run InfluxDB docker
```
docker run -d \
 --name=influxdb \
 --hostname=influxdb \
 --ulimit nofile=32768:32768 \
 -p 8086:8086 \
 -v ~/Dev/docker_volumes/influxdb_v2/data:/var/lib/influxdb2 \
 -v ~/Dev/docker_volumes/influxdb_v2/config:/etc/influxdb2 \
 -v /etc/localtime:/etc/localtime:ro \
 -e TZ=America/New_York \
 -e DOCKER_INFLUXDB_INIT_MODE=setup \
 -e DOCKER_INFLUXDB_INIT_USERNAME=db_admin \
 -e DOCKER_INFLUXDB_INIT_PASSWORD=db_password \
 -e DOCKER_INFLUXDB_INIT_ORG=ProductiveAnalytics \
 -e DOCKER_INFLUXDB_INIT_BUCKET=my_bucket \
 --restart unless-stopped \
 influxdb:latest
```

Using local DB credentials, open http://localhost:8086 

For programmatic access using bucket token, use:
```docker exec influxdb influx auth list | awk -v username=db_admin '$5 ~ username {print $4 " "}'```
