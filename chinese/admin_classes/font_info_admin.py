from io import BytesIO
import tempfile

from django.contrib import admin
from django.utils.html import mark_safe
from django.urls import path
from django.http import JsonResponse
from django.core.files.base import ContentFile
from chinese.models import FontInfo
from chinese.utils.font_utils import generate_font_preview, get_pinyin_code, get_filename_without_extension
import os
from django.conf import settings
import logging
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt

# 添加日志配置
logger = logging.getLogger(__name__)

class FontInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'code', 'is_active', 'created_at', 'preview_thumbnail')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('name', 'code')
    raw_id_fields = ('category',)
    readonly_fields = ('file_preview', 'preview_image_tag')
    
    def preview_thumbnail(self, obj):
        """在列表页显示缩略图"""
        if obj.preview_image:
            return mark_safe(
                f'<img src="{obj.preview_image.url}" width="100" style="max-width:100%;" />'
            )
        return '无预览图'
    preview_thumbnail.short_description = '预览缩略图'
    
    def get_urls(self):
        urls = super().get_urls()
        info = self.model._meta.app_label, self.model._meta.model_name
        
        custom_urls = [
            path(
                'apply_font/',
                self.admin_site.admin_view(self._apply_font_view),
                name='%s_%s_apply_font' % info
            ),
            path(
                'clear_font/',
                self.admin_site.admin_view(self._clear_font_view),
                name='%s_%s_clear_font' % info
            ),
        ]
        return custom_urls + urls

    @method_decorator(staff_member_required)
    def _apply_font_view(self, request):
        """处理应用字体请求的视图函数"""
        return self.apply_font(request)

    @method_decorator(staff_member_required)
    def _clear_font_view(self, request):
        """处理清除字体信息的视图函数"""
        return self.clear_font(request)

    def apply_font(self, request):
        """处理应用字体请求的具体逻辑"""
        logger.debug(f"Request method: {request.method}")
        logger.debug(f"User: {request.user}")
        logger.debug(f"POST data: {request.POST}")
        logger.debug(f"Files: {request.FILES}")
        
        if request.method != 'POST':
            return JsonResponse({'error': '仅支持POST请求'}, status=405)
            
        try:
            # 获取上传的文件
            font_file = request.FILES.get('font_file')
            if not font_file:
                return JsonResponse({'error': '未找到字体文件'}, status=400)

            try:
                # 获取文件名（不含扩展名）作为字体名称
                font_name = get_filename_without_extension(font_file.name)
                
                # 生成拼音代码
                font_code = get_pinyin_code(font_name)
                
                # 直接使用上传的文件对象生成预览图
                preview_img = generate_font_preview(font_file, font_name)
                
                # 将预览图保存到临时BytesIO
                img_io = BytesIO()
                preview_img.save(img_io, format='PNG')
                
                return JsonResponse({
                    'success': True,
                    'font_name': font_name,
                    'font_code': font_code,
                    'preview_data': img_io.getvalue().decode('latin1')
                })
                
            except Exception as e:
                logger.error(f"Error in apply_font: {str(e)}")
                return JsonResponse({
                    'error': f'处理字体文件时出错: {str(e)}'
                }, status=500)
                
        except Exception as e:
            logger.error(f"Error in apply_font outer: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)

    def clear_font(self, request):
        """处理清除字体信息请求的具体逻辑"""
        if request.method != 'POST':
            return JsonResponse({'error': '仅支持POST请求'}, status=405)
            
        try:
            preview_path = request.POST.get('preview_path')
            if preview_path:
                full_path = os.path.join(settings.MEDIA_ROOT, preview_path)
                if os.path.exists(full_path):
                    os.remove(full_path)
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    class Media:
        js = (
            'admin/js/jquery.init.js',  # 确保 jQuery 正确初始化
            'js/font_info.js',
        )
    
    fieldsets = (
        ('基本信息', {
            'fields': ('category', 'name', 'code', 'is_active')
        }),
        ('文件', {
            'fields': ('file',)
        }),
        ('预览图', {
            'fields': ('preview_image', 'preview_image_tag')
        }),
        ('其他信息', {
            'fields': ('description',)
        })
    ) 