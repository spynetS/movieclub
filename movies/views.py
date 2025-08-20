from django.http import Http404, HttpResponse
from django.shortcuts import render
import requests
import json

from accounts.models import Profile
from movies.models import Movie, Director
import os
# Create your views here.
def search(request):
    movies = []
    api = os.getenv("OMDB_API_KEY")
    url = f"https://www.omdbapi.com/?s={request.GET['search'].replace(' ','+')}&apikey={api}"
    print(url)
    response = requests.get(url)
    if response.json()["Response"] == "False":
        return render(request, "components/movies.html", {
        "movies":[]
    })
    movies_data = response.json()["Search"]

    movies = []
    for mj in movies_data:
        # Get or create the movie
        movie, created = Movie.objects.get_or_create(
            imdb_id=mj["imdbID"],  # Use imdb_id as the unique identifier
            defaults={
                'title': mj['Title'],
                'poster': mj['Poster'],
                'year': mj['Year'],
                'movie_type': mj["Type"],
                # Add other fields as needed, but they will be set to None if not provided
            }
        )

        # Only save the movie if it was created
        if created:
            movie.save()
        movies.append(movie)


    return render(request, "components/movies.html", {
        "search":request.GET['search'],
        "movies":movies
    })

def add_movie_to_user(request,movie_pk):
    movie: Movie = Movie.objects.get(pk=movie_pk)
    user: Profile = request.user

    movie.sync()

    response = Http404()
    if movie in user.movie_list.all():
        user.movie_list.remove(movie)
        response = HttpResponse("Add to my list")
    else:
        user.movie_list.add(movie)
        response = HttpResponse("Remove from my list")
    user.save()
    return response;
