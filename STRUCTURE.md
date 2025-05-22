# 專案架構說明

本專案為一個以 Flask 為基礎的部落格系統，支援文章管理、留言、圖片上傳與 AI 生成內容。主要結構如下：

## 1. 主要程式

- [`app.py`](src/app.py)：Flask 應用主程式，負責路由、API、前端頁面渲染與靜態檔案服務。
- [`gpt_article_tool.py`](src/gpt_article_tool.py)：利用 OpenAI GPT 生成文章與圖片，並儲存至資料庫。
- [`gpt_helper.py`](src/gpt_helper.py)：封裝與 OpenAI API 互動的功能，包含文字、圖片生成與輔助工具。
- [`sqlitetool.py`](src/sqlitetool.py)：SQLite 資料庫操作工具，提供查詢與資料存取功能。
- [`webp_to_ico.py`](src/webp_to_ico.py)：WebP 圖片轉 ICO 格式的小工具。

## 2. 配置與依賴

- [`config.py`](src/config.py)：儲存 OpenAI API 金鑰等設定。
- [`requirements.txt`](src/requirements.txt)：Python 套件依賴清單。
- [`Dockerfile`](src/Dockerfile)、[`docker-compose.yml`](src/docker-compose.yml)：容器化部署設定。

## 3. 靜態與模板資源

- `static/`：靜態檔案（如圖片、favicon）。
- `images/`：用戶上傳或 AI 生成的圖片。
- `templates/`：Flask Jinja2 HTML 模板（如首頁、文章列表、文章閱讀、關於、聯絡等頁面）。

## 4. 資料庫

- `my_blog.db`：SQLite 資料庫檔案，儲存文章與留言等資料。

## 5. 其他

- `.gitignore`、`.gitattributes`、`LICENSE`：版本控制與授權相關設定。

---

### 程式流程簡述

1. 使用者透過網頁介面（由 Flask 提供）瀏覽、發表或管理文章。
2. 文章與留言資料存於 SQLite 資料庫，透過 [`SQLiteTool`](src/sqlitetool.py) 操作。
3. 可利用 [`gpt_article_tool.py`](src/gpt_article_tool.py) 自動產生 AI 文章與圖片。
4. 所有靜態資源與上傳圖片由 Flask 路由或靜態目錄提供。
5. 支援 Docker 部署，方便快速上線。
