from django.db import models

class FontCategory(models.Model):
    """字体分类模型"""
    code = models.CharField('分类代码', max_length=50, unique=True)  # 如：kaishu
    name = models.CharField('分类名称', max_length=100)  # 如：楷书
    description = models.TextField('分类说明', blank=True)
    order = models.IntegerField('显示顺序', default=0)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '字体分类'
        verbose_name_plural = '字体分类'
        ordering = ['order', 'code']

    def __str__(self):
        return self.name 