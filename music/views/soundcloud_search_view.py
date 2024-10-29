import threading
from django.http import JsonResponse
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework.views import APIView
from ..models import Song
from ..serializers import SongSerializer
from ..utils.gconfig import GlobalConfig
from ..utils.utils import DateUtils
import requests

class SoundCloudSearchAPIView(APIView):

    def save_songs_to_db(self, songs_data):
        for song_data in songs_data:
            title = song_data.get('title')
            permalink_url = song_data.get('permalink_url')

            if title and permalink_url and not Song.objects.filter(permalink_url=permalink_url).exists():
                song = Song(**song_data)
                try:
                    song.save()
                except Exception as e:
                    print(f"Error saving song: {e}")

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
        post_params = request.data
        default_params = GlobalConfig().get_config(GlobalConfig.SOUNDCLOUD)
        params = {**default_params, **post_params}
        url = 'https://api-v2.soundcloud.com/search'

        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Connection": "keep-alive",
            "Host": "api-v2.soundcloud.com",
            "Origin": "https://soundcloud.com",
            "Referer": "https://soundcloud.com/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
            "sec-ch-ua": "\"Chromium\";v=\"128\", \"Not;A=Brand\";v=\"24\", \"Google Chrome\";v=\"128\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\""

        }

        try:
            response = requests.get(url, params=params, headers=headers)
            response_data = response.json()
        except requests.RequestException as e:
            if response.status_code == 401:
                GlobalConfig().update_soundcloud_client_id()
                return JsonResponse({"error": "Invalid API key"}, status=401)
            return JsonResponse({"error": str(e)}, status=500)

        songs = []

        for trackList in response_data.get('collection', []):
            if not trackList.get('tracks'):
                title = trackList.get('title')
                permalink_url = trackList.get('permalink_url')

                if title and permalink_url:
                    song_data = {
                        'title': title,
                        'artist': trackList.get('user', {}).get('username'),
                        'album': trackList.get('album'),
                        'genre': trackList.get('genre'),
                        'release_date': DateUtils.convert_date(trackList.get('release_date')),
                        'duration': trackList.get('duration'),
                        'description': trackList.get('description'),
                        'kind': trackList.get('kind'),
                        'license': trackList.get('license'),
                        'permalink': trackList.get('permalink'),
                        'permalink_url': permalink_url,
                        'permalink_image': trackList.get('artwork_url'),
                        'caption': trackList.get('caption'),
                        'download_url': trackList.get('download_url'),

                        'full_duration': trackList.get('full_duration'),
                        'likes_count': trackList.get('likes_count'),
                        'playback_count': trackList.get('playback_count'),
                        'tag_list': trackList.get('tag_list')
                    }

                    songs.append(song_data)
            else:
                for track in trackList.get('tracks', []):
                    title = track.get('title')
                    permalink_url = track.get('permalink_url')

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
                            'download_url': track.get('download_url'),

                            'full_duration': track.get('full_duration'),
                            'likes_count': track.get('likes_count'),
                            'playback_count': track.get('playback_count'),
                            'tag_list': track.get('tag_list')
                        }

                        songs.append(song_data)

        # Start a new thread to save songs to the database
        threading.Thread(target=self.save_songs_to_db, args=(songs,)).start()

        # Serialize the songs data
        serializer = SongSerializer(songs, many=True)
        return JsonResponse(serializer.data, safe=False, status=200)
