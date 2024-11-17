from django.contrib import admin
from chinese.models import Author, AuthorIntroduction

class AuthorIntroductionInline(admin.TabularInline):
    model = AuthorIntroduction
    extra = 1

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_pinyin')
    search_fields = ('name', 'name_pinyin')
    inlines = [AuthorIntroductionInline] 