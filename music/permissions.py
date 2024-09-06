# from rest_framework.permissions import BasePermission
# from rest_framework_simplejwt.tokens import AccessToken
# from rest_framework.exceptions import AuthenticationFailed
#
#
# class IsTokenAuthenticated(BasePermission):
#     def has_permission(self, request, view):
#         # 获取 Authorization 头中的 token
#         auth_header = request.headers.get('Authorization')
#
#         if auth_header is None or not auth_header.startswith('Bearer '):
#             return False
#
#         # 提取 token 字符串
#         token_str = auth_header.split(' ')[1]
#
#         try:
#             # 尝试验证 token
#             token = AccessToken(token_str)
#             token.check_exp()  # 检查 token 是否过期
#         except Exception as e:
#             raise AuthenticationFailed('Invalid or expired token') from e
#
#         return True
from rest_framework.authentication import BaseAuthentication
# your_app/authentication.py

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import AccessToken

class EmptyTokenAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # 允许所有请求通过认证
        return (None, None)  # 或者根据需要返回实际的用户和身份信息

    def authenticate_header(self, request):
        # 可以返回自定义的认证头部
        return None

class AccessTokenAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # 获取 Token
        raw_token = self.get_raw_token(request)

        if raw_token is None:
            raise InvalidToken("Token is missing or invalid.")

        try:
            # 验证 Token 的合法性
            validated_token = self.get_validated_token(raw_token)
        except InvalidToken as e:
            raise e

        # 返回验证过的 token，但不返回用户
        return (validated_token, None)  # 不返回用户信息

    def get_raw_token(self, request):
        # 从请求中提取 Token
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            return auth_header.split(' ')[1]
        return None

    # def get_validated_token(self, raw_token):
    #     # 使用 Simple JWT 的方法验证 Token
    #     try:
    #         token = AccessToken(raw_token)
    #         token.check_exp()  # 检查 token 是否过期
    #         return token
    #     except Exception as e:
    #         raise InvalidToken(e)
    def get_validated_token(self, raw_token):
        try:
            # 生成 AccessToken 实例并验证其合法性
            token = AccessToken(raw_token)
            token.check_exp()  # 检查 token 是否过期
            return token
        except TokenError as e:
            # 捕捉 Simple JWT 的 TokenError 异常并重新抛出 InvalidToken 异常
            raise InvalidToken(e)
        except Exception as e:
            # 捕捉其他异常
            raise InvalidToken(f"Invalid token: {str(e)}")

class UserTokenAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        # 使用默认的用户验证逻辑
        return super().get_user(validated_token)

