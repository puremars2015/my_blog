import os
import random
from flask import Flask, jsonify, redirect, render_template, request, send_from_directory, session, url_for
from flask_cors import CORS
from openai import OpenAI
# import config

from sqlitetool import SQLiteTool

app = Flask(__name__)
CORS(app)

## 在此處替換為你的 OpenAI API Key
# client = OpenAI(api_key=config.openai_api_key)

# 設定上傳目錄
UPLOAD_IMAGE_FOLDER = 'images'
os.makedirs(UPLOAD_IMAGE_FOLDER, exist_ok=True)
app.config['UPLOAD_IMAGE_FOLDER'] = UPLOAD_IMAGE_FOLDER


#favicon.ico
@app.route('/favicon.ico')
def favicon():
    return redirect(url_for('static', filename='favicon.ico'))
    
@app.route('/')
def index():

    # 從資料庫讀取文章列表 前六筆
    db = SQLiteTool("my_blog.db")
    articles = db.execute_read_query("SELECT id,title,content FROM articles ORDER BY id DESC")
    db.close_connection()

    if articles is None or len(articles) < 1:
        articles = [
            {
                "id": "1",
                "title": "no article",
                "content": "no article"
            },
                    {
                "id": "2",
                "title": "no article",
                "content": "no article"
            },
                    {
                "id": "3",
                "title": "no article",
                "content": "no article"
            }
        ]


    # articles轉型成為list,且只取前六筆
    articles = list(articles)[:6]

    # 將articles轉型為上面的形式
    articles = [
        {
            "image": "B0B0B0.png",
            "title": article["title"],
            # 把content當作description, 但要修改內容變成30個字以內
            "content": article["content"][:100] + "...",
            "link": "/read_article/" + str(article["id"]),
            "link_color": random.choice(["purple", "blue", "pink"])
        }
        for article in articles
    ]   

    # 在渲染模板時傳遞數據
    return render_template("index.html", articles=articles)

@app.route('/edit_article')
def edit_article():
    return render_template('edit_article.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/calculate')
def calculate():
    return render_template('calculate.html')

# 讀取文章內容
@app.route('/read_article/<int:id>')
def read_article(id):

    # 從資料庫讀取文章
    db = SQLiteTool("my_blog.db")
    article = db.execute_read_query("SELECT * FROM articles WHERE id=?", (id,))
    db.close_connection()

    return render_template('read_article.html', title=article[0]["title"], content=article[0]["content"])

# 讀取文章內容
@app.route('/list_article/<int:page>')
def list_article(page):

    # 從資料庫讀取文章列表 前三筆
    db = SQLiteTool("my_blog.db")
    articles = db.execute_read_query("SELECT id,title,content FROM articles ORDER BY id DESC")
    db.close_connection()


    if articles is None or len(articles) < 1:
        articles = [
            {
                "id": "1",
                "title": "no article",
                "content": "no article"
            },
                    {
                "id": "2",
                "title": "no article",
                "content": "no article"
            },
                    {
                "id": "3",
                "title": "no article",
                "content": "no article"
            }
        ]

    # 分頁數據
    current_page = page
    total_pages = int(len(articles)/10) if len(articles)%10 == 0 else int(len(articles)/10) + 1
    base_url = "/list_article"

    # 構造頁碼數據
    page_numbers = [
        {"number": i, "url": f"{base_url}/{i}", "current": (i == current_page)}
        for i in range(1, total_pages + 1)
    ]

    # 上一頁和下一頁的 URL
    prev_page_url = f"{base_url}/{current_page - 1}" if current_page > 1 else None
    next_page_url = f"{base_url}/{current_page + 1}" if current_page < total_pages else None

    # articles轉型成為list,且只取10筆
    articles = list(articles)[0+(page-1)*10:10+(page-1)*10]

    # 將articles轉型為上面的形式
    articles = [
        {
            "image": "B0B0B0.png",
            "title": article["title"],
            # 把content當作description, 但要修改內容變成100個字以內
            "description": article["content"][:100] + "...",
            "link": "/read_article/" + str(article["id"]),
            "link_color": random.choice(["purple", "blue", "pink"])
        }
        for article in articles
    ]

    
   
    return render_template('list_article.html', 
        articles=articles,
        page_numbers=page_numbers,
        prev_page_url=prev_page_url,
        next_page_url=next_page_url,)


