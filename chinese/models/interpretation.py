from django.db import models
from .poem import Poem
from .language import Language

class Interpretation(models.Model):
    """译文模型"""
    poem = models.ForeignKey(Poem, on_delete=models.CASCADE, related_name='interpretations')
    language = models.ForeignKey(Language, on_delete=models.CASCADE, verbose_name='语言')
    content = models.TextField('译文内容')

    class Meta:
        verbose_name = '译文'
        verbose_name_plural = '译文'
        unique_together = ['poem', 'language']  # 确保每个诗词在每种语言下只有一个译文 