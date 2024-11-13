from django.contrib import admin
from django.apps import apps

# 确保应用配置已加载
app_config = apps.get_app_config('chinese')
if not admin.site._registry:  # 只在admin站点未注册任何模型时执行
    app_config.ready()
