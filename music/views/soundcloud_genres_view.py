import requests
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from ..models import GenreItem
from ..serializers import GenreItemSerializer


class SoundCloudGenresView(APIView):
    @extend_schema(
        summary="SoundCloud API Search",
        description="调用 SoundCloud API 并返回 sections 数据，包括 items 信息",
        responses={200: 'OK'}
    )
    def get(self, request):
        url = 'https://api-mobile.soundcloud.com/search/query'
        params = {
            'client_id': 'dbdsA8b6V6Lw7wzu1x0T4CLxt58yd4Bf',
            'q': ' ',
            'layout': 'soundcloud:layouts:landing_page',
            'version': 'v4'
        }
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
            'Cookie': 'datadome=hUBWp3vGxAPd2HwGNwCeK781OM_3tSGjG444cLGMDCYe~Kr7ITzBR2vlAg1USc1z7heNW2Nhmg8sglKyxPGyBVyhsAGlX_7gUHCn3Y_jVUezF8rammzcDfr6jYIo3XK_',
            'Host': 'api-mobile.soundcloud.com',
            'If-Modified-Since': 'Wed, 18 Sep 2024 03:44:38 GMT'
        }

        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()  # 检查HTTP响应状态码

            # 获取返回的JSON数据
            data = response.json()
            genres = []
            # 提取并处理需要的 items 数据
            sections = data.get('sections', {})
            for section in sections:
                itemsData = section.get('data', [])

                # 保存每个 item 到数据库
                for item in itemsData.get('items', []):
                    action_link = item.get('action_link', {})
                    genreItem = {
                        'image_large_light': item.get('image_large_light', ''),
                        'image_large_dark': item.get('image_large_dark', ''),
                        'border_color': item.get('border_color', ''),
                        'title': item.get('title', ''),
                        'action_link_navigation_type': action_link.get('navigation_type', ''),
                        'action_link_id': action_link.get('id', ''),
                        'action_link_caption': action_link.get('caption', ''),
                        'image_small_dark': item.get('image_small_dark', ''),
                        'image_medium_dark': item.get('image_medium_dark', ''),
                        'portrait_size': item.get('portrait_size', 0),
                        'subtitle': item.get('subtitle', ''),
                        'image_medium_light': item.get('image_medium_light', ''),
                        'landscape_size': item.get('landscape_size', 0),
                        'image_small_light': item.get('image_small_light', '')
                    }

                    genres.append(genreItem)

            serializer = GenreItemSerializer(genres, many=True)
            return JsonResponse(serializer.data, safe=False, status=200)

        except requests.exceptions.RequestException as e:
            # 处理请求异常
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
