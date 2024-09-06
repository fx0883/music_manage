#!/usr/bin/python3
# -*- coding:utf-8 -*-
# __author__ = "__Jack__"

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from music.views import song_views

# router = DefaultRouter()
# router.register(prefix="viewsets", viewset=views.CourseViewSet)

urlpatterns = [
    # Function Based View
    # path("fbv/list/", views.course_list, name="fbv-list"),
    # path("fbv/detail/<int:pk>/", views.course_detail, name="fbv-detail"),

    # Class Based View
    # path("token/get/", auth_views.GenerateAnonymousTokenView.as_view(), name="generate-access-token"),

    path("search/", song_views.SongView.as_view(), name="song-search"),

    # # Generic Class Based View
    # path("gcbv/list/", views.GCourseList.as_view(), name="gcbv-list"),
    # path("gcbv/detail/<int:pk>/", views.GCourseDetail.as_view(), name="gcbv-detail"),

    # path("", include(router.urls))
]
