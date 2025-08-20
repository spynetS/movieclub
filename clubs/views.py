from django.http import HttpResponse
from django.shortcuts import render

from clubs.models import *
from movies.models import Movie


# Create your views here.
def vote(request, club_pk, movie_pk):
    club: Club = Club.objects.get(pk=club_pk)
    movie: Movie = Movie.objects.get(pk=movie_pk)

    existing_vote = Vote.objects.filter(user=request.user, club=club).first()
    if existing_vote:
        # If the user has already voted, you can choose to update their vote or prevent them from voting again
        existing_vote.movie = movie  # Update the vote to the new movie
        existing_vote.save()
    else:
        # Create a new vote
        Vote.objects.create(user=request.user, club=club, movie=movie)

    return HttpResponse("unvote")
