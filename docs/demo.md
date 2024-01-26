在生产环境中，通常会将 Flask 应用程序拆分成更为结构化的形式，采用 MVC（Model-View-Controller）或类似的设计模式来组织代码。这样可以使代码更清晰、易于维护，并支持更好的可扩展性。下面是一种常见的组织结构：

1. **创建一个 `models.py` 文件：**

    ```python
    # models.py

    from flask_sqlalchemy import SQLAlchemy
    from datetime import datetime

    db = SQLAlchemy()

    class Book(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(200), nullable=False)
        author = db.Column(db.String(200), nullable=False)
        create_date = db.Column(db.DateTime, default=datetime.utcnow)
    ```

2. **创建一个 `views.py` 文件：**

    ```python
    # views.py

    from flask import Blueprint, jsonify
    from .models import Book

    main = Blueprint('main', __name__)

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
    ```

3. **修改 `app.py` 文件：**

    ```python
    from flask import Flask
    from models import db
    from views import main

    app = Flask(__name__)

    # 配置数据库连接
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/dbname'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 初始化 SQLAlchemy
    db.init_app(app)

    # 注册蓝图
    app.register_blueprint(main)

    if __name__ == '__main__':
        app.run(debug=True)
    ```

这种结构的优势在于：

- `models.py` 文件包含所有模型的定义，用于与数据库进行交互。
- `views.py` 文件包含所有与视图（路由）相关的代码，例如请求处理逻辑。
- `app.py` 文件用于配置应用程序，初始化 Flask 和 SQLAlchemy，以及注册蓝图。

这样的组织方式有助于保持代码清晰，使得不同部分的代码分开，并且易于维护。同时，你可以根据需求进一步拆分代码，例如创建单独的文件夹用于存放蓝图、模型等。

在生产环境中，通常还会考虑使用一些优秀的 Flask 扩展，如 Flask-Migrate 用于数据库迁移、Flask-Script 用于管理命令行脚本等，以提高应用程序的可维护性和可扩展性。