import threading
from urllib.parse import urlencode

import requests
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from ..models import Song
from ..serializers import SongSerializer


class SoundCloudSearchAPIViewV2(APIView):

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
                default="王菲"
            ),
            OpenApiParameter(
                name='page',
                description='Page index starting from 1',
                required=False,
                type=int,
                default=1
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
                            "tag_list": "tag1,tag2"
                        }
                    ]
                }
            ),
            400: OpenApiResponse(description="Missing query parameter"),
            500: OpenApiResponse(description="SoundCloud API request failed")
        }
    )
    def get(self, request, *args, **kwargs):
        query = request.query_params.get('query', '王菲')  # 默认搜索 "王菲"
        page = request.query_params.get('page', 3)  # 默认第 3 页

        url = "https://api-mobile.soundcloud.com/search/query"

        # url = "https://api-mobile.soundcloud.com/search/query?client_id=dbdsA8b6V6Lw7wzu1x0T4CLxt58yd4Bf&limit=30&q=王菲&filter.content_type=all&version=v6&autocomplete_urn=soundcloud%3Asearch-autocomplete%3A966e6fc62c6142da8f1c84d7be2bad02&page=1"
        headers = {
            'Accept': 'application/json; charset=utf-8',
            'ADID': '83b5d936-150e-41c9-bd2a-edbe5e04cae4',
            'ADID-TRACKING': 'true',
            'Authorization': 'OAuth 2-293571-1410263487-kCK3vEG4A5lqd',
            'App-Locale': 'en',
            'Device-Locale': 'en-US',
            'User-Agent': 'SoundCloud/2024.09.16-release (Android 13.0.0; Google Pixel 4)',
            'App-Version': '260090',
            'UDID': 'd047bfb9ffb6bddf6a6796e67936ef85',
            'App-Requested-Features': 'api_ios_podcast=,api_ios_reduced_price=,api_ios_test=,api_test=,system_playlist_in_library=true',
            'App-Environment': 'prod',
            'Cookie': 'datadome=2cXNw44WLZ91mmGJBI425QlzumxPdUfwljJNhaLXAlfoyqMPghMFPZDFcY_IFQgEgvBjCf_kzT~J8VWvUYgvUnkgK~Q1pVuH12OrYNBmvVALn7mJQSYUtvRae9XEW5cm',
            'Host': 'api-mobile.soundcloud.com'
        }
        # params = {
        #     'client_id': 'dbdsA8b6V6Lw7wzu1x0T4CLxt58yd4Bf',
        #     'limit': 30,
        #     'q': query,
        #     'filter.content_type': 'all',
        #     'version': 'v6',
        #     'autocomplete_urn': 'soundcloud%3Asearch-autocomplete%3A966e6fc62c6142da8f1c84d7be2bad02',
        #     'page': page
        # }

        params = {
            'client_id': 'dbdsA8b6V6Lw7wzu1x0T4CLxt58yd4Bf',
            'limit': 30,
            'q': query,
            'filter.content_type': 'all',
            'version': 'v6',
            'page': page
        }

        # 手动构造 URL，将 autocomplete_urn 保留在 URL 中
        query_string = "&".join([f"{key}={value}" for key, value in params.items()])
        autocomplete_urn = 'soundcloud:search-autocomplete:966e6fc62c6142da8f1c84d7be2bad02'
        full_url = f"{url}?{query_string}&autocomplete_urn={autocomplete_urn}"

        # response = requests.request("GET", url, headers=headers, params=params, data=payload)

        query_string = urlencode(params)

        # 构造完整 URL
        full_url = f"{url}?{query_string}"
        print(full_url)
        response = requests.get(full_url, headers=headers)

        if response.status_code != 200:
            return Response({"error": f"SoundCloud API request failed: {response.status_code}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
                    'permalink_image': track_data.get('artwork_url_template'),
                    'caption': track_data.get('caption'),
                    'download_url': track_data.get('download_url'),
                    'full_duration': track_data.get('full_duration'),

                    'likes_count': None,
                    'playback_count': None,
                    'tag_list': None



                }

                try:
                    song_data['likes_count'] = track_data.get('_embedded').get('stats').get('likes_count')
                    song_data['playback_count'] = track_data.get('_embedded').get('stats').get('playback_count')
                    song_data['tag_list'] = ", ".join(track_data.get('user_tags'))
                except KeyError as e:
                    print(f"Key not found: {e}")
                except Exception as e:
                    print(f"An error occurred: {e}")


                # "_embedded": {
                #     "stats": {
                #         "playback_count": 17355,
                #         "comments_count": 57,
                #         "reposts_count": 27,
                #         "likes_count": 854
                #     },
                tracks_data.append(song_data)

        threading.Thread(target=self.save_songs_to_db, args=(tracks_data,)).start()

        # Serialize the songs data
        serializer = SongSerializer(tracks_data, many=True)
        return JsonResponse(serializer.data, safe=False, status=200)

        # return Response(tracks_data, status=status.HTTP_200_OK)
