from django.contrib import admin
from chinese.models import PoemType

class PoemTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code') 