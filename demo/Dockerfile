# 使用 Pythonn 3.9 作為 Base Image
FROM python:3.9-slim

# 設定工作目錄為 /app
WORKDIR /app

# 將本地目錄中的檔案複製到容器的 /app 目錄中
COPY . /app

# 安裝相依套件
RUN pip install fastapi uvicorn

# 指定執行的命令
CMD ["uvicorn", "hello_world:app", "--host", "0.0.0.0", "--port", "8080"]
