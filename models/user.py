from flask_login import UserMixin
from connection import ConnectionPool

# Definición de la clase User


class User(UserMixin):
    def __init__(self, username: str, email: str, password: str, id: int = None):
        self.username = username
        self.email = email
        self.password = password
        self.id = id

    @staticmethod
    def create(username, email, password):
        connection_pool = ConnectionPool()
        conn = connection_pool.get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
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
        cur.execute("UPDATE users SET username = %s, password = %s WHERE id = %s",
                    (self.username, self.id))
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

    @staticmethod
    def login(email):
        connection_pool = ConnectionPool()
        conn = connection_pool.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        row = cur.fetchone()
        cur.close()
        connection_pool.return_connection(conn)
        if row:
            return User(username=row[1], email=row[2], password=row[3], id=row[0])
        else:
            return None
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
        }
        
    
