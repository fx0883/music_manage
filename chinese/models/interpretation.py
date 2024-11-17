from django.db import models
from .poem import Poem
from .language import Language

class Interpretation(models.Model):
    """诗词译文模型"""
    poem = models.ForeignKey(
        Poem, 
        on_delete=models.CASCADE,
        related_name='interpretations',
        verbose_name='诗词'
    )
    language = models.ForeignKey(
        Language, 
        on_delete=models.CASCADE,
        verbose_name='语言'
    )
    content = models.TextField('译文内容')
    title_translation = models.CharField('标题译文', max_length=1000, blank=True)

    class Meta:
        verbose_name = '译文'
        verbose_name_plural = '译文'
        unique_together = ['poem', 'language']

    def __str__(self):
        return f"{self.poem.title} - {self.language.name}译文"