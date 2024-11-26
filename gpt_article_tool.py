from gpt_helper import MyGPT
from sqlitetool import SQLiteTool


# 使用chatgpt生成文章
def generate_article():
    gpt = MyGPT()
    title = gpt.AskGPT("請幫我想一個標題,主要要跟python,人工智慧,還有財務工程有關,一個就好,且是繁體中文的標題")
    content = gpt.AskGPT(f'請幫我依據這個標題"{title}"寫一篇文章,約500字,且是繁體中文的文章')
    return title, content

def save_article(title, content):

    if not title or not content:
        raise Exception("title和content不能為空")

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

    return "article created"

if __name__ == "__main__":
    # 連續產生5篇文章
    for i in range(3):
        title, content = generate_article()
        print(title)
        print(content)
        save_article(title, content)
        print("文章已儲存")