from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path("movies-search/", search, name="movie-search"),
]
