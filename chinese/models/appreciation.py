from django.db import models
from .poem import Poem
from .language import Language

class Appreciation(models.Model):
    """赏析模型"""
    poem = models.ForeignKey(Poem, on_delete=models.CASCADE, related_name='appreciations')
    language = models.ForeignKey(Language, on_delete=models.CASCADE, verbose_name='语言')
    content = models.TextField('赏析内容')

    class Meta:
        verbose_name = '赏析'
        verbose_name_plural = '赏析'
        unique_together = ['poem', 'language']  # 确保每个诗词在每种语言下只有一个赏析