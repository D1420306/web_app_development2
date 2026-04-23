# 流程圖設計 (Flowchart) - 讀書筆記本

本文件包含使用者操作系統時的「使用者流程圖」，以及系統內部元件互動的「系統序列圖」。

## 1. 使用者流程圖 (User Flow)

此流程圖展示了學生進入讀書筆記本後，可以進行的各項操作路徑。

```mermaid
flowchart LR
    Start([開啟讀書筆記本]) --> Home[首頁 - 書單與心得列表]
    Home --> Action{選擇操作}
    
    Action -->|新增紀錄| Add[進入新增頁面]
    Add --> FillAdd[填寫書名、心得、評分]
    FillAdd --> SubmitAdd([送出儲存])
    SubmitAdd --> Home
    
    Action -->|搜尋書籍| Search[輸入關鍵字搜尋]
    Search --> ViewList[檢視過濾後的列表]
    
    Action -->|點擊特定書籍| Detail[檢視單一書籍與心得詳細頁面]
    Detail --> DetailAction{對此書的操作}
    
    DetailAction -->|編輯| Edit[進入編輯頁面]
    Edit --> Modify[修改書名、心得或評分]
    Modify --> SubmitEdit([送出更新])
    SubmitEdit --> Detail
    
    DetailAction -->|刪除| Delete([確認刪除])
    Delete --> Home
    
    DetailAction -->|返回| Home
```

## 2. 系統序列圖 (Sequence Diagram)

此序列圖以「**新增讀書筆記**」為例，展示從前端瀏覽器到後端資料庫的完整互動流程。

```mermaid
sequenceDiagram
    actor Student as 學生 (User)
    participant Browser as 瀏覽器 (View)
    participant Flask as Flask 路由 (Controller)
    participant Model as 資料庫模型 (Model)
    participant DB as SQLite 資料庫
    
    Student->>Browser: 進入新增頁面，填寫書名、心得與評分
    Student->>Browser: 點擊「送出」
    Browser->>Flask: POST /books/add (包含表單資料)
    
    Flask->>Flask: 驗證資料 (如書名是否為空)
    Flask->>Model: 呼叫新增函數 (add_book)
    
    Model->>DB: INSERT INTO books (title, review, rating)
    DB-->>Model: 寫入成功
    Model-->>Flask: 回傳成功狀態
    
    Flask-->>Browser: 重導向 (Redirect) 至首頁 /
    Browser-->>Student: 顯示更新後的書單列表
```

## 3. 功能清單與路由對照表

以下為系統核心功能與預計對應的 URL 路徑及 HTTP 方法：

| 功能描述 | URL 路徑 | HTTP 方法 | 說明 |
| -------- | -------- | --------- | ---- |
| 首頁 / 書籍列表 | `/` 或 `/books` | GET | 顯示所有讀書筆記列表，支援透過 GET 參數搜尋 |
| 新增書籍表單頁面 | `/books/add` | GET | 顯示填寫新增書籍與心得的 HTML 表單 |
| 送出新增書籍資料 | `/books/add` | POST | 接收表單資料，寫入資料庫，並重導向至首頁 |
| 檢視書籍詳細頁面 | `/books/<id>` | GET | 根據書籍 ID 顯示該書的詳細內容與心得 |
| 編輯書籍表單頁面 | `/books/<id>/edit` | GET | 顯示包含舊有資料的編輯表單 |
| 送出編輯書籍資料 | `/books/<id>/edit`| POST | 接收修改後的資料，更新資料庫，並重導向至詳細頁面 |
| 刪除書籍紀錄 | `/books/<id>/delete`| POST | 從資料庫刪除指定書籍，並重導向至首頁 |

> 備註：為了安全性，刪除操作應使用 POST 方法而非單純的 GET 連結。
