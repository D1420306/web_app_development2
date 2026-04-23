import sqlite3
import os

def get_db_connection():
    """
    取得資料庫連線
    回傳: sqlite3.Connection 物件
    """
    base_dir = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    db_path = os.path.join(base_dir, 'instance', 'database.db')
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

class Book:
    @staticmethod
    def get_all(search_query=None):
        """
        取得所有書籍記錄
        參數:
            search_query (str, optional): 書名模糊搜尋字串
        回傳:
            list: 包含 sqlite3.Row 的列表，若發生錯誤則回傳空列表 []
        """
        try:
            conn = get_db_connection()
            if search_query:
                books = conn.execute(
                    'SELECT * FROM books WHERE title LIKE ? ORDER BY created_at DESC', 
                    ('%' + search_query + '%',)
                ).fetchall()
            else:
                books = conn.execute('SELECT * FROM books ORDER BY created_at DESC').fetchall()
            return books
        except sqlite3.Error as e:
            print(f"資料庫錯誤 (get_all): {e}")
            return []
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def get_by_id(book_id):
        """
        根據 ID 取得單筆書籍記錄
        參數:
            book_id (int): 書籍 ID
        回傳:
            sqlite3.Row: 單一書籍資料，若找不到或發生錯誤則回傳 None
        """
        try:
            conn = get_db_connection()
            book = conn.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()
            return book
        except sqlite3.Error as e:
            print(f"資料庫錯誤 (get_by_id): {e}")
            return None
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def create(title, review, rating):
        """
        新增一筆書籍記錄
        參數:
            title (str): 書名
            review (str): 心得筆記
            rating (int): 評分 (1-5)
        回傳:
            bool: 成功回傳 True，失敗回傳 False
        """
        try:
            conn = get_db_connection()
            conn.execute(
                'INSERT INTO books (title, review, rating) VALUES (?, ?, ?)',
                (title, review, rating)
            )
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"資料庫錯誤 (create): {e}")
            return False
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def update(book_id, title, review, rating):
        """
        更新書籍記錄
        參數:
            book_id (int): 欲更新的書籍 ID
            title (str): 新書名
            review (str): 新心得筆記
            rating (int): 新評分 (1-5)
        回傳:
            bool: 成功回傳 True，失敗回傳 False
        """
        try:
            conn = get_db_connection()
            conn.execute(
                'UPDATE books SET title = ?, review = ?, rating = ? WHERE id = ?',
                (title, review, rating, book_id)
            )
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"資料庫錯誤 (update): {e}")
            return False
        finally:
            if 'conn' in locals() and conn:
                conn.close()

    @staticmethod
    def delete(book_id):
        """
        刪除特定書籍記錄
        參數:
            book_id (int): 欲刪除的書籍 ID
        回傳:
            bool: 成功回傳 True，失敗回傳 False
        """
        try:
            conn = get_db_connection()
            conn.execute('DELETE FROM books WHERE id = ?', (book_id,))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"資料庫錯誤 (delete): {e}")
            return False
        finally:
            if 'conn' in locals() and conn:
                conn.close()
