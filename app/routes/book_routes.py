from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from app.models.book import Book

# 建立 Blueprint 以模組化路由
book_bp = Blueprint('book_bp', __name__)

@book_bp.route('/')
def index():
    """
    處理首頁與書籍搜尋請求。
    GET: 取得所有書籍，若有 ?q 參數則進行書名過濾。
    渲染 templates/index.html
    """
    search_query = request.args.get('q', '').strip()
    books = Book.get_all(search_query if search_query else None)
    return render_template('index.html', books=books, search_query=search_query)

@book_bp.route('/books/new', methods=['GET'])
def new_book():
    """
    顯示新增書籍的表單。
    GET: 渲染 templates/add.html
    """
    return render_template('add.html')

@book_bp.route('/books', methods=['POST'])
def create_book():
    """
    處理新增書籍的表單送出。
    POST: 接收 title, review, rating。驗證後呼叫 Book.create()，成功則導向首頁。
    """
    title = request.form.get('title', '').strip()
    review = request.form.get('review', '').strip()
    rating = request.form.get('rating', '')

    # 驗證必填欄位
    if not title:
        flash("書名為必填欄位！", "danger")
        return render_template('add.html', title=title, review=review, rating=rating)
    
    # 驗證評分
    try:
        rating = int(rating) if rating else None
        if rating is not None and not (1 <= rating <= 5):
            flash("評分必須在 1 到 5 之間！", "danger")
            return render_template('add.html', title=title, review=review, rating=rating)
    except ValueError:
        flash("評分格式錯誤！", "danger")
        return render_template('add.html', title=title, review=review, rating=rating)

    success = Book.create(title, review, rating)
    if success:
        flash("成功新增書籍紀錄！", "success")
        return redirect(url_for('book_bp.index'))
    else:
        flash("新增失敗，請稍後再試。", "danger")
        return render_template('add.html', title=title, review=review, rating=rating)

@book_bp.route('/books/<int:id>', methods=['GET'])
def detail(id):
    """
    顯示單一書籍詳細內容。
    GET: 根據 id 取得書籍。若無則 404。渲染 templates/detail.html
    """
    book = Book.get_by_id(id)
    if not book:
        abort(404)
    return render_template('detail.html', book=book)

@book_bp.route('/books/<int:id>/edit', methods=['GET'])
def edit_book(id):
    """
    顯示編輯書籍的表單。
    GET: 根據 id 取得書籍舊資料。若無則 404。渲染 templates/edit.html
    """
    book = Book.get_by_id(id)
    if not book:
        abort(404)
    return render_template('edit.html', book=book)

@book_bp.route('/books/<int:id>/update', methods=['POST'])
def update_book(id):
    """
    處理編輯書籍的表單送出。
    POST: 接收修改後的資料，呼叫 Book.update()。成功後導向該書籍的詳情頁。
    """
    # 先確認書籍存在
    book = Book.get_by_id(id)
    if not book:
        abort(404)

    title = request.form.get('title', '').strip()
    review = request.form.get('review', '').strip()
    rating = request.form.get('rating', '')

    if not title:
        flash("書名為必填欄位！", "danger")
        # 建立一個暫時的字典來保持使用者剛剛輸入的值
        temp_book = {'id': id, 'title': title, 'review': review, 'rating': rating}
        return render_template('edit.html', book=temp_book)
    
    try:
        rating = int(rating) if rating else None
        if rating is not None and not (1 <= rating <= 5):
            flash("評分必須在 1 到 5 之間！", "danger")
            temp_book = {'id': id, 'title': title, 'review': review, 'rating': rating}
            return render_template('edit.html', book=temp_book)
    except ValueError:
        flash("評分格式錯誤！", "danger")
        temp_book = {'id': id, 'title': title, 'review': review, 'rating': rating}
        return render_template('edit.html', book=temp_book)

    success = Book.update(id, title, review, rating)
    if success:
        flash("成功更新書籍紀錄！", "success")
        return redirect(url_for('book_bp.detail', id=id))
    else:
        flash("更新失敗，請稍後再試。", "danger")
        temp_book = {'id': id, 'title': title, 'review': review, 'rating': rating}
        return render_template('edit.html', book=temp_book)

@book_bp.route('/books/<int:id>/delete', methods=['POST'])
def delete_book(id):
    """
    處理刪除書籍請求。
    POST: 呼叫 Book.delete(id)。成功後導向首頁。
    """
    # 先確認書籍存在
    book = Book.get_by_id(id)
    if not book:
        abort(404)

    success = Book.delete(id)
    if success:
        flash("書籍已成功刪除。", "success")
    else:
        flash("刪除失敗，請稍後再試。", "danger")
        
    return redirect(url_for('book_bp.index'))
