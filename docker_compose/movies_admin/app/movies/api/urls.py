"""Модуль с перечислением url, используемых для доступа к версиям API."""

from django.urls import include, path

urlpatterns = [
    path('v1/', include('movies.api.v1.urls')),
]
