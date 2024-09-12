# 使用 Python 3.11 作为基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 安装 MySQL client 和构建依赖
RUN apt-get update && apt-get install -y \
    build-essential \
    pkg-config \
    default-libmysqlclient-dev \
    gcc \
    libssl-dev \
    libffi-dev \
    libmariadb-dev

# 复制项目文件到容器中
COPY . /app/

# 升级 pip
RUN pip install --upgrade pip

# 安装项目依赖
RUN pip install --no-cache-dir -r requirements.txt

# 暴露端口
EXPOSE 8000

# 启动 Django 服务器
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
