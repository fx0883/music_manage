# forms.py
from django import forms
from ..models import Config
# admin.py
from django.contrib import admin
import json

from ..utils.gconfig import GlobalConfig


class ConfigAdminForm(forms.ModelForm):
    class Meta:
        model = Config
        fields = ['name', 'value']  # 根据需求自定义要显示的字段

    def clean_value(self):
        value = self.cleaned_data.get('value')
        # 这里可以添加自定义的验证逻辑
        # 例如，确保配置值是一个有效的 JSON 字符串
        try:
            json.loads(value)  # 假设 value 需要是 JSON 格式
        except ValueError:
            raise forms.ValidationError("Invalid JSON format!")
        return value


class ConfigAdmin(admin.ModelAdmin):
    class Meta:
        model = Config
        fields = ['name', 'value', 'updated_at']  # 根据需求自定义要显示的字段
    list_display = ('name', 'value', 'updated_at')
    search_fields = ('name',)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        GlobalConfig.reload_config()  # 每次保存后重新加载配置

    def delete_model(self, request, obj):
        super().delete_model(request, obj)
        GlobalConfig.reload_config()  # 删除配置后重新加载


__all__ = ['ConfigAdmin']
