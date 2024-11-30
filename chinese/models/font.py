from django.db import models
import os
import time
import random
import string

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

class Font(models.Model):
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