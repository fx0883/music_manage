from django.db import models

class Config(models.Model):
    name = models.CharField(max_length=100, unique=True)  # 配置项的名称
    value = models.JSONField()  # 配置项的值，使用 JSON 存储
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
