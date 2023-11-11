from flask import Blueprint, jsonify, request
from models.book import Book

# Create a Flask blueprint
books_bp = Blueprint('books', __name__)

# Define the routes for the blueprint
@books_bp.route('/books')
def get_books():
    books = Book.all()
    return jsonify(books)

@books_bp.route('/books/search', methods=['GET'])
def search_books():
    # Obtén los parámetros de búsqueda de la URL
    query = request.args.get('query')
    author = request.args.get('author')
    category = request.args.get('category')
    min_pages = request.args.get('min_pages')
    max_pages = request.args.get('max_pages')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    books = Book.search(query=query, author=author, category=category, min_pages=min_pages, max_pages=max_pages, start_date=start_date, end_date=end_date)
    books = Book.sort(books)
    
    return jsonify(books)

@books_bp.route('/books/<int:book_id>')
def get_book(book_id):
    book = Book.find_by_id(book_id)
    return jsonify(book)

@books_bp.route('/books/<int:book_id>/read', methods=['POST'])
def mark_book_as_read(book_id):
    # Marca el libro como leído en la base de datos
    Book.mark_as_read(book_id)

    return jsonify({'message': 'Libro marcado como leído.'})

@books_bp.route('/books/<int:book_id>/wish', methods=['POST'])
def add_book_to_wish_list(book_id):
    # Agrega el libro a la lista de libros por leer en la base de datos
    Book.add_to_wish_list(book_id)

    return jsonify({'message': 'Libro agregado a la lista de libros por leer.'})
