from django.db import models

class Author(models.Model):
    """诗词作者模型"""
    name = models.CharField('作者姓名', max_length=100)
    introduction = models.TextField('作者简介', blank=True)
    image = models.ImageField('作者图片', upload_to='authors/', blank=True, null=True)

    class Meta:
        verbose_name = '作者'
        verbose_name_plural = '作者'

    def __str__(self):
        return self.name 