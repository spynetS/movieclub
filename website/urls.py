from django.contrib import admin
from django.urls import path

from movies.models import *
from .views import *

def movie(request,imdb_id):
    return render(request, "movie.html",{"movie":Movie.objects.get(imdb_id=imdb_id)})

def director(request,name):
    director = Director.objects.get(name=name)
    return render(request, "director.html",{"director":director,"movies":director.movies.all()})

def club(request):
    return render(request, "clubs.html", {})

urlpatterns = [
    path('', index, name="dashboard"),
    path("clubs/", club, name="clubs"),
    path("movies/", lambda request: render(request, "movies.html", {}), name="movies"),
    path("profile/", lambda request: render(request, "profile.html", {}), name="profile"),
    path("movie/<str:imdb_id>",movie,name="movie"),
    path("director/<str:name>",director, name="director")
]
