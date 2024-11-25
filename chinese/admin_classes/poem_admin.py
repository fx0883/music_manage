from django.contrib import admin
from django.utils.html import format_html
from chinese.models import Poem

class PoemAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'poem_type', 'difficulty', 'list_image_preview')
    search_fields = ('title', 'content')
    list_filter = ('difficulty', 'poem_type', 'author')
    raw_id_fields = ('author', 'poem_type')
    
    # 添加搜索字段以支持自动完成
    search_fields = ['title', 'title_pinyin']
    
    readonly_fields = ['image_preview']  # 在详情页显示预览
    
    def list_image_preview(self, obj):
        """列表页的图片预览"""
        if obj.image:
            # 使用16:9的比例，设置宽度为160，高度为90
            return format_html(
                '<img src="{}" width="160" height="90" style="object-fit: cover;" />', 
                obj.image.url
            )
        return '无图片'
    list_image_preview.short_description = '图片预览'

    fieldsets = (
        ('基本信息', {
            'fields': ('title', 'title_pinyin', 'author', 'poem_type', 'difficulty')
        }),
        ('内容', {
            'fields': ('content', 'pinyin', 'background')
        }),
        ('图片', {
            'fields': ('image', 'image_preview'),
        }),
    )
 