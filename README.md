使用 Flask 创建 REST API 操作 MySQL 数据表 `book` 的项目，并提供一些基本的用法和步骤。

### 步骤：

1. **创建项目文件夹:**
    ```bash
    mkdir flask_book_api
    cd flask_book_api
    ```

2. **创建虚拟环境:**
    ```bash
    python -m venv venv
    ```

3. **激活虚拟环境:**
    - Windows:
        ```bash
        venv\Scripts\activate
        ```
    - Linux/Mac:
        ```bash
        source venv/bin/activate
        ```

4. **安装 Flask 和 Flask-SQLAlchemy:**
    ```bash
    pip install Flask Flask-SQLAlchemy pymysql
    ```

5. **创建主应用文件 `app.py`:**
    ```python
    from flask import Flask, request, jsonify
    from flask_sqlalchemy import SQLAlchemy
    from datetime import datetime

    app = Flask(__name__)

    # 配置数据库连接
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/dbname'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 创建 SQLAlchemy 实例
    db = SQLAlchemy(app)

    # 定义 Book 模型
    class Book(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(200), nullable=False)
        author = db.Column(db.String(200), nullable=False)
        create_date = db.Column(db.DateTime, default=datetime.utcnow)

    # 创建数据库表
    db.create_all()

    # 路由 - 获取所有书籍
    @app.route('/books', methods=['GET'])
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

    # 路由 - 获取单个书籍
    @app.route('/books/<int:book_id>', methods=['GET'])
    def get_book(book_id):
        book = Book.query.get_or_404(book_id)
        book_data = {
            'id': book.id,
            'name': book.name,
            'author': book.author,
            'create_date': book.create_date.strftime('%Y-%m-%d %H:%M:%S')
        }
        return jsonify({'book': book_data})

    # 路由 - 添加书籍
    @app.route('/books', methods=['POST'])
    def add_book():
        data = request.get_json()

        new_book = Book(name=data['name'], author=data['author'])

        try:
            db.session.add(new_book)
            db.session.commit()
            return jsonify({'message': 'Book added successfully'})
        except:
            return jsonify({'message': 'Error adding book'}), 500

    # 路由 - 更新书籍
    @app.route('/books/<int:book_id>', methods=['PUT'])
    def update_book(book_id):
        book = Book.query.get_or_404(book_id)
        data = request.get_json()

        book.name = data['name']
        book.author = data['author']

        try:
            db.session.commit()
            return jsonify({'message': 'Book updated successfully'})
        except:
            return jsonify({'message': 'Error updating book'}), 500

    # 路由 - 删除书籍
    @app.route('/books/<int:book_id>', methods=['DELETE'])
    def delete_book(book_id):
        book = Book.query.get_or_404(book_id)

        try:
            db.session.delete(book)
            db.session.commit()
            return jsonify({'message': 'Book deleted successfully'})
        except:
            return jsonify({'message': 'Error deleting book'}), 500

    if __name__ == '__main__':
        app.run(debug=True)
    ```

6. **运行应用程序:**
    ```bash
    python app.py
    ```

7. **使用 Postman 或其他 API 测试工具测试 API:**
    - GET 请求获取所有书籍：`http://127.0.0.1:5000/books`
    - GET 请求获取单个书籍：`http://127.0.0.1:5000/books/1`
    - POST 请求添加书籍：`http://127.0.0.1:5000/books`（使用 JSON 格式的请求体）
    - PUT 请求更新书籍：`http://127.0.0.1:5000/books/1`（使用 JSON 格式的请求体）
    - DELETE 请求删除书籍：`http://127.0.0.1:5000/books/1`

请确保替换 `mysql://username:password@localhost/dbname` 中的 `username`, `password`, `localhost`, 和 `dbname` 为你的 MySQL 数据库的实际配置。

这个项目提供了一个基本的 REST API，用于对 `book` 表执行 CRUD 操作。你可以根据实际需求进行扩展和优化。