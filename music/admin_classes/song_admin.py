from django.contrib import admin
from ..models import Song

# 注册 Song 模型到 admin
@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'album', 'genre', 'release_date', 'duration')
    search_fields = ('title', 'artist')
    list_filter = ('genre', 'release_date')

__all__ = ['SongAdmin']