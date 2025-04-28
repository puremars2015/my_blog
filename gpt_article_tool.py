from gpt_helper import MyGPT
from sqlitetool import SQLiteTool
import time


# 使用chatgpt生成文章
def generate_article():
    gpt = MyGPT()
    title = gpt.AskGPT("請幫我想一個標題,主要跟越南各地文化與風景有關,且是繁體中文的標題")
    img_url = gpt.make_image(title)

    # 用時間產生檔案名稱
    file_name = time.strftime("%Y%m%d%H%M%S")

    gpt.download_image(img_url, 'images/' + file_name)
    content = gpt.AskGPT(f'請幫我依據這個標題"{title}"寫一篇文章,約500字,且是繁體中文的文章')
    return title, content, file_name

def save_article(title, content, img_url=None):

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
            content TEXT NOT NULL,
            img_url TEXT NULL
        );
        """
        db.execute_query(create_table_query)

    db.execute_query("INSERT INTO articles (title, content, img_url) VALUES (?, ?, ?)", (title, content, img_url))

    db.close_connection()

    return "article created"

if __name__ == "__main__":
    # 連續產生5篇文章
    for i in range(1):
        title, content, file_name = generate_article()
        print(title)
        print(content)
        save_article(title, content, file_name  + ".png")

        print("文章已儲存")