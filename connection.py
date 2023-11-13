
from dotenv import dotenv_values
from psycopg2 import pool

secrets = dotenv_values(".env")

class ConnectionPool:
    def __init__(self):
        self.connection_pool = pool.SimpleConnectionPool(
            1,  # minconn
            10,  # maxconn
            host=secrets["DB_HOST"],
            database=secrets["DB_NAME"],
            user=secrets["DB_USER"],
            password=secrets["DB_PASSWORD"]
        )

    def get_connection(self) -> pool.SimpleConnectionPool:
        return self.connection_pool.getconn()

    def return_connection(self, connection):
        self.connection_pool.putconn(connection)

    def close_all_connections(self):
        self.connection_pool.closeall()
