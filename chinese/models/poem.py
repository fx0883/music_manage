from django.db import models
from .author import Author
from .poem_type import PoemType
from pypinyin import pinyin, Style
from django.utils.html import mark_safe
import time
import random
import string
import os

def poem_image_path(instance, filename):
    # 获取文件扩展名
    ext = filename.split('.')[-1]
    
    # 生成时间戳
    timestamp = time.strftime('%Y%m%d%H%M%S')
    
    # 生成6位随机字符串
    random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    
    # 获取拼音名称
    py_list = pinyin(instance.title, style=Style.NORMAL)
    pinyin_name = '_'.join([''.join(p) for p in py_list])
    
    # 构建新的文件名
    new_filename = f"{pinyin_name}_{timestamp}_{random_str}.{ext}"
    
    return os.path.join('poems/images', new_filename)

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
    image = models.ImageField('诗词配图', upload_to=poem_image_path, blank=True, null=True)

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

    def image_preview(self):
        """用于在管理界面显示图片预览"""
        if self.image:
            # 使用16:9的比例，设置宽度为320，高度为180
            return mark_safe(f'<img src="{self.image.url}" width="320" height="180" style="object-fit: cover;" />')
        return '无图片'
    image_preview.short_description = '图片预览'