# 使用官方Python镜像
FROM python:3.9

# 设置工作目录
WORKDIR /app

# 复制项目的requirements文件到容器
COPY requirements.txt /app/

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件到容器
COPY . /app/

# 暴露端口
EXPOSE 8000

# 运行 Django 开发服务器
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
