import os
import time
import datetime
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.conf import settings
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

@receiver(pre_delete, sender=ImageInfo)
def delete_image_files(sender, instance, **kwargs):
    """在删除图片记录时同时删除图片文件"""
    try:
        if instance.image:
            # 获取图片的完整路径
            image_path = os.path.join(settings.MEDIA_ROOT, str(instance.image))
            # 检查文件是否存在
            if os.path.exists(image_path):
                try:
                    # 删除文件
                    os.remove(image_path)
                    logger.info(f"Successfully deleted image file: {image_path}")
                    
                    # 检查并删除空目录
                    directory = os.path.dirname(image_path)
                    if not os.listdir(directory):
                        os.rmdir(directory)
                        logger.info(f"Removed empty directory: {directory}")
                except Exception as e:
                    logger.error(f"Error deleting image file {image_path}: {str(e)}")
            else:
                logger.warning(f"Image file not found: {image_path}")
    except Exception as e:
        logger.error(f"Error in delete_image_files: {str(e)}") 