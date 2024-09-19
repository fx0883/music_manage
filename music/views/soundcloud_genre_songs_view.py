import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from ..models import Song


class SoundCloudGenreSongsAPIView(APIView):
    @extend_schema(
        summary="Search tracks on SoundCloud",
        description=(
                "This API allows you to search for tracks on SoundCloud by providing a query parameter. "
                "It calls the SoundCloud mobile API, extracts track data, and returns a list of tracks "
                "with their details mapped to the `Song` model."
        ),
        parameters=[
            OpenApiParameter(
                name='query',
                description='Search term to find tracks (e.g., "Country")',
                required=True,
                type=str,
                default="Country"
            )
        ],
        responses={
            200: OpenApiResponse(
                description="A list of tracks",
                examples={
                    "application/json": [
                        {
                            "title": "Song Title",
                            "artist": "Artist Name",
                            "album": "Album Name",
                            "genre": "Genre",
                            "release_date": "2023-01-01",
                            "duration": 180,
                            "description": "Track description",
                            "kind": "track",
                            "license": "license info",
                            "permalink": "track-permalink",
                            "permalink_url": "https://soundcloud.com/track-url",
                            "permalink_image": "https://image-url.com/image.jpg",
                            "caption": "Caption",
                            "download_url": "https://download-url.com/track.mp3",
                            "full_duration": 300,
                            "likes_count": 120,
                            "playback_count": 1500,
                            "tag_list": "tag1 tag2"
                        }
                    ]
                }
            ),
            400: OpenApiResponse(description="Missing query parameter"),
            500: OpenApiResponse(description="SoundCloud API request failed")
        }
    )
    def get(self, request, *args, **kwargs):
        query = request.query_params.get('query', None)
        if not query:
            return Response({"error": "Missing query parameter"}, status=status.HTTP_400_BAD_REQUEST)

        # 调用SoundCloud API
        url = 'https://api-mobile.soundcloud.com/search/query'
        headers = {
            'Accept': 'application/json; charset=utf-8',
            'ADID': '83b5d936-150e-41c9-bd2a-edbe5e04cae4',
            'Authorization': 'OAuth 2-293571-1410263487-kCK3vEG4A5lqd',
            'App-Locale': 'en',
            'Device-Locale': 'en-US',
            'User-Agent': 'SoundCloud/2024.09.16-release (Android 13.0.0; Google Pixel 4)',
            'App-Version': '260090',
            'UDID': 'd047bfb9ffb6bddf6a6796e67936ef85',
        }
        params = {
            'client_id': 'dbdsA8b6Vw7wzu1x0T4CLxt58yd4Bf',
            'size_scaling': '1.0',
            'see_all_page': '0',
            'page': '0',
            'query': query,
            'previous_urn': 'soundcloud:search:de386447-afb8-44d1-a732-d344ec74a0ef',
            'action': 'GENRE_CELL_CLICKED',
            'layout_version': 'v4',
            'filter.content_type': 'ALL',
            'layout': 'soundcloud:layouts:category_page',
            'session_urn': 'soundcloud:search:1170c2e5-4129-410c-9b12-8f4ff9cd0d7d'
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            return Response({"error": "SoundCloud API request failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        data = response.json()

        # 提取 entities 内的 tracks 数据
        entities = data.get('entities', {})
        tracks_data = []
        for key, value in entities.items():
            if key.startswith("soundcloud:tracks") and value.get('type') == 'track':
                track_data = value.get('data', {})
                # 将track_data映射到Song模型
                song_data = {
                    'title': track_data.get('title'),
                    'artist': '',
                    'album': track_data.get('album', ''),
                    'genre': track_data.get('genre'),
                    'release_date': track_data.get('release_date'),
                    'duration': track_data.get('duration'),
                    'description': track_data.get('description'),
                    'kind': track_data.get('kind'),
                    'license': track_data.get('license'),
                    'permalink': track_data.get('permalink'),
                    'permalink_url': track_data.get('permalink_url'),
                    'permalink_image': track_data.get('artwork_url'),
                    'caption': track_data.get('caption'),
                    'download_url': track_data.get('download_url'),
                    'full_duration': track_data.get('full_duration'),
                    'likes_count': track_data.get('likes_count'),
                    'playback_count': track_data.get('playback_count'),
                    'tag_list': track_data.get('tag_list')
                }
                tracks_data.append(song_data)

        return Response(tracks_data, status=status.HTTP_200_OK)
