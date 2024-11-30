from django.contrib import admin
from chinese.models import Font

class FontAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'code', 'is_active', 'created_at')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('name', 'code')
    raw_id_fields = ('category',)
    readonly_fields = ('file_preview',)
    
    fieldsets = (
        ('基本信息', {
            'fields': ('category', 'name', 'code', 'is_active')
        }),
        ('文件', {
            'fields': ('file', 'file_preview')
        }),
        ('其他信息', {
            'fields': ('description',)
        })
    ) 