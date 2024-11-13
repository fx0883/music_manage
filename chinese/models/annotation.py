from django.db import models
from .poem import Poem
from .language import Language

class Annotation(models.Model):
    """注释模型"""
    poem = models.ForeignKey(Poem, on_delete=models.CASCADE, related_name='annotations')
    language = models.ForeignKey(Language, on_delete=models.CASCADE, verbose_name='语言')
    content = models.TextField('注释内容')

    class Meta:
        verbose_name = '注释'
        verbose_name_plural = '注释'
        unique_together = ['poem', 'language']  # 确保每个诗词在每种语言下只有一个注释