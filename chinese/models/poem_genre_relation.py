from django.db import models
from .poem import Poem
from .poem_genre import PoemGenre

class PoemGenreRelation(models.Model):
    """诗歌与体裁关系模型"""
    poem = models.ForeignKey(
        Poem, 
        on_delete=models.CASCADE, 
        related_name='genre_relations',
        verbose_name='诗歌'
    )
    genre = models.ForeignKey(
        PoemGenre, 
        on_delete=models.CASCADE,
        related_name='poem_relations',
        verbose_name='体裁'
    )
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '诗歌体裁关系'
        verbose_name_plural = '诗歌体裁关系'
        unique_together = ['poem', 'genre']  # 确保一首诗与一个体裁只能关联一次
        ordering = ['created_at']

    def __str__(self):
        return f"{self.poem.title} - {self.genre.name}" 