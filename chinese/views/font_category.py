from rest_framework.views import APIView
from rest_framework.response import Response
from chinese.models import FontCategory
from chinese.serializers.font_category import FontCategorySerializer
from drf_spectacular.utils import extend_schema, OpenApiResponse

class FontCategoryListView(APIView):
    @extend_schema(
        summary="获取字体分类列表",
        description="返回所有字体分类及其包含的字体信息（只包含已启用的字体）",
        responses={
            200: OpenApiResponse(
                description="成功返回字体分类数据",
                response={
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "code": {"type": "string", "description": "分类代码"},
                            "name": {"type": "string", "description": "分类名称"},
                            "description": {"type": "string", "description": "分类描述"},
                            "order": {"type": "integer", "description": "显示顺序"},
                            "fonts": {
                                "type": "array",
                                "description": "分类下的字体列表（只包含已启用的字体）",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "code": {"type": "string", "description": "字体代码"},
                                        "name": {"type": "string", "description": "字体名称"},
                                        "file_url": {"type": "string", "description": "字体文件URL"},
                                        "preview_url": {"type": "string", "description": "预览图URL"},
                                        "is_active": {"type": "boolean", "description": "是否启用"}
                                    }
                                }
                            }
                        }
                    }
                }
            )
        }
    )
    def get(self, request):
        """获取所有字体分类及其字体信息"""
        # 获取所有分类，按order和code排序
        categories = FontCategory.objects.prefetch_related(
            'fonts'
        ).order_by('order', 'code')

        serializer = FontCategorySerializer(
            categories, 
            many=True, 
            context={'request': request}
        )
        return Response(serializer.data) 