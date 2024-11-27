from rest_framework import serializers
from chinese.models import FontCategory, FontInfo

class FontInfoSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()
    preview_url = serializers.SerializerMethodField()

    class Meta:
        model = FontInfo
        fields = ['code', 'name', 'file_url', 'preview_url', 'is_active']

    def get_file_url(self, obj):
        if obj.file:
            return self.context['request'].build_absolute_uri(obj.file.url)
        return None

    def get_preview_url(self, obj):
        if obj.preview_image:
            return self.context['request'].build_absolute_uri(obj.preview_image.url)
        return None

class FontCategorySerializer(serializers.ModelSerializer):
    fonts = serializers.SerializerMethodField()

    class Meta:
        model = FontCategory
        fields = ['code', 'name', 'description', 'order', 'fonts']

    def get_fonts(self, obj):
        # 只返回已启用的字体，并按 code 排序
        fonts = obj.fonts.filter(is_active=True).order_by('code')
        return FontInfoSerializer(fonts, many=True, context=self.context).data 