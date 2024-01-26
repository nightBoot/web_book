# views.py

from flask import Blueprint, jsonify, request
from .models import db, Book

main = Blueprint('main', __name__)

# 获取所有图书
@main.route('/books', methods=['GET'])
def get_all_books():
    books = Book.query.all()
    book_list = []
    for book in books:
        book_data = {
            'id': book.id,
            'name': book.name,
            'author': book.author,
            'create_date': book.create_date.strftime('%Y-%m-%d %H:%M:%S')
        }
        book_list.append(book_data)
    return jsonify({'books': book_list})

# 获取单个图书
@main.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'error': 'Book not found'}), 404

    book_data = {
        'id': book.id,
        'name': book.name,
        'author': book.author,
        'create_date': book.create_date.strftime('%Y-%m-%d %H:%M:%S')
    }
    return jsonify({'book': book_data})

# 创建新图书
@main.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()
    new_book = Book(name=data['name'], author=data['author'])
    db.session.add(new_book)
    db.session.commit()
    return jsonify({'message': 'Book created successfully'}), 201

# 更新图书信息
@main.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'error': 'Book not found'}), 404

    data = request.get_json()
    book.name = data['name']
    book.author = data['author']
    db.session.commit()
    return jsonify({'message': 'Book updated successfully'})

# 删除图书
@main.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'error': 'Book not found'}), 404

    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book deleted successfully'})
