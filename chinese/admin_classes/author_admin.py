from django.contrib import admin
from chinese.models import Author

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'introduction')
    search_fields = ('name',)
    list_filter = ('name',) 