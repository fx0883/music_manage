import os
import time
import datetime
from django.db import models
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.conf import settings
from PIL import Image
import logging
from .image_category import ImageCategory

logger = logging.getLogger(__name__)

def image_upload_path(instance, filename):
    """
    生成图片上传路径
    格式: images/{category_code}/{filename的拼音}_{timestamp}_{filename}
    """
    # 获取文件扩展名
    ext = filename.split('.')[-1]
    
    # 生成时间戳,精确到微秒
    now = datetime.datetime.now()
    timestamp = now.strftime('%Y%m%d%H%M%S') + str(now.microsecond)[:3]
    
    # 获取文件名(不含扩展名)
    name_without_ext = os.path.splitext(filename)[0]
    
    # 如果文件名包含中文,则需要转换为拼音
    if any('\u4e00' <= char <= '\u9fff' for char in name_without_ext):
        from pypinyin import lazy_pinyin
        pinyin_name = '_'.join(lazy_pinyin(name_without_ext))
        new_filename = f"{pinyin_name}_{timestamp}.{ext}"
    else:
        # 英文文件名不做转换
        new_filename = f"{name_without_ext}_{timestamp}.{ext}"
        
    # 返回完整的上传路径
    return os.path.join('images', instance.category.code, new_filename)

def thumbnail_upload_path(instance, filename):
    """
    生成缩略图上传路径
    在原始图片路径前加上 small_ 前缀
    """
    if not filename:
        return None
    
    path = image_upload_path(instance, filename)
    directory = os.path.dirname(path)
    filename = os.path.basename(path)
    return os.path.join(directory, f'small_{filename}')

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
    thumbnail = models.ImageField(
        '缩略图',
        upload_to=thumbnail_upload_path,
        blank=True,
        null=True,
        editable=False  # 不在管理界面显示此字段
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

    def create_thumbnail(self):
        """创建缩略图"""
        if not self.image:
            return

        try:
            # 打开原始图片
            image = Image.open(self.image)
            
            # 计算缩略图尺寸，保持宽高比
            max_size = (150, 150)  # 设置缩略图最大尺寸
            image.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # 准备缩略图文件路径
            thumbnail_name = os.path.basename(self.image.name)
            thumbnail_path = thumbnail_upload_path(self, thumbnail_name)
            full_path = os.path.join(settings.MEDIA_ROOT, thumbnail_path)
            
            # 确保目录存在
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            # 保存缩略图
            image.save(full_path, quality=85, optimize=True)
            
            # 更新模型的缩略图字段
            self.thumbnail.name = thumbnail_path
            
        except Exception as e:
            logger.error(f"Error creating thumbnail for {self.image.name}: {str(e)}")

@receiver(pre_save, sender=ImageInfo)
def create_thumbnail_on_save(sender, instance, **kwargs):
    """保存图片时自动创建缩略图"""
    if instance.image and not instance.thumbnail:
        instance.create_thumbnail()

@receiver(pre_delete, sender=ImageInfo)
def delete_image_files(sender, instance, **kwargs):
    """在删除图片记录时同时删除图片文件和缩略图"""
    try:
        # 删除原始图片
        if instance.image:
            image_path = os.path.join(settings.MEDIA_ROOT, str(instance.image))
            if os.path.exists(image_path):
                try:
                    os.remove(image_path)
                    logger.info(f"Successfully deleted image file: {image_path}")
                except Exception as e:
                    logger.error(f"Error deleting image file {image_path}: {str(e)}")
            
        # 删除缩略图
        if instance.thumbnail:
            thumbnail_path = os.path.join(settings.MEDIA_ROOT, str(instance.thumbnail))
            if os.path.exists(thumbnail_path):
                try:
                    os.remove(thumbnail_path)
                    logger.info(f"Successfully deleted thumbnail file: {thumbnail_path}")
                except Exception as e:
                    logger.error(f"Error deleting thumbnail file {thumbnail_path}: {str(e)}")
                    
        # 检查并删除空目录
        directory = os.path.dirname(image_path)
        if not os.listdir(directory):
            os.rmdir(directory)
            logger.info(f"Removed empty directory: {directory}")
            
    except Exception as e:
        logger.error(f"Error in delete_image_files: {str(e)}") 