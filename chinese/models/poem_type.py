from django.db import models

class PoemType(models.Model):
    """古诗词类型模型"""
    code = models.CharField('类型代码', max_length=50, unique=True)  # 用于系统内部标识，如：shi_jing
    name = models.CharField('类型名称(中文)', max_length=100)  # 默认中文名称，如：诗经

    class Meta:
        verbose_name = '古诗词类型'
        verbose_name_plural = '古诗词类型'

    def __str__(self):
        return self.name 