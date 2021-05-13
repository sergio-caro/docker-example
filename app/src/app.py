import time
import random
import os
from prometheus_client import start_http_server, Summary

from sqlalchemy import create_engine

db_name = os.getenv('POSTGRES_DB', 'test')
db_user = os.getenv('POSTGRES_USER', 'test')
db_pass = os.getenv('POSTGRES_PASSWORD', 'test')
db_host = os.getenv('POSTGRES_HOST', 'db')
db_port = os.getenv('POSTGRES_HOST_PORT', '5432')

# Connecto to the database
db_string = 'postgresql://{}:{}@{}:{}/{}'.format(db_user, db_pass, db_host, db_port, db_name)
db = create_engine(db_string)

# Create a metric to track time spent and requests made.
REQUEST_TIME = Summary('python_add_new_row_seconds', 'Time spent processing request')

# Decorate function with metric.
@REQUEST_TIME.time()
def add_new_row(n):
    # Insert a new number into the 'numbers' table.
    db.execute("INSERT INTO numbers (number,timestamp) VALUES ("+ 
        str(n) + "," + 
        str(int(round(time.time() * 1000))) + ");")

def get_last_row():
    # Retrieve the last number inserted inside the 'numbers'
    query = "SELECT number FROM numbers WHERE timestamp >= (SELECT max(timestamp) FROM numbers) LIMIT 1"

    result_set = db.execute(query)  
    for (r) in result_set:  
        return r[0]

def get_rows_count():
    query = "SELECT COUNT(*) FROM numbers"
    result_set = db.execute(query)
    for (r) in result_set:
        return r[0]

if __name__ == '__main__':
    print('Application started')

    # Prometheus - Start up the server to expose the metrics.
    start_http_server(8000)

    while True:
        add_new_row(random.randint(1,100000))
        print('Insertado un nuevo valor: {}'.format(get_last_row()))
        print('----> Hay {} registros'.format(get_rows_count()))
        time.sleep(5)
