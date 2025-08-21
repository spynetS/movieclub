# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

from movies.models import Movie

class Profile(AbstractUser):
    # Add any additional fields you want here
    bio = models.TextField(blank=True, null=True)
    movie_list = models.ManyToManyField(Movie, related_name="profiles")
    selected_club = models.ForeignKey("clubs.Club",on_delete=models.DO_NOTHING, null=True,blank=True)
    def __str__(self):
        return self.username

    def get_selected_club_vote(self):
        return self.selected_club.get_voted_movie(self)
