from django.http import FileResponse
from django.conf import settings
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

class FontView(APIView):
    @extend_schema(
        summary="获取字体文件",
        description="下载指定的字体文件",
        parameters=[],
        responses={200: bytes}
    )
    def get(self, request, font_name):
        """获取字体文件"""
        font_path = os.path.join(settings.MEDIA_ROOT, 'fonts', f'{font_name}.ttf')
        if os.path.exists(font_path):
            return FileResponse(open(font_path, 'rb'), content_type='font/ttf')
        return Response({'error': 'Font not found'}, status=404) 