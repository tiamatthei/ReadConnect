import json
from dotenv import dotenv_values
from psycopg2.extras import execute_values
import psycopg2
from psycopg2 import pool

secrets = dotenv_values(".env")

# Create a connection pool
connection_pool = pool.SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    host=secrets['DB_HOST'],
    database=secrets['DB_NAME'],
    user=secrets['DB_USER'],
    password=secrets['DB_PASSWORD'], 
    sslmode='require'
)

# Open the JSON file and load the data
with open('books3.json', "r") as f:
    data = json.load(f)['data']

starting = 797
# Loop through the data and insert each book into the database
for book in data:
    book_id = book['_id']
    if isinstance(book_id, dict):
        #use the starting value to generate a new id
        book_id = starting
        starting += 1

    # list of possible keys, if a key is not present, it will be set to None
    keys = ['isbn', 'pageCount', 'publishedDate', 'thumbnailUrl',
            'shortDescription', 'longDescription', 'status']
    for key in keys:
        if key not in book:
            book[key] = None
            
    try:
        published_date = book['publishedDate']['$date']
    except TypeError as e:
        print(book['publishedDate'], book['title'])
        published_date = None
    
    # Get a connection from the connection pool
    conn = connection_pool.getconn()
    cur = conn.cursor()

    query = "INSERT INTO books (id, title, isbn, page_count, published_date, thumbnail_url, short_description, long_description, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (book_id, book['title'], book['isbn'], book['pageCount'], published_date,
         book['thumbnailUrl'], book['shortDescription'], book['longDescription'], book['status'],)
    cur.execute(query, values)
    conn.commit()

    if book['authors'] is None or len(book['authors']) == 0:
        book['authors'] = ['Unknown']
    if book['categories'] is None or len(book['categories']) == 0:
        book['categories'] = ['Unknown']
        
    # Insert authors using execute_values
    author_values = [(author,) for author in book['authors']]
    insert_query = """
        INSERT INTO authors (name) 
        VALUES %s 
        ON CONFLICT (name) DO UPDATE SET name = authors.name
        RETURNING id
    """
    execute_values(cur, insert_query, author_values)
    author_ids = [row[0] for row in cur.fetchall()]

    # Insert book-authors relationships
    book_author_values = [(book_id, author_id) for author_id in author_ids]
    insert_query = "INSERT INTO book_authors (book_id, author_id) VALUES %s"
    execute_values(cur, insert_query, book_author_values)

    # Insert categories using execute_values
    category_values = [(category,) for category in book['categories']]
    insert_query = """
        INSERT INTO categories (name) 
        VALUES %s 
        ON CONFLICT (name) DO UPDATE SET name = categories.name
        RETURNING id
    """
    execute_values(cur, insert_query, category_values)
    category_ids = [row[0] for row in cur.fetchall()]

    # Insert book-categories relationships
    book_category_values = [(book_id, category_id) for category_id in category_ids]
    insert_query = "INSERT INTO book_categories (book_id, category_id) VALUES %s"
    execute_values(cur, insert_query, book_category_values)

    # Release the connection back to the connection pool
    cur.close()
    connection_pool.putconn(conn)

# Close the connection pool
connection_pool.closeall()
conn.close()
