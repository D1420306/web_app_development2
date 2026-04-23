import sqlite3
import os

# 資料庫檔案路徑 (對應 architecture.md 設計的 instance/database.db)
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'instance', 'database.db')

def get_db_connection():
    """取得資料庫連線"""
    # 確保 instance 資料夾存在
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # 讓回傳的資料可以像字典一樣透過欄位名稱存取
    return conn

class Book:
    @staticmethod
    def get_all(search_query=None):
        """取得所有書籍紀錄，可選傳入 search_query 進行書名模糊搜尋"""
        conn = get_db_connection()
        if search_query:
            books = conn.execute('SELECT * FROM books WHERE title LIKE ? ORDER BY created_at DESC', ('%' + search_query + '%',)).fetchall()
        else:
            books = conn.execute('SELECT * FROM books ORDER BY created_at DESC').fetchall()
        conn.close()
        return books

    @staticmethod
    def get_by_id(book_id):
        """根據 ID 取得單一書籍紀錄"""
        conn = get_db_connection()
        book = conn.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()
        conn.close()
        return book

    @staticmethod
    def create(title, review, rating):
        """新增一筆書籍紀錄"""
        conn = get_db_connection()
        conn.execute('INSERT INTO books (title, review, rating) VALUES (?, ?, ?)',
                     (title, review, rating))
        conn.commit()
        conn.close()

    @staticmethod
    def update(book_id, title, review, rating):
        """更新特定書籍紀錄"""
        conn = get_db_connection()
        conn.execute('UPDATE books SET title = ?, review = ?, rating = ? WHERE id = ?',
                     (title, review, rating, book_id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(book_id):
        """刪除特定書籍紀錄"""
        conn = get_db_connection()
        conn.execute('DELETE FROM books WHERE id = ?', (book_id,))
        conn.commit()
        conn.close()
