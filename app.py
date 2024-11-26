import random
from flask import Flask, jsonify, redirect, render_template, request, session, url_for
from openai import OpenAI

from sqlitetool import SQLiteTool

app = Flask(__name__)


#favicon.ico
@app.route('/favicon.ico')
def favicon():
    return redirect(url_for('static', filename='favicon.ico'))

# 首頁路由
@app.route('/')
def index():
    articles = [
        {
            "image": "B0B0B0.png",
            "title": "測試1標題",
            "description": "測試1描述",
            "link": "#",
            "link_color": "purple"
        },
        {
            "image": "ADD8E6.png",
            "title": "測試2標題",
            "description": "測試2描述",
            "link": "#",
            "link_color": "blue"
        },
        {
            "image": "E6E6FA.png",
            "title": "測試3標題",
            "description": "測試3s描述",
            "link": "#",
            "link_color": "pink"
        }
    ]

    # 在渲染模板時傳遞數據
    return render_template("index.html", articles=articles)

# 編輯頁面路由
@app.route('/edit_article')
def edit_article():
    return render_template('edit_article.html')

# 讀取文章內容
@app.route('/read_article')
def read_article():
    return render_template('read_article.html')

# 讀取文章內容
@app.route('/list_article')
def list_article():
    return render_template('list_article.html')


# api 新增文章
@app.route('/api/create', methods=['POST'])
def create():
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    if not title or not content:
        return jsonify({'error': 'missing title or content'}), 400

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
            content TEXT NOT NULL
        );
        """
        db.execute_query(create_table_query)

    db.execute_query("INSERT INTO articles (title, content) VALUES (?, ?)", (title, content))

    db.close_connection()

    return jsonify({'message': 'article created'}), 201

# api 取得文章列表
@app.route('/api/articles', methods=['GET'])
def readlist():
    db = SQLiteTool("my_blog.db")
    articles = db.execute_read_query("SELECT id,content FROM articles")
    db.close_connection()

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

if __name__ == '__main__':
    app.run(debug=True)