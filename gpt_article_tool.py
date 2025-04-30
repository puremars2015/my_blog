from gpt_helper import MyGPT
from sqlitetool import SQLiteTool
import time
import re


# 使用chatgpt生成文章
def generate_article():
    gpt = MyGPT()
    title = gpt.AskGPT("我想介紹一個越南景點,請幫我給我一個標題,要有趣,且是繁體中文的文章")
    img_url = gpt.make_image(title)

    # 用時間產生檔案名稱
    file_name = time.strftime("%Y%m%d%H%M%S")

    gpt.download_image(img_url, 'images/' + file_name)
    structure = gpt.AskGPT(f'請幫我依據這個標題"{title}"寫一個大綱,介紹1個景點,並深度的介紹這個景點5~10個特色,並且要有結論,內容要有趣,且是繁體中文的文章')

    article = gpt.AskGPT(f'請幫我依據這個大綱"{structure}"寫一篇文章,內容要有趣,且是繁體中文的文章')

    return title, article, file_name



def beautify_content(content):
    gpt = MyGPT()
    template = f'''
!!!請幫我將以下內文排版成 HTML 格式，只需要文章本體，不要包含<html>、<head>、<body>標籤，回覆的內文主體用<article></article>來標註。  

要求如下：  
- 幫每一個主題段落設定一個小標題（<h2>），小標題可以稍微美化一下用詞（但不要改變內文意思）  
- 內文用<p>標籤包起來，行距舒適，段落之間保留適當空白感  
- 使用 Tailwind CSS 樣式，排版現代感清爽、結構清晰  
- 整個內容用<section>包住，設定 max-width，置中顯示，白底、圓角、陰影效果  
- 文章主標題用<h1>，並加上底線或顏色區別  
- 內文文字顏色使用 text-gray-700，小標題使用 text-blue-600，主標題使用 text-pink-600  
- 每一個小節的間距適當（例如 mb-10）
- 如果有結論段落，也請給一個適合的小標題  

以下是內文：
{content}
'''
    
    content = gpt.AskGPT(template)

    # 擷取 <article> 與 </article> 之間的內容
    article_pattern = re.compile(r'<article>(.*?)</article>', re.DOTALL)
    match = article_pattern.search(content)
    if match:
        content = match.group(1).strip()

    return content 

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
        content = beautify_content(content)
        save_article(title, content, file_name  + ".png")

        print("文章已儲存")