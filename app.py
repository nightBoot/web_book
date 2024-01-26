# app.py

from flask import Flask
from app.models import db
from app.views import main

app = Flask(__name__)

# 配置数据库连接
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:it0703@127.0.0.1:3306/erp_tool'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化 SQLAlchemy
db.init_app(app)

# 注册视图
app.register_blueprint(main)

if __name__ == '__main__':
    app.run(debug=True)