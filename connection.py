
import os
from psycopg2 import pool

class ConnectionPool:
    def __init__(self):
        self.connection_pool = pool.SimpleConnectionPool(
            1,  # minconn
            10,  # maxconn
            host=os.environ["DB_HOST"],
            database=os.environ["DB_NAME"],
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"]
        )

    def get_connection(self) -> pool.SimpleConnectionPool:
        return self.connection_pool.getconn()

    def return_connection(self, connection):
        self.connection_pool.putconn(connection)

    def close_all_connections(self):
        self.connection_pool.closeall()
