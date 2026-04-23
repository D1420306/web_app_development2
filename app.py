from flask import Flask
from app.routes.book_routes import book_bp
import sqlite3
import os

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-12345')

# 註冊 Blueprint
app.register_blueprint(book_bp)

def init_db():
    """初始化資料庫"""
    base_dir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(base_dir, 'instance', 'database.db')
    schema_path = os.path.join(base_dir, 'database', 'schema.sql')
    
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    with sqlite3.connect(db_path) as conn:
        with open(schema_path, 'r', encoding='utf-8') as f:
            conn.executescript(f.read())
        print("資料庫初始化完成！")

if __name__ == '__main__':
    # 開發環境下自動初始化 DB (若不存在)
    if not os.path.exists(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance', 'database.db')):
        init_db()
    app.run(debug=True)
