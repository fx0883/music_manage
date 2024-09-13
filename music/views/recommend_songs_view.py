import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiResponse
from ..models import Song
from ..serializers import SongSerializer
from ..utils.utils import DateUtils

class RecommendSongsAPIView(APIView):

    @extend_schema(
        summary="Get Recommended Songs from SoundCloud",
        description="Fetches recommended songs from a SoundCloud playlist and stores unique tracks in the database. Returns a list of stored songs.",
        responses={
            200: OpenApiResponse(response=SongSerializer(many=True), description="List of recommended songs"),
            400: OpenApiResponse(description="Error occurred while fetching songs from SoundCloud")
        }
    )
    def get(self, request, *args, **kwargs):
        """
        Fetch recommended songs from SoundCloud, save to database if not already present,
        and return the list of songs.
        """
        # SoundCloud API URL and parameters
        soundcloud_url = 'https://api-v2.soundcloud.com/playlists/1711492746'
        params = {
            'representation': 'full',
            'client_id': 'yxyU37cOIWLSzVIT8WE4Ppx0BzGakZsq',
            'app_version': '1725965070',
            'app_locale': 'en'
        }

        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Origin': 'https://soundcloud.com',
            'Referer': 'https://soundcloud.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'x-datadome-clientid': '7Az4fOIJ4tMY0jAHsVtrhORc10XhVCHQzKy5GyZdb9z1uZrYL_e4cZCQcC1Klw9Lh5Go4bcwxY5gcFHQySYae10VZSGIZKJn5b83KOLJxIOss8tuUbdqCNsC~Mekex3n',
        }

        try:
            response = requests.get(soundcloud_url, headers=headers, params=params)
            response.raise_for_status()
        except requests.RequestException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        data = response.json()

        # Parse SoundCloud API data and save new songs
        songs = []
        for track in data.get('tracks', []):
            # song_data = {
            #     'title': track.get('title'),
            #     'artist': track.get('user', {}).get('username'),
            #     'album': track.get('publisher_metadata', {}).get('release_title'),
            #     'genre': track.get('genre'),
            #     'release_date': DateUtils.convert_date(track.get('release_date')),
            #     'duration': track.get('duration'),
            #     'description': track.get('description'),
            #     'kind': track.get('kind'),
            #     'license': track.get('license'),
            #     'permalink': track.get('permalink'),
            #     'permalink_url': track.get('permalink_url'),
            #     'permalink_image': track.get('artwork_url'),
            #     'caption': track.get('caption'),
            #     'download_url': track.get('download_url'),
            # }
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

                song = Song(**song_data)
                songs.append(song)

                # Save the song only if permalink_url does not exist
                if permalink_url and not Song.objects.filter(permalink_url=permalink_url).exists():
                    try:
                        song.save()
                    except Exception as e:
                        print(f"Error saving song: {e}")

        # Serialize and return the list of songs
        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
