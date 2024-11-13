from django.db import models

class Language(models.Model):
    """支持的语言模型"""
    code = models.CharField('语言代码', max_length=10, unique=True)
    name = models.CharField('语言名称', max_length=50)
    is_active = models.BooleanField('是否启用', default=True)

    class Meta:
        verbose_name = '支持语言'
        verbose_name_plural = '支持语言'

    def __str__(self):
        return f"{self.name} ({self.code})"