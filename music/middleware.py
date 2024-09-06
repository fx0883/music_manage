# your_app/middleware.py

# from django.http import JsonResponse
# from rest_framework_simplejwt.exceptions import InvalidToken
#
# from music.permissions import AccessTokenAuthentication
#
#
# class AccessTokenMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#         self.authenticator = AccessTokenAuthentication()
#
#     def __call__(self, request):
#         if request.path.startswith('/access-token/'):
#             # 使用 AccessTokenAuthentication 的 authenticate 方法进行认证
#             try:
#                 # 调用 authenticate 方法进行认证
#                 self.authenticator.authenticate(request)
#             except InvalidToken:
#                 return JsonResponse({'detail': 'Invalid or expired token.'}, status=401)
#             except Exception as e:
#                 return JsonResponse({'detail': str(e)}, status=401)
#
#         response = self.get_response(request)
#         return response
