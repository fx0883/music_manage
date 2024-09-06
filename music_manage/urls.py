"""
URL configuration for music_manage project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.models import User
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework import routers, serializers, viewsets, permissions
from rest_framework_simplejwt.views import TokenRefreshView

from music.views import auth_views
from music.views.auth_views import AccessTokenAPIView, UserTokenAPIView, CustomTokenObtainPairView
from rest_framework_simplejwt import views as jwt_views

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)




urlpatterns = [
    # path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    # path('api/token/verify/', jwt_views.TokenVerifyView.as_view(), name='token_verify'),
    # dj-rest-auth 提供的登录、注销、注册等API
    # path('auth/', include('dj_rest_auth.urls')),
    #
    # # JWT token 的刷新和验证
    # path('auth/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    # path('auth/token/verify/', jwt_views.TokenVerifyView.as_view(), name='token_verify'),

    path("api/v1/auth/", include("dj_rest_auth.urls")),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path("music/", include("music.urls")),

    # 用于生成 schema 的端点
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    # Swagger 文档的 UI 视图
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # Redoc 文档的 UI 视图
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),


]







