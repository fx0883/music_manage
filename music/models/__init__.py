from .song import Song
from .site_config import SiteConfig
from .config import Config
from .genre_item import GenreItem

__all__ = ['Song', 'SiteConfig', 'Config', 'GenreItem']
#
#
# # music/models/__init__.py
#
# import os
# import importlib
#
# # 获取当前文件夹路径
# models_dir = os.path.dirname(__file__)
#
# # 初始化 __all__ 列表
# __all__ = []
#
# # 动态遍历当前目录下的所有 Python 文件
# for filename in os.listdir(models_dir):
#     # 排除 __init__.py 和非 .py 文件
#     if filename.endswith('.py') and not filename.startswith('__'):
#         module_name = filename[:-3]  # 去掉 .py 扩展名
#         module = importlib.import_module(f'.{module_name}', package=f'{__name__}')
#
#         # 获取模块中的所有属性，并将模型名称添加到 __all__ 中
#         for attr_name in dir(module):
#             attr = getattr(module, attr_name)
#             if isinstance(attr, type):
#                 __all__.append(attr_name)
#
# # 将 __all__ 列表转换为模块级别的全局变量
# globals().update(
#     {name: getattr(importlib.import_module(f'.{module_name}', package=f'{__name__}'), name) for name in __all__})
#
# print(__all__)

# import os
# import sys
# from importlib import import_module
#
# # 获取当前目录路径
# current_dir = os.path.dirname(os.path.abspath(__file__))
#
# # 获取当前目录下的所有.py文件（不包括__init__.py）
# files = [f[:-3] for f in os.listdir(current_dir) if f.endswith('.py') and f != '__init__.py']
#
# # 动态导入每个.py文件作为模块
# for file in files:
#     module_path = f"{__name__}.{file}"
#     # module_path = f"music.models.{file}"
#     try:
#         imported_module = import_module(module_path)
#         # 如果模块中有`__all__`属性，则将其中的类或变量名添加到当前模块的`__all__`列表中
#         if hasattr(imported_module, '__all__'):
#             for name in getattr(imported_module, '__all__'):
#                 globals()[name] = getattr(imported_module, name)
#     except ImportError as e:
#         print(f"Failed to import {module_path}: {e}", file=sys.stderr)
#
# # 设置__all__以允许从该模块导入指定的对象
# __all__ = [name for file in files for name in getattr(import_module(f"{__name__}.{file}"), '__all__', [])]
#
# print(__all__)



# yourapp/__init__.py
# import os
# from importlib import import_module
#
# # 获取当前目录路径
# current_dir = os.path.dirname(os.path.abspath(__file__))
#
# # 获取当前目录下的所有.py文件（不包括__init__.py）
# files = [f[:-3] for f in os.listdir(current_dir) if f.endswith('.py') and f != '__init__.py']
#
# __all__ = []
#
# for file in files:
#     module_path = f".{file}"
#     try:
#         imported_module = import_module(module_path, package=__name__)
#         # 将模块中的所有名字添加到当前模块的命名空间中
#         if hasattr(imported_module, '__all__'):
#             for name in imported_module.__all__:
#                 globals()[name] = getattr(imported_module, name)
#                 __all__.append(name)
#         else:
#             print(f"Warning: {module_path} does not define an __all__, skipping.")
#     except Exception as e:
#         print(f"Failed to import {module_path}: {e}")
#
# print(f"__all__: {__all__}")
