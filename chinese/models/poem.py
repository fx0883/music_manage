from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.conf import settings
from .author import Author
from .poem_type import PoemType
from pypinyin import pinyin, Style
from django.utils.html import mark_safe
import time
import random
import string
import os
import logging

logger = logging.getLogger(__name__)

def poem_image_path(instance, filename):
    """
    生成图片上传路径
    格式: images/poem[_banner]/{pinyin_name}_{timestamp}_{random_str}.{ext}
    """
    # 获取文件扩展名
    ext = filename.split('.')[-1]
    
    # 生成时间戳
    timestamp = time.strftime('%Y%m%d%H%M%S')
    
    # 生成6位随机字符串
    random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    
    # 获取拼音名称
    py_list = pinyin(instance.title, style=Style.NORMAL)
    pinyin_name = '_'.join([''.join(p) for p in py_list])
    
    # 判断当前处理的是哪个字段
    current_field = None
    for field in instance._meta.fields:
        if isinstance(field, models.ImageField):
            value = getattr(instance, field.name)
            if value and value.name == filename:
                current_field = field.name
                break
    
    # 根据字段类型设置目录和前缀
    if current_field == 'banner_image':
        directory = 'images/poem_banner'
        prefix = 'banner_'
    else:
        directory = 'images/poem'
        prefix = ''
    
    # 构建新的文件名
    new_filename = f"{prefix}{pinyin_name}_{timestamp}_{random_str}.{ext}"
    
    # 确保目录存在
    full_path = os.path.join(settings.MEDIA_ROOT, directory)
    if not os.path.exists(full_path):
        os.makedirs(full_path)
    
    return os.path.join(directory, new_filename)

class Poem(models.Model):
    """古诗词模型"""
    title = models.CharField('标题', max_length=100)
    title_pinyin = models.CharField('标题拼音', max_length=200, blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='作者')
    content = models.TextField('原文')
    pinyin = models.TextField('拼音')
    background = models.TextField('创作背景', blank=True)
    excerpt = models.TextField('摘录', blank=True, help_text='诗词中的经典名句或精彩片段')
    poem_type = models.ForeignKey(PoemType, on_delete=models.SET_NULL, null=True, verbose_name='诗词类型')
    difficulty = models.IntegerField('难度等级', default=1, choices=[
        (1, 'easy'),
        (2, 'medium'),
        (3, 'hard')
    ])
    image = models.ImageField('诗词配图', upload_to=poem_image_path, blank=True, null=True)
    banner_image = models.ImageField(
        '横幅图片',
        upload_to=poem_image_path,
        blank=True,
        null=True,
        help_text='用于展示页面顶部的横幅图片，建议尺寸 1920x480'
    )

    class Meta:
        verbose_name = '古诗词'
        verbose_name_plural = '古诗词'

    def save(self, *args, **kwargs):
        # 在保存前记录当前处理的字段名
        if hasattr(self, '_current_field_name'):
            delattr(self, '_current_field_name')
        
        # 确定需要更新的字段
        update_fields = []
        if self.image:
            update_fields.append('image')
        if self.banner_image:
            update_fields.append('banner_image')
        if self.title and not self.title_pinyin:
            update_fields.append('title_pinyin')
        
        if update_fields:
            super().save(update_fields=update_fields, *args, **kwargs)
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def image_preview(self):
        """用于在管理界面显示图片预览"""
        if self.image:
            return mark_safe(
                '<img src="{}" width="50" height="50" style="object-fit: cover;" />'.format(
                    self.image.url
                )
            )
        return "无图片"
    image_preview.short_description = '图片预览'

    def banner_image_preview(self):
        """用于在管理界面显示横幅图片预览"""
        if self.banner_image:
            return mark_safe(
                '<img src="{}" width="120" height="50" style="object-fit: cover;" />'.format(
                    self.banner_image.url
                )
            )
        return "无横幅图片"
    banner_image_preview.short_description = '横幅图片预览'

@receiver(pre_delete, sender=Poem)
def delete_poem_files(sender, instance, **kwargs):
    """在删除诗词记录时同时删除相关的图片文件"""
    try:
        # 删除普通图片
        if instance.image:
            image_path = os.path.join(settings.MEDIA_ROOT, str(instance.image))
            if os.path.exists(image_path):
                try:
                    os.remove(image_path)
                    logger.info(f"Successfully deleted poem image: {image_path}")
                except Exception as e:
                    logger.error(f"Error deleting poem image {image_path}: {str(e)}")
            else:
                logger.warning(f"Poem image not found: {image_path}")

        # 删除横幅图片
        if instance.banner_image:
            banner_path = os.path.join(settings.MEDIA_ROOT, str(instance.banner_image))
            if os.path.exists(banner_path):
                try:
                    os.remove(banner_path)
                    logger.info(f"Successfully deleted banner image: {banner_path}")
                except Exception as e:
                    logger.error(f"Error deleting banner image {banner_path}: {str(e)}")
            else:
                logger.warning(f"Banner image not found: {banner_path}")

        # 检查并删除空的图片目录
        for directory in ['images/poem', 'images/poem_banner']:
            dir_path = os.path.join(settings.MEDIA_ROOT, directory)
            if os.path.exists(dir_path) and not os.listdir(dir_path):
                try:
                    os.rmdir(dir_path)
                    logger.info(f"Removed empty directory: {dir_path}")
                except Exception as e:
                    logger.error(f"Error removing directory {dir_path}: {str(e)}")

    except Exception as e:
        logger.error(f"Error in delete_poem_files: {str(e)}")