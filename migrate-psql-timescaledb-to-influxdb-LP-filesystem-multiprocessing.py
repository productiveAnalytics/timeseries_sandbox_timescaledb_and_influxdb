import multiprocessing as mp
import time
import psycopg2
import psycopg2.extras
import influxdb_client

arr = []
a_file = open("/tmp/test.txt", "w")

'''
break down query in multiple segments to fetch records from the table so that
each query run by a separate thread on a different processor.
'''

query_load = [("select * FROM conditions ORDER BY time DESC limit 300000;"),
("select * FROM conditions ORDER BY time DESC limit 300000 offset 300000;"),
("select * FROM conditions ORDER BY time DESC limit 400000 offset 600000;")]

def generate_influx_points(records):
    influx_points = []
    for record in records:
        p=influxdb_client.Point("conditions").tag("device_id", record['device_id']).field("temperature", record['temperature']).field("humidity",record['humidity']).time(record['time'])
        #queue.put(p)
        influx_points.append(p)
    return influx_points
# running each query in a new session
def read_sql(query):
    conn = psycopg2.connect("dbname=tsdb user=postgres password=root host=127.0.0.1")
    print(query)
    curr = conn.cursor('cursor', cursor_factory=psycopg2.extras.RealDictCursor)
    curr.execute(query)
    selected_rows = curr.fetchall()
    points=generate_influx_points(selected_rows)
    #print(queue.qsize())
    conn.close()
    return points
    
if __name__ == '__main__':
    start = time.process_time()   
    pool = mp.Pool(mp.cpu_count())

    jobs=[]
    for query in query_load:
        job=pool.apply_async(read_sql, (query,))
        jobs.append(job)

    for job in jobs:
        arr.append(job.get())  

# writing all data into file in a single shot   
    s='\n'.join('\n'.join(map(str, l)) for l in arr)
    a_file.write(s)
    print("time taken (in sec) : ", time.process_time() - start)
