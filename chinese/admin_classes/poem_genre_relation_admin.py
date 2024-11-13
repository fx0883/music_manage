from django.contrib import admin
from chinese.models import PoemGenreRelation

class PoemGenreRelationAdmin(admin.ModelAdmin):
    list_display = ('poem', 'genre', 'created_at')
    search_fields = ('poem__title', 'genre__name')
    list_filter = ('genre', 'created_at')
    raw_id_fields = ['poem', 'genre']
    readonly_fields = ('created_at',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('poem', 'genre') 