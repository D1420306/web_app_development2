# 路由與頁面設計 (API Design) - 讀書筆記本

本文件依據 PRD 與資料庫設計，規劃系統所需的所有 HTTP 路由與對應的 HTML 模板。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| ---- | --------- | -------- | -------- | ---- |
| 首頁 (書籍列表) | GET | `/` | `index.html` | 顯示所有讀書筆記，支援書名搜尋 |
| 新增書籍頁面 | GET | `/books/new` | `add.html` | 顯示新增書籍與心得的表單 |
| 建立書籍 | POST | `/books` | — | 接收表單，存入 DB，重導向至首頁 |
| 書籍詳情 | GET | `/books/<int:id>` | `detail.html` | 顯示單筆書籍的完整心得與評分 |
| 編輯書籍頁面 | GET | `/books/<int:id>/edit` | `edit.html` | 顯示包含舊有資料的編輯表單 |
| 更新書籍 | POST | `/books/<int:id>/update` | — | 接收表單，更新 DB，重導向至書籍詳情 |
| 刪除書籍 | POST | `/books/<int:id>/delete` | — | 刪除指定書籍，重導向至首頁 |

## 2. 每個路由的詳細說明

### 首頁 (書籍列表)
- **輸入**：URL 參數 `?q=關鍵字`（選填，用於搜尋書名）。
- **處理邏輯**：呼叫 `Book.get_all(search_query)` 取得資料。
- **輸出**：渲染 `index.html`，傳遞書籍列表給前端。
- **錯誤處理**：無特定錯誤，若無資料則顯示「尚無書籍紀錄」。

### 新增書籍與心得 (顯示表單與建立)
- **GET `/books/new`**：
  - 輸出：渲染 `add.html`，提供填寫 `title`, `review`, `rating` 的表單。
- **POST `/books`**：
  - 輸入：表單欄位 `title` (必填), `review`, `rating`。
  - 處理邏輯：驗證 `title` 是否存在，若無誤則呼叫 `Book.create(...)`。
  - 輸出：重導向至 `/` (首頁)。
  - 錯誤處理：若 `title` 為空，重新渲染 `add.html` 並顯示錯誤訊息。

### 書籍詳情與編輯、刪除
- **GET `/books/<int:id>`** (書籍詳情)：
  - 輸入：URL 參數 `id`。
  - 處理邏輯：呼叫 `Book.get_by_id(id)`。
  - 輸出：渲染 `detail.html`。
  - 錯誤處理：若找不到該 ID，回傳 404 Not Found 頁面。
- **GET `/books/<int:id>/edit`** (編輯頁面)：
  - 輸入：URL 參數 `id`。
  - 處理邏輯：呼叫 `Book.get_by_id(id)`。
  - 輸出：渲染 `edit.html`，將舊資料帶入表單。
  - 錯誤處理：若找不到該 ID，回傳 404。
- **POST `/books/<int:id>/update`** (更新書籍)：
  - 輸入：URL 參數 `id` 與表單資料 `title`, `review`, `rating`。
  - 處理邏輯：呼叫 `Book.update(...)`。
  - 輸出：重導向至 `/books/<int:id>` (書籍詳情頁)。
- **POST `/books/<int:id>/delete`** (刪除書籍)：
  - 輸入：URL 參數 `id`。
  - 處理邏輯：呼叫 `Book.delete(id)`。
  - 輸出：重導向至 `/` (首頁)。

## 3. Jinja2 模板清單

所有的模板將放置於 `app/templates/` 目錄下：

1. **`base.html`**：共用基礎版型，包含 HTML `<head>`、CSS 連結、共用導覽列 (Navbar) 與頁首/頁尾。其餘頁面皆繼承此模板。
2. **`index.html`** (繼承 `base.html`)：顯示搜尋列與書籍卡片列表。
3. **`add.html`** (繼承 `base.html`)：新增書籍表單。
4. **`edit.html`** (繼承 `base.html`)：編輯書籍表單。
5. **`detail.html`** (繼承 `base.html`)：單一書籍詳細閱讀頁面。

## 4. 路由骨架程式碼

路由骨架已建立於 `app/routes/book_routes.py`。
