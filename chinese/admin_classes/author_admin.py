from django.contrib import admin
from django.utils.html import format_html
from chinese.models import Author, AuthorIntroduction

class AuthorIntroductionInline(admin.TabularInline):
    model = AuthorIntroduction
    extra = 1

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_pinyin', 'image_preview')
    search_fields = ('name', 'name_pinyin')
    inlines = [AuthorIntroductionInline]
    readonly_fields = ('image_preview',)
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius: 50%;" />',
                obj.image.url
            )
        return "No Image"
    image_preview.short_description = 'Image Preview'

    fieldsets = (
        (None, {
            'fields': ('name', 'name_pinyin', 'image', 'image_preview')
        }),
    )