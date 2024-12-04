from django.contrib import admin
from django.utils.html import format_html
from ..models.image_category import ImageCategory
from ..models.image_info import ImageInfo

class ImageCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'description', 'created_at']
    search_fields = ['name', 'code']
    ordering = ['code']

class ImageInfoAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'image_preview', 'is_active', 'created_at']
    list_filter = ['category', 'is_active']
    search_fields = ['title', 'description']
    ordering = ['-created_at']
    readonly_fields = ['image_preview_detail']
    
    def image_preview(self, obj):
        """在列表页显示图片预览"""
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover;" />',
                obj.image.url
            )
        return "无图片"
    image_preview.short_description = '图片预览'

    def image_preview_detail(self, obj):
        """在详情页显示大图预览"""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 400px; max-height: 400px;" />',
                obj.image.url
            )
        return "无图片"
    image_preview_detail.short_description = '图片预览'

    class Media:

        js = (
            'admin/js/jquery.init.js',  # 确保 jQuery 正确初始化
            'js/image_auto_title.js',
        )
