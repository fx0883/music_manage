from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.views import APIView
from rest_framework.response import Response


class SongView(APIView):
    def get(self, request, *args, **kwargs):
        # 创建一个未绑定用户的 access token

        print(request)
        return Response({'access_token': 'hello world'})