# api 新增留言
@app.route('/api/new_message', methods=['POST'])
def submit_contact_message():
    # 從表單中提取資料
    title = request.json.get('title')
    content = request.json.get('content')
    
    # 確保資料完整
    if not title or not content:
        return jsonify({'status': 'error', 'message': '主旨與內容皆為必填'}), 400


    # 檢查是不是有messages table
    db = SQLiteTool("my_blog.db")
    check_table_query = """
    SELECT name FROM sqlite_master WHERE type='table' AND name='messages';
    """
    table = db.execute_read_query(check_table_query)

    if not table:
        create_table_query = """
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        );
        """
        db.execute_query(create_table_query)

    # 將資料寫入資料庫
    db.execute_query("INSERT INTO messages (title, content) VALUES (?, ?)", (title, content))
    db.close_connection()
    
    # 返回回應
    return jsonify({'message': 'message sended'}), 201

# api 新增文章
@app.route('/api/create', methods=['POST'])
def create():

    file = request.files['file']
    title = request.form['title']
    content = request.form['content']

    if file.filename == '':
        return jsonify({"error": "未選擇檔案"}), 400

    if not title or not content:
        return jsonify({'error': 'missing title or content'}), 400
    
    # 儲存圖片檔案
    file_path = os.path.join(app.config['UPLOAD_IMAGE_FOLDER'], file.filename)
    file.save(file_path)

    # 寫入資料庫
    db = SQLiteTool("my_blog.db")

    # 檢查是不是有article table
    check_table_query = """
    SELECT name FROM sqlite_master WHERE type='table' AND name='articles';
    """
    table = db.execute_read_query(check_table_query)

    if not table:
        create_table_query = """
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            img_url TEXT NULL
        );
        """
        db.execute_query(create_table_query)

    db.execute_query("INSERT INTO articles (title, content, img_url) VALUES (?, ?, ?)", (title, content, file_path))

    db.close_connection()

    return jsonify({'message': 'article created'}), 201

# api 取得文章列表
@app.route('/api/articles', methods=['GET'])
def readlist():
    # 從資料庫讀取文章列表 前六筆
    db = SQLiteTool("my_blog.db")
    articles = db.execute_read_query("SELECT id,title,content FROM articles ORDER BY id DESC")
    db.close_connection()

    
    if articles is None or len(articles) < 1:
        articles = [
            {
                "id": "1",
                "title": "no article",
                "content": "no article"
            },
                    {
                "id": "2",
                "title": "no article",
                "content": "no article"
            },
                    {
                "id": "3",
                "title": "no article",
                "content": "no article"
            }
        ]

    # 將articles轉型為上面的形式
    articles = [
        {
            "image": "B0B0B0.png",
            "title": article["title"],
            # 把content當作description, 但要修改內容變成30個字以內
            "content": article["content"][:100] + "...",
            "link": "/read_article/" + str(article["id"]),
            "link_color": random.choice(["purple", "blue", "pink"])
        }
        for article in articles
    ]   

    return jsonify({'articles': articles})

# api 取得文章
@app.route('/api/article/<int:id>', methods=['GET'])
def read(id):
    db = SQLiteTool("my_blog.db")
    article = db.execute_read_query("SELECT * FROM articles WHERE id=?", (id,))
    db.close_connection()

    if not article:
        return jsonify({'error': 'article not found'}), 404

    return jsonify({'article': article[0]})

# api 更新文章
@app.route('/api/update/<int:id>', methods=['PUT'])
def update(id):
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    if not title or not content:
        return jsonify({'error': 'missing title or content'}), 400

    db = SQLiteTool("my_blog.db")
    article = db.execute_read_query("SELECT * FROM articles WHERE id=?", (id,))
    if not article:
        return jsonify({'error': 'article not found'}), 404

    db.execute_query("UPDATE articles SET title=?, content=? WHERE id=?", (title, content, id))
    db.close_connection()

    return jsonify({'message': 'article updated'}), 200

# 路由：公開圖片目錄
@app.route('/api/images/<path:filename>', methods=['GET'])
def serve_file(filename):
    return send_from_directory(app.config['UPLOAD_IMAGE_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)