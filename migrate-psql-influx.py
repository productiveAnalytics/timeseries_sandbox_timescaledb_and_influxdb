import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS, ASYNCHRONOUS
import psycopg2
import psycopg2.extras
import time

bucket = "test-bucket"
org = "test"
token = "_6Mb0Td0U5pbKecnJZ0ajSSw3uGJZggVpLmr9WDdAbXsTDImNZI3pO3zj5OgJtoiGXV6-1HGD5E8xi_4GwFw-g=="
# Store the URL of your InfluxDB instance
url="http://127.0.0.1:9999"

client = influxdb_client.InfluxDBClient(
    url=url,
    token=token,
    org=org
)


'''
Generates an collection of influxdb points from the given SQL records
'''
def generate_influx_points(records):
    influx_points = []
    for record in records:
        p=influxdb_client.Point("conditions").tag("device_id", record['device_id']).field("temperature", record['temperature']).field("humidity",record['humidity']).time(record['time'])
        influx_points.append(p)
#        print(str(p))
    return influx_points


conn = psycopg2.connect("dbname=tsdb user=postgres password=root host=127.0.0.1")

# query relational DB for all records
curr = conn.cursor('cursor', cursor_factory=psycopg2.extras.RealDictCursor)
# curr = conn.cursor(dictionary=True)
curr.execute("SELECT * FROM conditions ORDER BY time DESC;")
row_count = 0
# process 100000 records at a time
write_api = client.write_api(write_options=SYNCHRONOUS)
start = time.process_time()
while True:
    print("Processing row #" + str(row_count + 1))
    selected_rows = curr.fetchmany(100000)
    #influxClient.write_points(generate_influx_points(selected_rows))

    rows=generate_influx_points(selected_rows)
    write_api.write(bucket=bucket, org=org, record=rows)
    row_count += 100000
    if len(selected_rows) < 100000:
        break
conn.close()
print("time taken (in sec) : ", time.process_time() - start)


