from flask_login import UserMixin
from connection import ConnectionPool

# Definición de la clase User
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    @staticmethod
    def create(username, password):
        connection_pool = ConnectionPool()
        conn = connection_pool.get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        cur.close()
        connection_pool.return_connection(conn)

    @staticmethod
    def read(id):
        connection_pool = ConnectionPool()
        conn = connection_pool.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE id = %s", (id,))
        row = cur.fetchone()
        cur.close()
        connection_pool.return_connection(conn)
        if row:
            return User(*row)
        else:
            return None

    def update(self):
        connection_pool = ConnectionPool()
        conn = connection_pool.get_connection()
        cur = conn.cursor()
        cur.execute("UPDATE users SET username = %s, password = %s WHERE id = %s", (self.username, self.password, self.id))
        conn.commit()
        cur.close()
        connection_pool.return_connection(conn)

    def delete(self):
        connection_pool = ConnectionPool()
        conn = connection_pool.get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM users WHERE id = %s", (self.id,))
        conn.commit()
        cur.close()
        connection_pool.return_connection(conn)
