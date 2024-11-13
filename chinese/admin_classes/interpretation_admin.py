from django.contrib import admin
from chinese.models import Interpretation

class InterpretationAdmin(admin.ModelAdmin):
    list_display = ('poem', 'language', 'content_preview')
    search_fields = ('content',)
    list_filter = ('language',)
    raw_id_fields = ('poem', 'language')

    def content_preview(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    content_preview.short_description = '译文内容预览' 