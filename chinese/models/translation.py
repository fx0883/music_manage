from django.db import models
from .poem import Poem
from .language import Language

class Translation(models.Model):
    """翻译模型"""
    poem = models.ForeignKey(Poem, on_delete=models.CASCADE, related_name='translations')
    language = models.ForeignKey(Language, on_delete=models.CASCADE, verbose_name='语言')
    content = models.TextField('翻译内容')

    class Meta:
        verbose_name = '翻译'
        verbose_name_plural = '翻译'
        unique_together = ['poem', 'language']  # 确保每个诗词在每种语言下只有一个翻译 