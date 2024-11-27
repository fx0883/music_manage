from django.db import models
import os
import time
import random
import string
from django.utils.html import mark_safe
from django.db.models.signals import pre_delete
from django.dispatch import receiver
import logging

logger = logging.getLogger(__name__)

def font_file_path(instance, filename):
    # 获取文件扩展名
    ext = filename.split('.')[-1]
    
    # 生成时间戳
    timestamp = time.strftime('%Y%m%d%H%M%S')
    
    # 生成6位随机字符串
    random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    
    # 构建新的文件名
    new_filename = f"{instance.code}_{timestamp}_{random_str}.{ext}"
    
    # 将文件保存到对应分类的目录下
    return os.path.join('fonts', instance.category.code, new_filename)

def font_preview_path(instance, filename):
    # 获取文件扩展名
    ext = filename.split('.')[-1]
    
    # 生成时间戳
    timestamp = time.strftime('%Y%m%d%H%M%S')
    
    # 生成6位随机字符串
    random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    
    # 构建新的文件名
    new_filename = f"{instance.code}_preview_{timestamp}_{random_str}.{ext}"
    
    # 将预览图片保存到对应分类的preview子目录下
    return os.path.join('fonts', instance.category.code, 'previews', new_filename)

class FontInfo(models.Model):
    """字体详情模型"""
    category = models.ForeignKey(
        'FontCategory', 
        on_delete=models.CASCADE, 
        related_name='fonts',
        verbose_name='字体分类'
    )
    name = models.CharField('字体名称', max_length=100)
    code = models.CharField('字体代码', max_length=50, unique=True)
    file = models.FileField('字体文件', upload_to=font_file_path)
    preview_image = models.ImageField(
        '字体预览图', 
        upload_to=font_preview_path,
        help_text='建议上传包含常用汉字的预览图片',
        blank=True,
        null=True
    )
    description = models.TextField('字体说明', blank=True)
    is_active = models.BooleanField('是否启用', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '字体'
        verbose_name_plural = '字体'
        ordering = ['category', 'code']

    def __str__(self):
        return f"{self.category.name} - {self.name}"

    def file_preview(self):
        """用于在管理界面显示文件链接"""
        if self.file:
            return f'<a href="{self.file.url}" target="_blank">{self.file.name}</a>'
        return '无文件'
    file_preview.short_description = '文件预览'
    file_preview.allow_tags = True

    def preview_image_tag(self):
        """用于在管理界面显示预览图片"""
        if self.preview_image:
            return mark_safe(
                f'<img src="{self.preview_image.url}" width="400" style="max-width:100%;" />'
            )
        return '无预览图'
    preview_image_tag.short_description = '预览图'

@receiver(pre_delete, sender=FontInfo)
def delete_font_files(sender, instance, **kwargs):
    """在删除字体记录时同时删除字体文件和预览图"""
    try:
        # 删除字体文件
        if instance.file:
            try:
                instance.file.delete(save=False)
            except Exception as e:
                logger.error(f"Error deleting font file: {str(e)}")

        # 删除预览图
        if instance.preview_image:
            try:
                instance.preview_image.delete(save=False)
            except Exception as e:
                logger.error(f"Error deleting preview image: {str(e)}")

    except Exception as e:
        logger.error(f"Error in delete_font_files: {str(e)}")