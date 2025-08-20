from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path("movies-search/", search, name="movie-search"),
    path("movies-add/<int:movie_pk>/", add_movie_to_user, name="add-movie-to-user"),

]
