# yourapp/admin_classes/siteconfig.py
from django.contrib import admin
from django import forms
from music.models import SiteConfig
from django_json_widget.widgets import JSONEditorWidget

class SiteConfigAdminForm(forms.ModelForm):
    class Meta:
        model = SiteConfig
        fields = '__all__'
        widgets = {
            'value': JSONEditorWidget(),
        }

class SiteConfigAdmin(admin.ModelAdmin):
    form = SiteConfigAdminForm
    list_display = ('key',)
    search_fields = ('key',)

__all__ = ['SiteConfigAdmin']