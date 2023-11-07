
import json
from dotenv import dotenv_values
import psycopg2

secrets = dotenv_values(".env")
# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host=secrets['DB_HOST'],
    database=secrets['DB_NAME'],
    user=secrets['DB_USER'],
    password=secrets['DB_PASSWORD']
)

# Open the JSON file and load the data
with open('amazon.books.json', "r") as f:
    data = json.load(f)['data']

# Loop through the data and insert each book into the database
for book in data:
    print(book)
    cur = conn.cursor()
    book_id = book['_id']
    if isinstance(book_id, dict):
        book_id = book_id['$oid']
        
    #list of possible keys, if a key is not present, it will be set to None
    keys = ['isbn', 'pageCount', 'publishedDate', 'thumbnailUrl', 'shortDescription', 'longDescription', 'status']
    for key in keys:
        if key not in book:
            book[key] = None
    
    cur.execute("INSERT INTO books (id, title, isbn, page_count, published_date, thumbnail_url, short_description, long_description, status) VALUES %s", [(book_id, book['title'], book['isbn'], book['pageCount'], book['publishedDate']['$date'], book['thumbnailUrl'], book['shortDescription'], book['longDescription'], book['status'])])
    conn.commit()

    # Insert authors
    author_values = [(author,) for author in book['authors']]
    cur.executemany("INSERT INTO authors (name) VALUES (%s) RETURNING id", author_values)
    author_ids = cur.fetchall()
    conn.commit()

    book_author_values = [(book_id, author_id) for author_id in author_ids]
    cur.executemany("INSERT INTO book_authors (book_id, author_id) VALUES (%s, %s)", book_author_values)
    conn.commit()

    # Insert categories
    category_values = [(category,) for category in book['categories']]
    cur.executemany("INSERT INTO categories (name) VALUES (%s) RETURNING id", category_values)
    category_ids = cur.fetchall()
    conn.commit()

    book_category_values = [(book_id, category_id) for category_id in category_ids]
    cur.executemany("INSERT INTO book_categories (book_id, category_id) VALUES (%s, %s)", book_category_values)
    conn.commit()

# Close the database connection
conn.close()

