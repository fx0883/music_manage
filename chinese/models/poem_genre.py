from django.db import models

class PoemGenre(models.Model):
    """诗歌体裁模型"""
    code = models.CharField('体裁代码', max_length=50, unique=True)  # 如：wu_yan_gu_shi
    name = models.CharField('体裁名称', max_length=100)  # 如：五言古诗
    description = models.TextField('体裁说明', blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '诗歌体裁'
        verbose_name_plural = '诗歌体裁'
        ordering = ['code']

    def __str__(self):
        return self.name 