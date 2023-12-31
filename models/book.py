from connection import ConnectionPool

connection_pool = ConnectionPool()


class Book:
    def __init__(self, id, title, authors, categories, publication_date, pages, short_description, long_description, read=False, wish_to_read=False, thumbnail_url=None):
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
        self.thumbnail_url = thumbnail_url

    @classmethod
    def all(cls):
        conn = connection_pool.get_connection()
        cursor = conn.cursor()
        sql_query = """
                    SELECT 
                       b.id, b.title, b.page_count, TO_CHAR(b.published_date::DATE, 'dd/mm/yyyy'), b.short_description, b.long_description, b.status, c.name as categories, string_agg(a.name, '|') as authors, b.thumbnail_url
                    FROM books b
                        JOIN book_authors ba ON b.id = ba.book_id
                        JOIN authors a ON ba.author_id = a.id
                        JOIN book_categories bc ON b.id = bc.book_id
                        JOIN categories c ON bc.category_id = c.id
                    """
        sql_query += " GROUP BY b.id, b.title, b.page_count, b.published_date, b.short_description, b.long_description, b.status, c.name"
        cursor.execute(sql_query)
        books = cursor.fetchall()
        cursor.close()
        connection_pool.return_connection(conn)
        return [Book(id=book[0],
                     title=book[1],
                     authors=book[8],
                     categories=book[7],
                     publication_date=book[3],
                     pages=book[2],
                     short_description=book[4],
                     long_description=book[5],
                     read=book[6],
                     thumbnail_url=book[9]) for book in books]

    @classmethod
    def find_by_id(cls, id):
        conn = connection_pool.get_connection()
        cursor = conn.cursor()
        sql_query = """
                    SELECT 
                       b.id, b.title, b.page_count, TO_CHAR(b.published_date::DATE, 'dd/mm/yyyy'), b.short_description, b.long_description, b.status, c.name as categories, string_agg(a.name, '|') as authors, b.thumbnail_url
                    FROM books b
                        JOIN book_authors ba ON b.id = ba.book_id
                        JOIN authors a ON ba.author_id = a.id
                        JOIN book_categories bc ON b.id = bc.book_id
                        JOIN categories c ON bc.category_id = c.id
                    WHERE b.id = %s
                    """
        sql_query += " GROUP BY b.id, b.title, b.page_count, b.published_date, b.short_description, b.long_description, b.status, c.name"
        cursor.execute(sql_query, (id,))
        book = cursor.fetchone()
        cursor.close()
        connection_pool.return_connection(conn)
        if book:
            return cls(*book)
        return None

    @classmethod
    def get_status(cls, id, user_id):
        conn = connection_pool.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM user_read_books WHERE user_id = %s AND book_id = %s", (user_id, id))
        user_read_book = cursor.fetchone()
        cursor.execute(
            "SELECT * FROM user_wish_list WHERE user_id = %s AND book_id = %s", (user_id, id))
        user_wish_list_book = cursor.fetchone()
        cursor.close()
        connection_pool.return_connection(conn)
        data = {
            'read': user_read_book is not None,
            'wish': user_wish_list_book is not None
        }
        return data

    @classmethod
    def search(cls, query=None, author=None, category=None, min_pages=None, max_pages=None, start_date=None, end_date=None, id_user=None):
        conn = connection_pool.get_connection()
        cursor = conn.cursor()

        # Build the SQL query based on the provided parameters
        sql_query = """
        SELECT
            b.id,
            b.title,
            b.page_count,
            TO_CHAR(b.published_date, 'DD/MM/YYYY') as formatted_published_date,
            b.short_description,
            b.long_description,
            b.status,
            string_agg(DISTINCT c.name, '|') as categories,
            string_agg(DISTINCT a.name, '|') as authors,
            b.thumbnail_url
        FROM books b
            JOIN book_authors ba ON b.id = ba.book_id
            JOIN authors a ON ba.author_id = a.id
            JOIN book_categories bc ON b.id = bc.book_id
            JOIN categories c ON bc.category_id = c.id
        """
        if query:
            sql_query += f" AND (b.title ILIKE '%{query}%' OR b.short_description ILIKE '%{query}%')"
        if author:
            sql_query += f" AND a.name = '{author}'"
        if category:
            sql_query += f" AND c.name = '{category}'"
        if min_pages:
            sql_query += f" AND b.page_count >= {min_pages}"
        if max_pages:
            sql_query += f" AND b.page_count <= {max_pages}"
        if start_date:
            sql_query += f" AND b.publication_date >= '{start_date}'"
        if end_date:
            sql_query += f" AND b.publication_date <= '{end_date}'"

        sql_query += " GROUP BY b.id, b.title, b.page_count, b.published_date, b.short_description, b.long_description, b.status, b.thumbnail_url;"
        cursor.execute(sql_query)
        books = cursor.fetchall()
        cursor.close()
        connection_pool.return_connection(conn)
        return [Book(id=book[0],
                     title=book[1],
                     authors=book[8],
                     categories=book[7],
                     publication_date=book[3],
                     pages=book[2],
                     short_description=book[4],
                     long_description=book[5],
                     read=book[6],
                     thumbnail_url=book[9]) for book in books]

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

    def mark_as_read(self, user_id):
        conn = connection_pool.get_connection()

        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM user_read_books WHERE user_id = %s AND book_id = %s", (user_id, self.id))
        user_read_book = cursor.fetchone()
        if not user_read_book:
            cursor.execute(
                "INSERT INTO user_read_books (user_id, book_id, read_date) VALUES (%s, %s, NOW())", (user_id, self.id))
            conn.commit()
        cursor.close()
        connection_pool.return_connection(conn)

    def mark_as_unread(self, user_id):
        conn = connection_pool.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM user_read_books WHERE user_id = %s AND book_id = %s", (user_id, self.id))
        conn.commit()
        cursor.close()
        connection_pool.return_connection(conn)

    def mark_as_wishlist(self, user_id):
        conn = connection_pool.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM user_wish_list WHERE user_id = %s AND book_id = %s", (user_id, self.id))
        user_wish_list = cursor.fetchone()
        if not user_wish_list:
            cursor.execute(
                "INSERT INTO user_wish_list (user_id, book_id, added_date) VALUES (%s, %s, NOW())", (user_id, self.id))
            conn.commit()
        cursor.close()
        connection_pool.return_connection(conn)

    def mark_as_unwishlist(self, user_id):
        conn = connection_pool.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM user_wish_list WHERE user_id = %s AND book_id = %s", (user_id, self.id))
        conn.commit()
        cursor.close()
        connection_pool.return_connection(conn)

    @staticmethod
    def get_all_read_books(user_id):
        conn = connection_pool.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """SELECT
                b.id,
                b.title,
                b.page_count,
                TO_CHAR(b.published_date, 'DD/MM/YYYY') as formatted_published_date,
                b.short_description,
                b.long_description,
                b.status,
                string_agg(DISTINCT c.name, '|') as categories,
                string_agg(DISTINCT a.name, '|') as authors,
                b.thumbnail_url
            FROM
                books b
                JOIN book_authors ba ON b.id = ba.book_id
                JOIN authors a ON ba.author_id = a.id
                JOIN book_categories bc ON b.id = bc.book_id
                JOIN categories c ON bc.category_id = c.id
                JOIN user_read_books urb ON urb.book_id = b.id
            WHERE
                urb.user_id = %s
            GROUP BY
                b.id,
                b.title,
                b.page_count,
                b.published_date,
                b.short_description,
                b.long_description,
                b.status,
                b.thumbnail_url;
            """, (user_id,))
        user_read_books = cursor.fetchall()
        cursor.close()
        connection_pool.return_connection(conn)
        return [Book(id=book[0],
                     title=book[1],
                     authors=book[8],
                     categories=book[7],
                     publication_date=book[3],
                     pages=book[2],
                     short_description=book[4],
                     long_description=book[5],
                     thumbnail_url=book[9],
                     read=True
                     ) for book in user_read_books]

    @staticmethod
    def get_all_wishlist_books(user_id):
        conn = connection_pool.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """SELECT
                b.id,
                b.title,
                b.page_count,
                TO_CHAR(b.published_date, 'DD/MM/YYYY') as formatted_published_date,
                b.short_description,
                b.long_description,
                b.status,
                string_agg(DISTINCT c.name, '|') as categories,
                string_agg(DISTINCT a.name, '|') as authors,
                b.thumbnail_url
            FROM
                books b
                JOIN book_authors ba ON b.id = ba.book_id
                JOIN authors a ON ba.author_id = a.id
                JOIN book_categories bc ON b.id = bc.book_id
                JOIN categories c ON bc.category_id = c.id
                JOIN user_wish_list uwl ON uwl.book_id = b.id
            WHERE
                uwl.user_id = %s
            GROUP BY
                b.id,
                b.title,
                b.page_count,
                b.published_date,
                b.short_description,
                b.long_description,
                b.status,
                b.thumbnail_url;
            """, (user_id,))
        user_wish_list_books = cursor.fetchall()
        cursor.close()
        connection_pool.return_connection(conn)
        return [Book(id=book[0],
                     title=book[1],
                     authors=book[8],
                     categories=book[7],
                     publication_date=book[3],
                     pages=book[2],
                     short_description=book[4],
                     long_description=book[5],
                     thumbnail_url=book[9],
                     wish_to_read=True
                     ) for book in user_wish_list_books]

    def get_read_book(self, user_id):
        conn = connection_pool.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """SELECT * FROM user_read_books urb
                JOIN books b ON urb.book_id = b.id
                JOIN book_authors ba ON b.id = ba.book_id
                JOIN authors a ON ba.author_id = a.id
                JOIN book_categories bc ON b.id = bc.book_id
                JOIN categories c ON bc.category_id = c.id
            WHERE urb.user_id = %s AND urb.book_id = %s
            """, (user_id, self.id))
        user_read_book = cursor.fetchone()
        cursor.close()
        connection_pool.return_connection(conn)
        # if the book is not in the user_read_books table, return False, else
        if not user_read_book:
            return False
        else:
            return True

    def get_wishlist_book(self, user_id):
        conn = connection_pool.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """SELECT * FROM user_wish_list uw
                JOIN books b ON uw.book_id = b.id
                JOIN book_authors ba ON b.id = ba.book_id
                JOIN authors a ON ba.author_id = a.id
                JOIN book_categories bc ON b.id = bc.book_id
                JOIN categories c ON bc.category_id = c.id
            WHERE uw.user_id = %s AND uw.book_id = %s
            """, (user_id, self.id))
        user_wish_list_book = cursor.fetchone()
        cursor.close()
        connection_pool.return_connection(conn)
        # if the book is not in the user_wish_list table, return False, else
        if not user_wish_list_book:
            return False
        else:
            return True

    def to_dict(self):
        # if any key is null, it will be replaced by N/A
        for key in self.__dict__:
            if not self.__dict__[key]:
                self.__dict__[key] = 'N/A'
        return {
            'id': self.id,
            'title': self.title,
            'authors': self.authors,
            'categories': self.categories,
            'publication_date': self.publication_date,
            'pages': self.pages,
            'short_description': self.short_description,
            'long_description': self.long_description,
            'read': self.read,
            'wish_to_read': self.wish_to_read,
            'thumbnail_url': self.thumbnail_url,
        }
