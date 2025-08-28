from django.contrib import admin
from django.urls import path

from movies.models import *
from .views import *

from django.db.models import Avg, F, ExpressionWrapper, FloatField
from ratings.models import *

def movie(request, imdb_id):
    movie = Movie.objects.get(imdb_id=imdb_id)

    # Use tuple unpacking to get the rating object and the 'created' boolean
    rating_object, created = Rating.objects.get_or_create(
        user=request.user,
        movie=movie
    )

    return render(request, "movie.html", {
        "movie": movie,
        "rating": rating_object,  # Pass only the rating object to the template
    })


def director(request,name):
    director = Director.objects.get(name=name)
    movies = director.movies.all()
        # Retrieve ratings for all movies directed by this director
    ratings = Rating.objects.filter(movie__in=movies).annotate(
        avg_look=Avg('look'),
        avg_script=Avg('script'),
        avg_acting=Avg('acting'),
        avg_soundtrack=Avg('soundtrack'),
        avg_overalscore=Avg('overalscore'),
        avg_bonus=Avg('bonus'),
        avg_total=ExpressionWrapper(
            (F('look') + F('script') + F('acting') + F('soundtrack') + F('overalscore') + F('bonus')) / 5,
            output_field=FloatField()
        )
    )
    return render(request, "director.html",{
        "director":director,
        "movies":movies,
        "ratings":ratings})

def club(request):
    return render(request, "clubs.html", {})

def profile_username(request,username):
    return render(request, "profile.html",
           {
               'profile':Profile.objects.get(username=username)
           })


urlpatterns = [
    path('', index, name="dashboard"),

    path("clubs/", club, name="clubs"),
    path("movies/", lambda request: render(request, "movies.html", {}), name="movies"),
    path("profile/", lambda request: render(request, "profile.html", {'profile':request.user}), name="profile"),
    path("profile/<str:username>", profile_username, name="profile"),
    path("movie/<str:imdb_id>",movie,name="movie"),
    path("director/<str:name>",director, name="director"),
    path("add-member-modal", add_member_modal, name="add-member-modal")
]
