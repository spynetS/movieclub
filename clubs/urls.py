from django.contrib import admin
from django.urls import path

from movies.models import *
from .views import *

urlpatterns = [
    path("vote/<int:club_pk>/<int:movie_pk>/",vote,name="vote"),
    path("vote-tab/",lambda request: render(request,"components/vote-tab.html",{}),name="vote-tab"),
    path("movies-tab/",lambda request: render(request,"components/movies-tab.html",{}),name="movies-tab"),
]
