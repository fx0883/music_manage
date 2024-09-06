from django.db import models


class SiteConfig(models.Model):
    key = models.CharField(max_length=255, unique=True, verbose_name="Key")
    value = models.JSONField(verbose_name="Value")  # 使用 JSONField 存储 JSON 数据

    def __str__(self):
        return self.key


# __all__ = ['SiteConfig']
