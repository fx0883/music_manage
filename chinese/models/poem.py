from django.db import models
from .author import Author
from .poem_type import PoemType

class Poem(models.Model):
    """古诗词模型"""
    title = models.CharField('标题', max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='作者')
    content = models.TextField('原文')
    pinyin = models.TextField('拼音')
    background = models.TextField('创作背景', blank=True)
    poem_type = models.ForeignKey(PoemType, on_delete=models.SET_NULL, null=True, verbose_name='诗词类型')
    difficulty = models.IntegerField('难度等级', default=1, choices=[
        (1, 'easy'),
        (2, 'medium'),
        (3, 'hard')
    ])

    class Meta:
        verbose_name = '古诗词'
        verbose_name_plural = '古诗词'

    def __str__(self):
        return self.title 