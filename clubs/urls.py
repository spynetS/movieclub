from django.contrib import admin
from django.urls import path

from movies.models import *
from .views import *

urlpatterns = [
    path("vote/<int:club_pk>/<int:movie_pk>/",vote,name="vote"),
    path("vote-tab/",lambda request: render(request,"components/vote-tab.html",{"voted_movie":request.user.selected_club.get_voted_movie(request.user)}),name="vote-tab"),
    path("movies-tab/",lambda request: render(request,"components/movies-tab.html",{}),name="movies-tab"),
    path("schedule-tab/",lambda request: render(request,"components/schedule-tab.html",{"club":request.user.clubs.first()}),name="schedule-tab"),
    path("manage-tab/",lambda request: render(request,"components/manage-tab.html",{"club":request.user.clubs.first()}),name="manage-tab"),
    path("schedule/<int:club_pk>/",schedule,name="schedule"),
    path("set-selected-club/",set_selected_club,name="set-selected-club"),
    path("votes/<int:movie_pk>/",votes,name="movie-votes"),
    path("create_vote/<int:club_pk>/",create_vote,name="create_vote"),
    path("pick_movie/<int:club_pk>/",pick_movie,name="pick_movie"),
    path("club",club,name="club"),
    path("toggle-membership/<int:user_pk>",toggle_membership,name='toggle-membership')
]
