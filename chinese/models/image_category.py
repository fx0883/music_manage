from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class ImageCategory(models.Model):
    """图片分类模型"""
    name = models.CharField('分类名称', max_length=50)
    code = models.CharField('分类代码', max_length=20, unique=True)
    description = models.TextField('分类描述', blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '图片分类'
        verbose_name_plural = '图片分类'
        ordering = ['code']

    def __str__(self):
        return f"{self.name} ({self.code})"

    def clean(self):
        """验证code只能包含小写字母、数字和下划线"""
        if not self.code:
            self.code = slugify(self.name)
        if not all(c.isalnum() or c == '_' for c in self.code):
            raise ValidationError({'code': _('分类代码只能包含字母、数字和下划线')})
        self.code = self.code.lower() 