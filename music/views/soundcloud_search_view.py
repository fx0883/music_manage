import requests
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Song
from ..serializers import SongSerializer
from ..utils.gconfig import GlobalConfig
from ..utils.utils import DateUtils


from django.db.models import Q

class SoundCloudSearchAPIView(APIView):

    @extend_schema(
        operation_id='SoundCloud 搜索 API',
        summary='搜索 SoundCloud 音乐',
        description='通过提供的参数搜索 SoundCloud 音乐，并返回匹配的歌曲列表。',
        request={
            'application/json': OpenApiTypes.OBJECT
        },
        examples=[
            OpenApiExample(
                '搜索请求示例',
                value={
                    'q': '王菲',
                    'limit': 20,
                    'offset': 0,
                },
            )
        ],
        responses={
            200: OpenApiTypes.OBJECT,  # 您可以在这里指定响应的结构
            400: OpenApiTypes.OBJECT,
            500: OpenApiTypes.OBJECT,
        }
    )
    def post(self, request):
        # Extract all POST parameters from the request
        post_params = request.data

        # Get default params from GlobalConfig
        default_params = GlobalConfig().get_config(GlobalConfig.SOUNDCLOUD)

        # Merge the POST parameters with the default params
        params = {**default_params, **post_params}

        # Call the SoundCloud API with the combined params
        url = 'https://api-v2.soundcloud.com/search'

        try:
            response = requests.get(url, params=params)
            response_data = response.json()
        except requests.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Map response data to Song model
        songs = []
        for track in response_data.get('collection', []):
            title = track.get('title')
            permalink_url = track.get('permalink_url')

            # Add song to the list if the title is not empty
            if title and permalink_url:
                song_data = {
                    'title': title,
                    'artist': track.get('user', {}).get('username'),
                    'album': track.get('album'),
                    'genre': track.get('genre'),
                    'release_date': DateUtils.convert_date(track.get('release_date')),
                    'duration': track.get('duration'),
                    'description': track.get('description'),
                    'kind': track.get('kind'),
                    'license': track.get('license'),
                    'permalink': track.get('permalink'),
                    'permalink_url': permalink_url,
                    'permalink_image': track.get('artwork_url'),
                    'caption': track.get('caption'),
                    'download_url': track.get('download_url')
                }

                # Append the song to the list
                song = Song(**song_data)
                songs.append(song)

                # Save the song only if permalink_url does not exist
                if permalink_url and not Song.objects.filter(permalink_url=permalink_url).exists():
                    try:
                        song.save()
                    except Exception as e:
                        print(f"Error saving song: {e}")
        # Serialize the songs data
        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
