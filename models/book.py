from connection import ConnectionPool

connection_pool = ConnectionPool()


class Book:
    def __init__(self, id, title, authors, categories, publication_date, pages, short_description, long_description, read=False, wish_to_read=False):
        self.id = id
        self.title = title
        self.authors = authors
        self.categories = categories
        self.publication_date = publication_date
        self.pages = pages
        self.short_description = short_description
        self.long_description = long_description
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
        sql_query = """
        SELECT
            b.id, b.title, b.page_count, b.published_date, b.short_description, b.long_description, b.status, c.name as categories, string_agg(a.name, '|') as authors
        FROM books b
            JOIN book_authors ba ON b.id = ba.book_id
            JOIN authors a ON ba.author_id = a.id
            JOIN book_categories bc ON b.id = bc.book_id
            JOIN categories c ON bc.category_id = c.id
        """
        if query:
            sql_query += f" AND (b.title ILIKE '%{query}%' OR b.short_description ILIKE '%{query}%')"
        if author:
            sql_query += f" AND authors = '{author}'"
        if category:
            sql_query += f" AND categories = '{category}'"
        if min_pages:
            sql_query += f" AND b.page_count >= {min_pages}"
        if max_pages:
            sql_query += f" AND b.page_count <= {max_pages}"
        if start_date:
            sql_query += f" AND b.publication_date >= '{start_date}'"
        if end_date:
            sql_query += f" AND b.publication_date <= '{end_date}'"

        sql_query += " GROUP BY b.id, b.title, b.page_count, b.published_date, b.short_description, b.long_description, b.status, c.name"
        print(sql_query)
        cursor.execute(sql_query)
        books = cursor.fetchall()
        cursor.close()
        connection_pool.return_connection(conn)
        return [Book(id=book[0], title=book[1], authors=book[8], categories=book[7], publication_date=book[3], pages=book[2], short_description=book[4], long_description=book[5], read=book[6]) for book in books]

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

    @staticmethod
    def sort(books):
        for book in books:
            book.authors = book.authors.split('|')
            book.categories = book.categories.split('|')

        books.sort(key=lambda book: book.id)

        # use the to_dict method to convert the books to a dictionary
        books = [book.to_dict() for book in books]

        return books

    def to_dict(self):
        #if any key is null, it will be replaced by N/A
        for key in self.__dict__:
            if not self.__dict__[key]:
                self.__dict__[key] = 'N/A'
        return {
            'title': self.title,
            'authors': self.authors,
            'categories': self.categories,
            'publication_date': self.publication_date,
            'pages': self.pages,
            'short_description': self.short_description,
            'long_description': self.long_description,
            'read': self.read,
            'wish_to_read': self.wish_to_read
        }
