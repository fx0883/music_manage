import json
import os
import requests
import time
from pathlib import Path
from django.core.management.base import BaseCommand
from django.conf import settings
from chinese.models import Author
from urllib.parse import urljoin
import logging

class Command(BaseCommand):
    help = '从JSON文件更新唐代作者的图片信息'

    def add_arguments(self, parser):
        parser.add_argument('--json-file', type=str, default='doc/authors.json', help='作者JSON文件路径')
        parser.add_argument('--base-url', type=str, default='https://abc/', help='图片基础URL')
        parser.add_argument('--image-dir', type=str, default='media/authors/avatars', help='图片保存目录')

    def get_ip_info(self):
        """获取当前IP信息"""
        try:
            response = requests.get('https://api.ipify.org?format=json', timeout=5)
            if response.status_code == 200:
                public_ip = response.json()['ip']
                
                # 获取IP详细信息
                detail_response = requests.get(f'https://ipapi.co/{public_ip}/json/', timeout=5)
                if detail_response.status_code == 200:
                    ip_info = detail_response.json()
                    return {
                        'ip': public_ip,
                        'city': ip_info.get('city', 'Unknown'),
                        'region': ip_info.get('region', 'Unknown'),
                        'country': ip_info.get('country_name', 'Unknown')
                    }
            return {'ip': public_ip, 'city': 'Unknown', 'region': 'Unknown', 'country': 'Unknown'}
        except Exception as e:
            logging.error(f'获取IP信息失败: {str(e)}')
            return None

    def setup_logging(self):
        # 设置日志
        log_dir = 'logs'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        logging.basicConfig(
            filename=os.path.join(log_dir, 'update_author_images.log'),
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def ensure_directory(self, directory):
        """确保目录存在"""
        if not os.path.exists(directory):
            os.makedirs(directory)
            self.stdout.write(f'Created directory: {directory}')

    def download_image(self, url, save_path):
        """下载图片"""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            with open(save_path, 'wb') as f:
                f.write(response.content)
            return True
        except Exception as e:
            logging.error(f'下载图片失败 {url}: {str(e)}')
            return False

    def handle(self, *args, **options):
        self.setup_logging()
        
        # 获取并显示IP信息
        ip_info = self.get_ip_info()
        if ip_info:
            self.stdout.write(
                self.style.SUCCESS(
                    f"\n当前IP信息:\n"
                    f"IP: {ip_info['ip']}\n"
                    f"城市: {ip_info['city']}\n"
                    f"地区: {ip_info['region']}\n"
                    f"国家: {ip_info['country']}\n"
                )
            )
            logging.info(f"当前IP信息: {ip_info}")
        else:
            self.stdout.write(self.style.WARNING('无法获取IP信息'))
            
        # 确保图片保存目录存在
        image_dir = options['image_dir']
        self.ensure_directory(image_dir)

        try:
            # 读取JSON文件
            with open(options['json_file'], 'r', encoding='utf-8') as f:
                data = json.load(f)

            # 查找唐代部分
            tang_section = next(
                (section for section in data if section['sectionName'] == '唐代'),
                None
            )

            if not tang_section:
                self.stderr.write('未找到唐代数据')
                logging.error('未找到唐代数据')
                return

            success_count = 0
            error_count = 0
            base_url = options['base_url']

            # 处理每个作者
            for author_data in tang_section['datas']:
                break
                try:
                    name = author_data['nameStr']
                    pic_url = author_data['picSmallUrl']
                    
                    # 构建完整的图片URL和保存路径
                    full_url = urljoin(base_url, pic_url)
                    image_filename = os.path.basename(pic_url)
                    save_path = os.path.join(image_dir, image_filename)

                    # 下载图片
                    if self.download_image(full_url, save_path):
                        # 更新数据库
                        author = Author.objects.filter(name=name).first()
                        if author:
                            # 使用新的相对路径格式
                            relative_path = f'authors/avatars/{image_filename}'
                            author.image = relative_path
                            author.save()
                            success_count += 1
                            self.stdout.write(
                                self.style.SUCCESS(f'成功更新作者图片: {name}')
                            )
                            logging.info(f'成功更新作者图片: {name}')
                        else:
                            error_count += 1
                            self.stderr.write(f'作者不存在: {name}')
                            logging.error(f'作者不存在: {name}')
                    else:
                        error_count += 1
                        self.stderr.write(f'下载图片失败: {name}')

                    # 每次下载后休息3秒
                    self.stdout.write(f'休息3秒后继续...')
                    time.sleep(3)

                except Exception as e:
                    error_count += 1
                    error_msg = f'处理作者失败 {name if "name" in locals() else "unknown"}: {str(e)}'
                    self.stderr.write(self.style.ERROR(error_msg))
                    logging.error(error_msg)
                

            # 输出统计信息
            self.stdout.write("\n更新统计:")
            self.stdout.write(f"成功: {success_count}")
            self.stdout.write(f"失败: {error_count}")
            logging.info(f"更新完成 - 成功: {success_count}, 失败: {error_count}")

        except Exception as e:
            self.stderr.write(self.style.ERROR(f'执行失败: {str(e)}'))
            logging.error(f'执行失败: {str(e)}')
