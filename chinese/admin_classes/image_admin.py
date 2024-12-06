from django.contrib import admin
from django.utils.html import format_html
from ..models.image_category import ImageCategory
from ..models.image_info import ImageInfo

class ImageCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'description', 'created_at']
    search_fields = ['name', 'code']
    ordering = ['code']

class ImageInfoAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'image_preview', 'thumbnail_preview', 'is_active', 'created_at']
    list_filter = ['category', 'is_active']
    search_fields = ['title', 'description']
    ordering = ['-created_at']
    readonly_fields = ['image_preview_detail', 'thumbnail_preview_detail']
    
    def image_preview(self, obj):
        """在列表页显示图片预览"""
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover;" />',
                obj.image.url
            )
        return "无图片"
    image_preview.short_description = '原图预览'

    def thumbnail_preview(self, obj):
        """在列表页显示缩略图预览"""
        if obj.thumbnail:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover;" />',
                obj.thumbnail.url
            )
        return "无缩略图"
    thumbnail_preview.short_description = '缩略图预览'

    def image_preview_detail(self, obj):
        """在详情页显示原图大图预览"""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 400px; max-height: 400px;" />',
                obj.image.url
            )
        return "无图片"
    image_preview_detail.short_description = '原图预览'

    def thumbnail_preview_detail(self, obj):
        """在详情页显示缩略图大图预览"""
        if obj.thumbnail:
            return format_html(
                '<img src="{}" style="max-width: 150px; max-height: 150px;" />',
                obj.thumbnail.url
            )
        return "无缩略图"
    thumbnail_preview_detail.short_description = '缩略图预览'

    fieldsets = (
        ('基本信息', {
            'fields': ('title', 'category', 'description', 'is_active')
        }),
        ('图片', {
            'fields': ('image', 'image_preview_detail')
        }),
        ('缩略图', {
            'fields': ('thumbnail_preview_detail',)
        })
    )

    class Media:
        js = (
            'admin/js/jquery.init.js',
            'js/image_auto_title.js',
        )
