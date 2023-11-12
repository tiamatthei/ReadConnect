import math
from flask import Blueprint, jsonify, request
from models.book import Book

# Create a Flask blueprint
books_bp = Blueprint('books', __name__)

# Define the routes for the blueprint
@books_bp.route('/books')
def get_books():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)
    
    books = Book.all()
    books = Book.sort(books)
    paginated_books = books[(page-1)*per_page:page*per_page]

    pagination = {
        'page': page,
        'per_page': per_page,
        'total_pages': math.ceil(len(books) / per_page),
        'total_items': len(books)
    }
    
    return jsonify({'books': paginated_books, 'pagination': pagination})

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
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)

    books = Book.search(query=query, author=author, category=category, min_pages=min_pages, max_pages=max_pages, start_date=start_date, end_date=end_date)
    books = Book.sort(books)
    paginated_books = books[(page-1)*per_page:page*per_page]

    pagination = {
        'page': page,
        'per_page': per_page,
        'total_pages': math.ceil(len(books) / per_page),
        'total_items': len(books)
    }
    return jsonify({'books': paginated_books, 'pagination': pagination})

@books_bp.route('/books/<int:book_id>')
def get_book(book_id):
    book = Book.find_by_id(book_id)
    return jsonify(book)

@books_bp.route('/books/<int:book_id>/read', methods=['POST'])
def mark_book_as_read(book_id):
    # Marca el libro como leído en la base de datos
    book = Book.find_by_id(book_id)
    if book:
        book.mark_as_read()
        return jsonify({'message': 'Libro marcado como leído.'})
    else:
        return jsonify({'message': 'Libro no encontrado.'}), 404
    

@books_bp.route('/books/<int:book_id>/wish', methods=['POST'])
def add_book_to_wish_list(book_id):
    # Agrega el libro a la lista de libros por leer en la base de datos
    book = Book.find_by_id(book_id)
    if book:
        book.mark_as_wishlist()
        return jsonify({'message': 'Libro agregado a la lista de libros por leer.'})
    else:
        return jsonify({'message': 'Libro no encontrado.'}), 404
    
@books_bp.route('/books/<int:book_id>/read', methods=['DELETE'])
def remove_book_from_read_list(book_id):
    # Elimina el libro de la lista de libros leídos en la base de datos
    book = Book.find_by_id(book_id)
    if book:
        book.mark_as_unread()
        return jsonify({'message': 'Libro eliminado de la lista de libros leídos.'})
    else:
        return jsonify({'message': 'Libro no encontrado.'}), 404
    
@books_bp.route('/books/<int:book_id>/wish', methods=['DELETE'])
def remove_book_from_wish_list(book_id):
    # Elimina el libro de la lista de libros por leer en la base de datos
    book = Book.find_by_id(book_id)
    if book:
        book.mark_as_unwishlist()
        return jsonify({'message': 'Libro eliminado de la lista de libros por leer.'})
    else:
        return jsonify({'message': 'Libro no encontrado.'}), 404


@books_bp.route('/read_books/<int:user_id>')
def get_read_books(user_id):
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)
    
    books = Book.get_all_read_books(user_id)
    books = Book.sort(books)
    paginated_books = books[(page-1)*per_page:page*per_page]

    pagination = {
        'page': page,
        'per_page': per_page,
        'total_pages': math.ceil(len(books) / per_page),
        'total_items': len(books)
    }
    
    return jsonify({'books': paginated_books, 'pagination': pagination})

@books_bp.route('/wish_books/<int:user_id>')
def get_wish_books(user_id):
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)
    
    books = Book.get_all_wishlist_books(user_id)
    books = Book.sort(books)
    paginated_books = books[(page-1)*per_page:page*per_page]

    pagination = {
        'page': page,
        'per_page': per_page,
        'total_pages': math.ceil(len(books) / per_page),
        'total_items': len(books)
    }
    
    return jsonify({'books': paginated_books, 'pagination': pagination})
