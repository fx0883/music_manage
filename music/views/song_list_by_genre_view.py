from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from ..models import Song
from ..serializers import SongSerializer


class SongPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


@extend_schema(
    description="Retrieve a list of songs filtered by genre with pagination support.",
    parameters=[
        OpenApiParameter(
            name='genre',
            description='Genre of the song',
            required=False,
            type=str,
            default="Pop"  # 默认值为 "Pop"
        ),
        OpenApiParameter(
            name='page',
            description='Page number for pagination',
            required=False,
            type=int,
            default=1  # 默认值为第一页
        ),
        OpenApiParameter(
            name='page_size',
            description='Number of items per page',
            required=False,
            type=int,
            default=20  # 默认值为每页 20 条记录
        )
    ],
    examples=[
        OpenApiExample(
            "Genre Filter Example",
            description="An example of filtering songs by genre.",
            value={"genre": "rock", "page": 0, "page_size": 20},
        )
    ],
    responses={
        200: SongSerializer(many=True),
        400: "Error message if genre is not provided."
    }
)
class SongListByGenreView(generics.ListAPIView):
    serializer_class = SongSerializer
    pagination_class = SongPagination

    def get(self, request, *args, **kwargs):
        genre = request.query_params.get('genre', None)
        if genre:
            # 使用 icontains 进行大小写不敏感的部分匹配
            songs = Song.objects.filter(genre__icontains=genre)
        else:
            return Response({'error': 'Genre parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)

        page = self.paginate_queryset(songs)
        if page is not None:
            serializer = self.get_paginated_response(SongSerializer(page, many=True).data)
        else:
            serializer = SongSerializer(songs, many=True)

        return Response(serializer.data)
