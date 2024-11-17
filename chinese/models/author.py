from django.db import models
from .language import Language

class Author(models.Model):
    """诗词作者模型"""
    name = models.CharField('作者姓名', max_length=100)
    name_pinyin = models.CharField('作者拼音', max_length=100, blank=True)
    image = models.ImageField('作者图片', upload_to='authors/', blank=True, null=True)

    class Meta:
        verbose_name = '作者'
        verbose_name_plural = '作者'

    def __str__(self):
        return self.name

class AuthorIntroduction(models.Model):
    """作者介绍的多语言模型"""
    author = models.ForeignKey(
        Author, 
        on_delete=models.CASCADE, 
        related_name='introductions',
        verbose_name='作者'
    )
    language = models.ForeignKey(
        Language, 
        on_delete=models.CASCADE,
        verbose_name='语言'
    )
    content = models.TextField('作者介绍')

    class Meta:
        verbose_name = '作者介绍'
        verbose_name_plural = '作者介绍'
        unique_together = ['author', 'language']  # 确保每个作者在每种语言下只有一个介绍

    def __str__(self):
        return f"{self.author.name} - {self.language.name}介绍" 