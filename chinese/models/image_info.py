import os
import time
from django.db import models
from .image_category import ImageCategory

def image_upload_path(instance, filename):
    """
    生成图片上传路径
    格式: images/{category_code}/{category_code}_{timestamp}_{filename}
    """
    # 获取文件扩展名
    ext = filename.split('.')[-1]
    # 生成时间戳
    timestamp = time.strftime('%Y%m%d%H%M%S')
    # 生成新的文件名
    new_filename = f"{instance.category.code}_{timestamp}.{ext}"
    # 返回完整的上传路径
    return os.path.join('images', instance.category.code, new_filename)

class ImageInfo(models.Model):
    """图片信息模型"""
    title = models.CharField('图片标题', max_length=100)
    category = models.ForeignKey(
        ImageCategory,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='所属分类'
    )
    image = models.ImageField(
        '图片文件',
        upload_to=image_upload_path,
        help_text='支持jpg、png、gif格式的图片'
    )
    description = models.TextField('图片描述', blank=True)
    is_active = models.BooleanField('是否启用', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '图片信息'
        verbose_name_plural = '图片信息'
        ordering = ['-created_at']

    def __str__(self):
        return self.title 