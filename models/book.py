from connection import ConnectionPool

connection_pool = ConnectionPool()

class Book:
    def __init__(self, title, author, category, publication_date, pages, description, read=False, wish_to_read=False):
        self.title = title
        self.author = author
        self.category = category
        self.publication_date = publication_date
        self.pages = pages
        self.description = description
        self.read = read
        self.wish_to_read = wish_to_read

    @classmethod
    def all(cls):
        conn = connection_pool.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books")
        books = cursor.fetchall()
        cursor.close()
        connection_pool.return_connection(conn)
        return [cls(*book) for book in books]

    @classmethod
    def find_by_id(cls, id):
        conn = connection_pool.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books WHERE id = %s", (id,))
        book = cursor.fetchone()
        cursor.close()
        connection_pool.return_connection(conn)
        if book:
            return cls(*book)
        return None
    

    @classmethod
    def search(cls, query=None, author=None, category=None, min_pages=None, max_pages=None, start_date=None, end_date=None):
        conn = connection_pool.get_connection()
        cursor = conn.cursor()

        # Build the SQL query based on the provided parameters
        sql_query = "SELECT * FROM books WHERE 1=1"
        if query:
            sql_query += f" AND (title LIKE '%{query}%' OR description LIKE '%{query}%')"
        if author:
            sql_query += f" AND author = '{author}'"
        if category:
            sql_query += f" AND category = '{category}'"
        if min_pages:
            sql_query += f" AND pages >= {min_pages}"
        if max_pages:
            sql_query += f" AND pages <= {max_pages}"
        if start_date:
            sql_query += f" AND publication_date >= '{start_date}'"
        if end_date:
            sql_query += f" AND publication_date <= '{end_date}'"

        cursor.execute(sql_query)
        books = cursor.fetchall()
        cursor.close()
        connection_pool.return_connection(conn)
        return [cls(*book) for book in books]

    def update(self):
        conn = connection_pool.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE books SET title = %s, author = %s, category = %s, publication_date = %s, pages = %s, description = %s, read = %s, wish_to_read = %s WHERE id = %s",
            (self.title, self.author, self.category, self.publication_date, self.pages, self.description, self.read, self.wish_to_read, self.id))
        conn.commit()
        cursor.close()
        connection_pool.return_connection(conn)

    def delete(self):
        conn = connection_pool.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM books WHERE id = %s", (self.id,))
        conn.commit()
        cursor.close()
        connection_pool.return_connection(conn)
