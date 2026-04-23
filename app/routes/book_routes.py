from flask import Blueprint, render_template, request, redirect, url_for, flash, abort

# 建立 Blueprint 以模組化路由
book_bp = Blueprint('book_bp', __name__)

@book_bp.route('/')
def index():
    """
    處理首頁與書籍搜尋請求。
    GET: 取得所有書籍，若有 ?q 參數則進行書名過濾。
    渲染 templates/index.html
    """
    pass

@book_bp.route('/books/new', methods=['GET'])
def new_book():
    """
    顯示新增書籍的表單。
    GET: 渲染 templates/add.html
    """
    pass

@book_bp.route('/books', methods=['POST'])
def create_book():
    """
    處理新增書籍的表單送出。
    POST: 接收 title, review, rating。驗證後呼叫 Book.create()，成功則導向首頁。
    """
    pass

@book_bp.route('/books/<int:id>', methods=['GET'])
def detail(id):
    """
    顯示單一書籍詳細內容。
    GET: 根據 id 取得書籍。若無則 404。渲染 templates/detail.html
    """
    pass

@book_bp.route('/books/<int:id>/edit', methods=['GET'])
def edit_book(id):
    """
    顯示編輯書籍的表單。
    GET: 根據 id 取得書籍舊資料。若無則 404。渲染 templates/edit.html
    """
    pass

@book_bp.route('/books/<int:id>/update', methods=['POST'])
def update_book(id):
    """
    處理編輯書籍的表單送出。
    POST: 接收修改後的資料，呼叫 Book.update()。成功後導向該書籍的詳情頁。
    """
    pass

@book_bp.route('/books/<int:id>/delete', methods=['POST'])
def delete_book(id):
    """
    處理刪除書籍請求。
    POST: 呼叫 Book.delete(id)。成功後導向首頁。
    """
    pass
