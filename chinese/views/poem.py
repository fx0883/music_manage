from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from chinese.models import Poem, Language, PoemType, PoemGenre
from chinese.serializers.poem import PoemListSerializer, PoemDetailSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
import random
from django.core.paginator import Paginator

class PoemViewSet(viewsets.ReadOnlyModelViewSet):
    """
    古诗词相关的API端点
    """
    queryset = Poem.objects.all()
    
    def get_serializer_class(self):
        """
        根据不同的action返回不同的序列化器
        """
        if self.action == 'retrieve':
            return PoemDetailSerializer
        return PoemListSerializer

    def get_serializer_context(self):
        """
        添加额外的上下文信息到序列化器
        """
        context = super().get_serializer_context()
        # 获取语言参数，默认为 'zh'
        language_code = self.request.query_params.get('language', 'zh')
        
        # 处理特殊情况
        if language_code == 'cn':
            language_code = 'zh'
            
        try:
            context['language'] = Language.objects.get(code=language_code)
        except Language.DoesNotExist:
            # 如果找不到指定语言，使用中文
            context['language'] = Language.objects.get(code='zh')
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # 获取诗词类型，默认为"唐诗"
        poem_type_code = self.request.query_params.get('poem_type', 'tang_shi')
        try:
            poem_type = PoemType.objects.get(code=poem_type_code)
            queryset = queryset.filter(poem_type=poem_type)
        except PoemType.DoesNotExist:
            default_type = PoemType.objects.get(code='tang_shi')
            queryset = queryset.filter(poem_type=default_type)
        
        # 体裁过滤
        genre_code = self.request.query_params.get('genre')
        if genre_code:
            try:
                genre = PoemGenre.objects.get(code=genre_code)
                queryset = queryset.filter(genre_relations__genre=genre)
            except PoemGenre.DoesNotExist:
                pass
        
        # 难度筛选
        difficulty = self.request.query_params.get('difficulty')
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
            
        # 排序
        sort_by = self.request.query_params.get('sort')
        if sort_by == 'difficulty':
            queryset = queryset.order_by('difficulty')
        elif sort_by == 'title':
            queryset = queryset.order_by('title_pinyin')
            
        return queryset

    @extend_schema(
        summary="获取古诗词列表",
        description="返回古诗词列表，支持按类型、体裁、难度筛选和多种排序方式。默认返回唐诗。",
        parameters=[
            OpenApiParameter(
                name='page',
                type=int,
                description='页码 (从1开始)',
                required=False,
                default=1
            ),
            OpenApiParameter(
                name='page_size',
                type=int,
                description='每页数量 (默认10，最大100)',
                required=False,
                default=10
            ),
            OpenApiParameter(
                name='poem_type',
                type=str,
                description='诗词类型代码 (默认: tang_shi 唐诗)',
                required=False,
                default='tang_shi'
            ),
            OpenApiParameter(
                name='genre',
                type=str,
                description='诗词体裁代码 (例如: wu_yan_shi 五言诗)',
                required=False
            ),
            OpenApiParameter(
                name='language',
                type=str,
                description='语言代码 (例如: en, zh, ja)',
                required=False
            ),
            OpenApiParameter(
                name='difficulty',
                type=int,
                description='难度等级 (1: 简单, 2: 中等, 3: 困难)',
                required=False
            ),
            OpenApiParameter(
                name='sort',
                type=str,
                description='排序方式 (difficulty: 按难度, title: 按标题拼音)',
                required=False
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        
        try:
            # 获取分页参数，处理可能的类型转换错误
            page = int(request.query_params.get('page', '1'))
            page_size = int(request.query_params.get('page_size', '10'))
            # 限制页大小范围
            page_size = max(1, min(page_size, 100))
        except ValueError:
            return Response({
                'error': 'Invalid page or page_size parameter'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 创建分页器
        paginator = Paginator(queryset, page_size)
        total_pages = paginator.num_pages
        total_count = paginator.count
        
        # 获取当前页数据
        try:
            current_page = paginator.page(page)
        except:
            return Response({
                'error': 'Invalid page number'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 序列化数据
        serializer = self.get_serializer(current_page.object_list, many=True)
        
        # 构建分页信息
        has_next = current_page.has_next()
        has_previous = current_page.has_previous()
        
        return Response({
            'count': total_count,  # 总记录数
            'total_pages': total_pages,  # 总页数
            'current_page': page,  # 当前页码
            'page_size': page_size,  # 每页大小
            'has_next': has_next,  # 是否有下一页
            'has_previous': has_previous,  # 是否有上一页
            'next_page': page + 1 if has_next else None,  # 下一页页码
            'previous_page': page - 1 if has_previous else None,  # 上一页页码
            'results': serializer.data  # 当前页数据
        })

    @extend_schema(
        summary="获取古诗词详情",
        description="返回指定古诗词的详细信息，包括注释、译文和赏析",
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

    @extend_schema(
        summary="获取随机背诵题目",
        description="随机选择一首诗的一句，并随机遮盖部分字词作为背诵题目",
        responses={200: {
            "type": "object",
            "properties": {
                "poem_id": {"type": "integer"},
                "poem_title": {"type": "string"},
                "quiz_line": {"type": "string"},
                "answer": {"type": "object"}
            }
        }}
    )
    @action(detail=False, methods=['get'])
    def random_quiz(self, request):
        """
        获取随机背诵题目
        """
        poems = Poem.objects.all()
        if not poems.exists():
            return Response(
                {'error': 'No poems available'}, 
                status=status.HTTP_404_NOT_FOUND
            )
            
        poem = random.choice(poems)
        content_lines = poem.content.split('\n')
        selected_line = random.choice(content_lines)
        
        # 随机遮盖一些字
        words = list(selected_line)
        mask_count = len(words) // 3  # 遮盖约1/3的字
        mask_indices = random.sample(range(len(words)), mask_count)
        
        quiz_line = ''
        answer = {}
        for i, word in enumerate(words):
            if i in mask_indices:
                quiz_line += '_'
                answer[i] = word
            else:
                quiz_line += word
                
        return Response({
            'poem_id': poem.id,
            'poem_title': poem.title,
            'quiz_line': quiz_line,
            'answer': answer
        }) 