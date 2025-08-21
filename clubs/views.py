from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from clubs.models import *
from movies.models import Movie
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Club

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

class SetPickForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ['next_pick']  # Only include the next_pick field
        widgets = {
            'next_pick': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

def schedule(request, club_pk):
    club = get_object_or_404(Club, pk=club_pk)

    if request.method == 'POST':
        form = SetPickForm(request.POST, instance=club)
        if form.is_valid():
            form.save()  # Save the updated club instance
            return redirect('/', club_pk=club.pk)  # Redirect to the club detail page
    else:
        form = SetPickForm(instance=club)  # Pre-fill the form with the current club data

    return render(request, 'yes', {})

def set_selected_club(request):
    user: Profile = request.user
    club: Club = Club.objects.get(pk=int(request.POST['selected_club']))
    user.selected_club = club
    user.save()
    return redirect(request.POST['current_path'])

def votes(request, movie_pk):
    movie: Movie = Movie.objects.get(pk=movie_pk)
    club: Club = request.user.selected_club
    votes = Vote.objects.filter(movie=movie, club=club)
    for vote in votes:
        print(vote)
    return render(request,"components/vote-progress.html",{"votes":int(len(votes)/club.users.count()*100)})


def create_vote(request, club_pk):
    club: Club = get_object_or_404(Club,pk=club_pk)
    club.pick_votes()
    return HttpResponse("Done")

def pick_movie(request, club_pk):
    club: Club = get_object_or_404(Club,pk=club_pk)
    club.pick_movie()
    return HttpResponse("Done")
