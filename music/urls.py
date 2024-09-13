#!/usr/bin/python3
# -*- coding:utf-8 -*-
# __author__ = "__Jack__"

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from music.views import recommend_songs_view
from music.views.permalink_view import PermalinkToOfficialURLAPIView
from music.views.recommend_songs_view import RecommendSongsAPIView
from music.views.song_list_by_genre_view import SongListByGenreView
from music.views.soundcloud_search_view import SoundCloudSearchAPIView

# router = DefaultRouter()
# router.register(prefix="viewsets", viewset=views.CourseViewSet)

urlpatterns = [
    # Function Based View
    # path("fbv/list/", views.course_list, name="fbv-list"),
    # path("fbv/detail/<int:pk>/", views.course_detail, name="fbv-detail"),

    # Class Based View
    # path("token/get/", auth_views.GenerateAnonymousTokenView.as_view(), name="generate-access-token"),

    # path("search/", song_views.SongView.as_view(), name="song-search"),
    path('soundcloud/search/', SoundCloudSearchAPIView.as_view(), name='soundcloud-search'),
    path('soundcloud/permalink/', PermalinkToOfficialURLAPIView.as_view(), name='permalink'),
    path('soundcloud/recommend-songs/', RecommendSongsAPIView.as_view(), name='recommend-songs'),
    path('local/songs/', SongListByGenreView.as_view(), name='song-list-by-genre'),
    # # Generic Class Based View
    # path("gcbv/list/", views.GCourseList.as_view(), name="gcbv-list"),
    # path("gcbv/detail/<int:pk>/", views.GCourseDetail.as_view(), name="gcbv-detail"),

    # path("", include(router.urls))
]
