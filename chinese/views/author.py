from rest_framework import viewsets
from rest_framework.response import Response
from chinese.models import Author, Language
from chinese.serializers.author import AuthorListSerializer, AuthorDetailSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter

class AuthorViewSet(viewsets.ReadOnlyModelViewSet):
    """
    作者相关的API端点
    """
    queryset = Author.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return AuthorListSerializer
        return AuthorDetailSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        language_code = self.request.query_params.get('language', 'en')
        context['language'] = Language.objects.get(code=language_code)
        return context

    @extend_schema(
        summary="获取作者列表",
        description="返回所有作者的基本信息列表",
        parameters=[
            OpenApiParameter(
                name='language',
                type=str,
                description='语言代码 (例如: en, zh, ja)',
                required=False
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="获取作者详情",
        description="返回指定作者的详细信息，包括介绍和作品列表",
        parameters=[
            OpenApiParameter(
                name='language',
                type=str,
                description='语言代码 (例如: en, zh, ja)',
                required=False
            )
        ]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs) 