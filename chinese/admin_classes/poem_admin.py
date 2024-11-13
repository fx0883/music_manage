from django.contrib import admin
from chinese.models import Poem

class PoemAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'poem_type', 'difficulty')
    search_fields = ('title', 'content')
    list_filter = ('difficulty', 'poem_type', 'author')
    raw_id_fields = ('author', 'poem_type')
    
    # 添加搜索字段以支持自动完成
    search_fields = ['title', 'title_pinyin']
 