from django.db import models
from .language import Language
import os
from pypinyin import pinyin, Style
from django.conf import settings
import random
import string

def generate_random_string(length=6):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def author_image_path(instance, filename):
    # 获取文件扩展名
    ext = filename.split('.')[-1]
    
    # 使用 pypinyin 转换名称为拼音
    name_pinyin = ''.join([item[0] for item in pinyin(instance.name, style=Style.NORMAL)])
    
    # 生成基础文件名
    base_filename = f"{name_pinyin}_{generate_random_string()}.{ext}"
    
    # 检查文件是否已存在，如果存在则重新生成
    full_path = os.path.join('authors/avatars', base_filename)
    while os.path.exists(os.path.join(settings.MEDIA_ROOT, full_path)):
        base_filename = f"{name_pinyin}_{generate_random_string()}.{ext}"
        full_path = os.path.join('authors/avatars', base_filename)
    
    return f'authors/avatars/{base_filename}'

class Author(models.Model):
    """诗词作者模型"""
    name = models.CharField('作者姓名', max_length=100)
    name_pinyin = models.CharField('作者拼音', max_length=100, blank=True)
    image = models.ImageField(upload_to=author_image_path, null=True, blank=True)

    class Meta:
        verbose_name = '作者'
        verbose_name_plural = '作者'

    def __str__(self):
        return self.name

class AuthorIntroduction(models.Model):
    """作者介绍的多语言模型"""
    author = models.ForeignKey(
        Author, 
        on_delete=models.CASCADE, 
        related_name='introductions',
        verbose_name='作者'
    )
    language = models.ForeignKey(
        Language, 
        on_delete=models.CASCADE,
        verbose_name='语言'
    )
    content = models.TextField('作者介绍')

    class Meta:
        verbose_name = '作者介绍'
        verbose_name_plural = '作者介绍'
        unique_together = ['author', 'language']  # 确保每个作者在每种语言下只有一个介绍

    def __str__(self):
        return f"{self.author.name} - {self.language.name}介绍" 