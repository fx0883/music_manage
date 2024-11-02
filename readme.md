主要部署命令如下
gcloud compute ssh --project=upbeat-orb-435001-b1 --zone=us-central1-f instance-music

gcloud compute ssh --project=meta-matrix-440509-c3 --zone=us-central1-f instance-fsapp

gcloud compute ssh --zone "us-central1-a" "instance-fsapp" --project "meta-matrix-440509-c3"

http://35.223.168.206:8000/api/docs/#/music/music_local_recommend_songs_list

# 更新包列表
sudo apt-get update

# 安装Docker和Git
sudo apt-get install -y docker.io git

# 安装Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose


# 克隆项目代码
git clone https://github.com/fx0883/music_manage.git
cd music_manage

进入项目的目录

docker-compose down

docker system prune -a

git clone https://github.com/fx0883/music_manage.git

git pull origin master


sudo docker-compose up --build -d

35.188.0.156

http://35.188.0.156:8000/admin


docker exec -it django_app /bin/bash

docker exec -it django_app bash

python manage.py migrate

python manage.py createsuperuser

python manage.py makemigrations music

python manage.py migrate music




# 添加执行权限
chmod +x backup_db.sh

# 执行备份
./backup_db.sh

备份数据库
# 停止容器
docker-compose down

# 备份 mysql_data 目录
tar -czf backups/mysql_data_$(date +%Y%m%d_%H%M%S).tar.gz mysql_data/

# 重启容器
docker-compose up -d