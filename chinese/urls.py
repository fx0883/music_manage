from django.urls import path, include
from rest_framework.routers import DefaultRouter
from chinese.views.poem import PoemViewSet
from chinese.views.author import AuthorViewSet
from chinese.views.font import FontView
from chinese.views.font_category import FontCategoryListView
from chinese.views.image import ImageListByCategory

router = DefaultRouter()
router.register(r'poems', PoemViewSet)
router.register(r'authors', AuthorViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/fonts/<str:font_name>', FontView.as_view(), name='font'),
    path('api/font-categories/', FontCategoryListView.as_view(), name='font-categories'),
    path('api/images/category/', ImageListByCategory.as_view(), name='image-list-default-category'),
    path('api/images/category/<str:category_code>/', ImageListByCategory.as_view(), name='image-list-by-category'),
] 
