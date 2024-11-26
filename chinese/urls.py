from django.urls import path, include
from rest_framework.routers import DefaultRouter
from chinese.views.poem import PoemViewSet
from chinese.views.author import AuthorViewSet
from chinese.views.font import FontView

router = DefaultRouter()
router.register(r'poems', PoemViewSet)
router.register(r'authors', AuthorViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/fonts/<str:font_name>', FontView.as_view(), name='font'),
] 