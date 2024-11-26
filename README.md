# 開始遊玩之前,請先閱讀以下說明


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
python generate_article.py
```


4. 使用前,請先補上config.py, 格式如下

```config.py
openai_api_key = "abcdefg..."

```
