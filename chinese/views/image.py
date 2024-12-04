from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from chinese.models import ImageCategory, ImageInfo
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse, OpenApiExample

class ImageListByCategory(APIView):
    """
    获取指定分类下的所有图片，默认获取卡片背景图片
    """
    
    @extend_schema(
        summary="获取分类图片列表",
        description="根据分类代码返回该分类下的所有图片信息。如果不指定分类代码，默认返回卡片背景图片(card_background)。",
        parameters=[
            OpenApiParameter(
                name='category_code',
                type=str,
                location=OpenApiParameter.PATH,
                description='图片分类代码，默认为card_background',
                required=False,
                examples=[
                    OpenApiExample(
                        'Card Background',
                        value='card_background',
                        description='卡片背景图片'
                    ),
                    OpenApiExample(
                        'Author Avatar',
                        value='author',
                        description='作者头像'
                    ),
                    OpenApiExample(
                        'Poem Image',
                        value='poem',
                        description='诗词配图'
                    ),
                ]
            )
        ],
        responses={
            200: OpenApiResponse(
                description="成功返回图片列表",
                response={
                    "type": "object",
                    "properties": {
                        "category": {
                            "type": "object",
                            "properties": {
                                "code": {"type": "string", "description": "分类代码"},
                                "name": {"type": "string", "description": "分类名称"},
                                "description": {"type": "string", "description": "分类描述"}
                            }
                        },
                        "images": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "integer", "description": "图片ID"},
                                    "title": {"type": "string", "description": "图片标题"},
                                    "description": {"type": "string", "description": "图片描述"},
                                    "image_url": {"type": "string", "description": "图片URL"},
                                    "is_active": {"type": "boolean", "description": "是否启用"},
                                    "created_at": {"type": "string", "format": "date-time", "description": "创建时间"}
                                }
                            }
                        }
                    }
                }
            ),
            404: OpenApiResponse(
                description="分类不存在",
                response={
                    "type": "object",
                    "properties": {
                        "error": {"type": "string"}
                    }
                }
            )
        }
    )
    def get(self, request, category_code=None):
        """获取指定分类下的所有图片"""
        # 如果没有指定分类代码，使用默认值
        if category_code is None:
            category_code = 'card_background'
            
        # 获取分类信息，如果不存在则返回404
        category = get_object_or_404(ImageCategory, code=category_code)
        
        # 获取该分类下的所有启用的图片
        images = ImageInfo.objects.filter(
            category=category,
            is_active=True
        ).order_by('-created_at')
        
        # 构建响应数据
        response_data = {
            'category': {
                'code': category.code,
                'name': category.name,
                'description': category.description
            },
            'images': [
                {
                    'id': img.id,
                    'title': img.title,
                    'description': img.description,
                    'image_url': request.build_absolute_uri(img.image.url),
                    'is_active': img.is_active,
                    'created_at': img.created_at
                } for img in images
            ]
        }
        
        return Response(response_data) 