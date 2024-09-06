from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.views import APIView
from rest_framework.response import Response

from music.utils.gconfig import GlobalConfig


class SongView(APIView):
    def get(self, request, *args, **kwargs):
        # 创建一个未绑定用户的 access token

        print(request)

        soundCloudConfig = GlobalConfig().get_config(GlobalConfig.SOUNDCLOUD)
        print(soundCloudConfig)
        return Response({'access_token': 'hello world'})