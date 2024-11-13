from django.db import models
from .author import Author
from .poem_type import PoemType
from pypinyin import pinyin, Style

class Poem(models.Model):
    """古诗词模型"""
    title = models.CharField('标题', max_length=100)
    title_pinyin = models.CharField('标题拼音', max_length=200, blank=True)
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

    def save(self, *args, **kwargs):
        if self.title and not self.title_pinyin:
            py_list = pinyin(self.title, style=Style.NORMAL)
            self.title_pinyin = ' '.join([''.join(p) for p in py_list])
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title 