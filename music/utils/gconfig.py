from django.core.cache import cache
from ..models import Config, SiteConfig
import re
import requests

class GlobalConfig:
    _instance = None
    _config = {}

    # 定义全局常量
    SOUNDCLOUD = 'soundCloud'  # 以秒为单位的默认超时时间
    MAX_RETRIES = 5  # 最大重试次数

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GlobalConfig, cls).__new__(cls)
            cls.load_config()
        return cls._instance

    @classmethod
    def load_config(cls):
        """加载配置，将其存储在缓存中"""
        # 加载 Config 表数据
        configs = Config.objects.all()
        for config in configs:
            cls._config[config.name] = config.value
        
        # 加载 SiteConfig 表数据
        site_configs = SiteConfig.objects.all()
        for site_config in site_configs:
            cls._config[f"site_{site_config.key}"] = site_config.value
        
        # 将所有配置存入缓存
        cache.set('global_config', cls._config)  # 缓存配置信息

    @classmethod
    def get_config(cls, name, default=None):
        """获取某个配置项的值"""
        config = cache.get('global_config', cls._config)  # 从缓存中获取配置
        return config.get(name, default)

    @classmethod
    def reload_config(cls):
        """重新加载配置，将其更新到缓存中"""
        cls._config = {}  # 清空当前的配置
        cls.load_config()  # 重新加载配置

    @classmethod
    def update_soundcloud_client_id(cls):
        """
        获取并更新 SoundCloud client_id 到 Config 表，保留其他现有配置
        """
        url = "https://a-v2.sndcdn.com/assets/0-400ac023.js"
        headers = {
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'origin': 'https://soundcloud.com',
            'priority': 'u=1, i',
            'referer': 'https://soundcloud.com/',
            'sec-ch-ua': '"Microsoft Edge";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0'
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            pattern = r'client_id=([a-zA-Z0-9]+)'
            match = re.search(pattern, response.text)
            
            if match:
                client_id = match.group(1)
                
                # 获取现有配置
                existing_config = Config.objects.filter(name=cls.SOUNDCLOUD).first()
                if existing_config:
                    # 如果配置存在，更新现有值中的 client_id
                    current_value = existing_config.value
                    current_value['client_id'] = client_id
                    existing_config.value = current_value
                    existing_config.save()
                else:
                    # 如果配置不存在，创建新配置
                    Config.objects.create(
                        name=cls.SOUNDCLOUD,
                        value={'client_id': client_id}
                    )
                
                # 更新缓存
                cache.delete('global_config')
                cls.reload_config()
                
                return client_id
            else:
                raise ValueError("No client_id found in response")
                
        except Exception as e:
            print(f"Error updating SoundCloud client_id: {str(e)}")
            return None



# "app_version":"1729507807",
# "app_locale":"en"
#
# {"client_id": "e5qtqnBx108ZVHabnxYWmtRiknqDLQ2W", "app_version":"1729507807", "app_locale": "en"}
# "app_locale": "en"}