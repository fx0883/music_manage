# # your_app/admin.py
#
# import os
# import importlib
# from django.contrib import admin
# from django.apps import apps
#
# # 动态遍历并注册所有 admin_classes 文件夹中的 ModelAdmin 类
# admin_classes_dir = os.path.join(os.path.dirname(__file__), 'admin_classes')
#
# for filename in os.listdir(admin_classes_dir):
#     if filename.endswith('.py') and not filename.startswith('__'):
#         module_name = f'music.admin_classes.{filename[:-3]}'  # 去掉 .py 扩展名
#         module = importlib.import_module(module_name)
#
#         for attr_name in dir(module):
#             attr = getattr(module, attr_name)
#             if isinstance(attr, type) and issubclass(attr, admin.ModelAdmin):
#                 # 确定与 ModelAdmin 相关的模型
#                 model_name = attr.model._meta.model_name
#                 model = apps.get_model('music', model_name)
#                 admin.site.register(model, attr)
from django.contrib import admin

# Register your models here.



# yourapp/admin.py
from django.contrib import admin
import os
from importlib import import_module

# 获取当前目录路径
current_dir = os.path.dirname(os.path.abspath(__file__))
admin_classes_dir = os.path.join(current_dir, 'admin_classes')

# 获取admin_classes目录下的所有.py文件（不包括__init__.py）
files = [f[:-3] for f in os.listdir(admin_classes_dir) if f.endswith('.py') and f != '__init__.py']

# 动态导入每个.py文件作为模块，并注册Admin类
for file in files:
    module_path = f"music.admin_classes.{file}"
    try:
        imported_module = import_module(module_path)
        # 获取模块中的Admin类，并注册到admin.site
        for name in getattr(imported_module, '__all__', []):
            try:
                admin_class = getattr(imported_module, name)
                if issubclass(admin_class, admin.ModelAdmin):
                    model = admin_class.Meta.model
                    admin.site.register(model, admin_class)
            except Exception as e:
                print(f"Failed to import {module_path}: {e}")
    except Exception as e:
        print(f"Failed to import {module_path}: {e}")

# 输出注册的信息，以供调试
print("Registered Admin Classes:")
for model, admin_class in admin.site._registry.items():
    print(f"{model}: {admin_class}")
