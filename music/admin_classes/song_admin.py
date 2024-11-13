from django.contrib import admin
from ..models import Song

class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'album', 'genre', 'release_date', 'duration')
    search_fields = ('title', 'artist')
    list_filter = ('genre', 'release_date')

# 注册 model 和 admin 类
admin.site.register(Song, SongAdmin)