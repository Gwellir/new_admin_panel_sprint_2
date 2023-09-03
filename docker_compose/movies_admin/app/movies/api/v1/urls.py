"""Модуль с перечислением url, используемых для доступа к методам API v1.0."""

from django.urls import path
from movies.api.v1 import views

urlpatterns = [
    path('movies/', views.MoviesListApi.as_view()),
    path('movies/<uuid:pk>/', views.MoviesDetailApi.as_view()),
]
