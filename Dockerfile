FROM python:3.12-slim

WORKDIR /app

# 拷贝依赖并安装
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 拷贝根目录的所有后端代码
COPY . .

EXPOSE 8000

# 启动后端，注意 host 必须是 0.0.0.0
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]