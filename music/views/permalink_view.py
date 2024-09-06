from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from drf_spectacular.utils import extend_schema, OpenApiTypes, OpenApiExample

import youtube_dl
class PermalinkSerializer(serializers.Serializer):
    permalink_url = serializers.URLField(required=True,
                                         help_text="Provide the permalink URL to retrieve the official URL.")


class PermalinkToOfficialURLAPIView(APIView):
    """
    API to return the official URL given a permalink_url.
    """

    @extend_schema(
        operation_id='Permalink to Official URL API',
        summary='Retrieve official URL from permalink',
        description='This API accepts a permalink URL and returns the corresponding official URL.',
        request={
            'application/json': OpenApiTypes.OBJECT
        },
        examples=[
            OpenApiExample(
                'Permalink Request Example',
                value={
                    'permalink_url': 'https://soundcloud.com/nguyengocnhuynhxd/nhu-uoc-nguyen-vuong-phi',
                },
            )
        ],
        responses={
            200: OpenApiTypes.OBJECT,  # Define the structure of the 200 response
            400: OpenApiTypes.OBJECT,
            500: OpenApiTypes.OBJECT,
        }
    )
    def post(self, request):
        # Validate the request data using a serializer
        serializer = PermalinkSerializer(data=request.data)
        if serializer.is_valid():
            permalink_url = serializer.validated_data['permalink_url']

            # Logic to convert permalink_url to the official URL (example logic)
            # In this case, we simply return the permalink_url itself as the official URL.
            official_url = self.get_official_url(permalink_url)

            return Response({'official_url': official_url}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_official_url(self, permalink_url):
        """
        Function to retrieve or convert permalink_url to the official URL.
        Currently, it simply returns the permalink_url. You can modify the logic here.
        """




        # youtube_dl options
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,  # Suppresses verbose output
            'no_warnings': True,
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(permalink_url, download=False)
            download_url = info_dict.get('url', None)
            # title = info_dict.get('title', None)

            # print(f"Title: {title}")
            print(f"Download URL: {download_url}")
        return download_url
