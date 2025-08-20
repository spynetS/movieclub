from django.shortcuts import render
import requests
import json

# Create your views here.
def search(request):
    movies = []
    api="e5f1fd02"
    url = f"https://www.omdbapi.com/?s={request.GET['search']}&apikey={api}"
    response = requests.get(url)
    movie_data = response.json()["Search"]
    print(movie_data)

    return render(request, "movies.html", {
        "search":request.GET['search'],
        "movies":movie_data
    })
