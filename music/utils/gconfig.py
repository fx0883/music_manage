# class GlobalConfig:
#     _instance = None
#     _config = {}
#
#     # 定义全局常量
#     DEFAULT_TIMEOUT = 300  # 以秒为单位的默认超时时间
#     MAX_RETRIES = 5  # 最大重试次数
#
#     def __new__(cls):
#         if cls._instance is None:
#             cls._instance = super(GlobalConfig, cls).__new__(cls)
#             cls.load_config()
#         return cls._instance
#
#     @classmethod
#     def load_config(cls):
#         from ..models import Config
#         configs = Config.objects.all()
#         for config in configs:
#             cls._config[config.name] = config.value
#
#     @classmethod
#     def get_config(cls, name, default=None):
#         return cls._config.get(name, default)
#
#     @classmethod
#     def get_default_timeout(cls):
#         return cls.DEFAULT_TIMEOUT


from django.core.cache import cache
from ..models import Config

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
        configs = Config.objects.all()
        for config in configs:
            cls._config[config.name] = config.value
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
