# 開始遊玩之前,請先閱讀以下說明

## 初次啟動

1. 第一次啟動,需要先在my_blog.db裡面產生table,為了有文章,需要先執行

```bash
python gpt_article_tool.py
```

2. 補上config.py, 格式如下

```config.py
openai_api_key = "abcdefg..."

```

## 普通啟動(非初次啟動)

1. 若有docker環境, 可以使用以下指令

```bash
docker-compose up --build   
```

2. 若沒有docker環境, 可以使用以下指令

```bash
pip install -r requirements.txt
python app.py
```

3. 如果文章不夠, 可以使用以下指令

```bash
python gpt_article_tool.py
```
