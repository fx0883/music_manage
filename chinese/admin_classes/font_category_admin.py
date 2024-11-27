from django.contrib import admin
from chinese.models import FontCategory

class FontCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'order', 'created_at', 'updated_at')
    search_fields = ('name', 'code')
    list_filter = ('created_at', 'updated_at')
    ordering = ('order', 'code') 