from django.db import models
from .poem_type import PoemType
from .language import Language

class PoemTypeInterpretation(models.Model):
    """古诗词类型多语言解释模型"""
    poem_type = models.ForeignKey(PoemType, on_delete=models.CASCADE, related_name='interpretations')
    language = models.ForeignKey(Language, on_delete=models.CASCADE, verbose_name='语言')
    name = models.CharField('类型名称翻译', max_length=100)
    description = models.TextField('类型描述', blank=True)

    class Meta:
        verbose_name = '古诗词类型译文'
        verbose_name_plural = '古诗词类型译文'
        unique_together = ['poem_type', 'language']  # 确保每个类型在每种语言下只有一个译文

    def __str__(self):
        return f"{self.poem_type.name} ({self.language.name})" 