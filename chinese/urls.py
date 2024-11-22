from django.urls import path, include
from rest_framework.routers import DefaultRouter
from chinese.views.poem import PoemViewSet
from chinese.views.author import AuthorViewSet

router = DefaultRouter()
router.register(r'poems', PoemViewSet)
router.register(r'authors', AuthorViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
] 