from django.contrib import admin
from chinese.models import PoemGenre

class PoemGenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'created_at', 'updated_at')
    search_fields = ('name', 'code')
    list_filter = ('created_at', 'updated_at')
    ordering = ('code',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'code')
        }),
        ('详细说明', {
            'fields': ('description',)
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    ) 