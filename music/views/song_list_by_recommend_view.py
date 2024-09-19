# from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
# from rest_framework.response import Response
# from rest_framework import status, generics
# from rest_framework.pagination import PageNumberPagination
# from ..models import Song
# from ..serializers import SongSerializer
#
#
# class SongPagination(PageNumberPagination):
#     page_size = 20
#     page_size_query_param = 'pagesize'
#     page_query_param = 'pageindex'
#     max_page_size = 100
#
#
#
# class SoundCloudSongListView(generics.ListAPIView):
#     serializer_class = SongSerializer
#     pagination_class = SongPagination
#
#     def get(self, request, *args, **kwargs):
#         # Extract query parameters
#         query_param = request.query_params.get('query', 'playback_count')
#         page_size = request.query_params.get('pagesize', SongPagination.page_size)
#         page_index = request.query_params.get('pageindex', 0)
#
#         # Get queryset
#         queryset = Song.objects.all()
#         if query_param == 'likes_count':
#             queryset = queryset.order_by('-likes_count')
#         else:
#             queryset = queryset.order_by('-playback_count')
#
#         # Handle pagination
#         paginator = self.pagination_class()
#         paginator.page_size = int(page_size)
#         paginated_queryset = paginator.paginate_queryset(queryset, request)
#
#         serializer = SongSerializer(paginated_queryset, many=True)
#         return paginator.get_paginated_response(serializer.data)



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
    description="Retrieve a paginated list of songs sorted by likes_count or playback_count.",
    parameters=[
        OpenApiParameter(
            name='query',
            description='Sort by likes_count or playback_count',
            required=False,
            type=str,
            default='playback_count'
        ),
        OpenApiParameter(
            name='page_size',
            description='Number of items per page',
            required=False,
            type=int,
            default=20
        ),
        OpenApiParameter(
            name='page',
            description='Page index starting from 0',
            required=False,
            type=int,
            default=1
        ),
    ],
    examples=[
        OpenApiExample(
            "Sorting and Pagination Example",
            description="An example of retrieving sorted and paginated songs.",
            value={"query": "playback_count", "pagesize": 20, "pageindex": 0},
        )
    ],
    responses={
        200: SongSerializer(many=True),
        400: "Error message if parameters are invalid."
    }
)
class SongListByRecommendView(generics.ListAPIView):
    serializer_class = SongSerializer
    pagination_class = SongPagination

    def get(self, request, *args, **kwargs):
        query_param = request.query_params.get('query', 'playback_count')
        songs = None
        if query_param == 'likes_count':
            songs = Song.objects.order_by('-likes_count')
        else:
            songs = Song.objects.order_by('-playback_count')

        page = self.paginate_queryset(songs)
        if page is not None:
            serializer = self.get_paginated_response(SongSerializer(page, many=True).data)
        else:
            serializer = SongSerializer(songs, many=True)

        return Response(serializer.data)

