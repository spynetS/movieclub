from django.db import models
from accounts.models import Profile
from movies.models import Movie  # Ensure you import Movie from the correct module

class Club(models.Model):
    name = models.CharField(max_length=200, default="")  # Use CharField for better validation
    description = models.TextField(null=True, blank=True)  # Optional description of the club
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the club was created
    past_movies = models.ManyToManyField(Movie, related_name='past_clubs', blank=True)  # Movies watched by the club
    vote_movies = models.ManyToManyField(Movie, related_name='voted_clubs', blank=True)  # Movies available for voting
    next_movie = models.ForeignKey(Movie, on_delete=models.SET_NULL, null=True, blank=True)  # Next movie to watch

    users = models.ManyToManyField(Profile, related_name='clubs', blank=True)  # Users in the club

    owner = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="my_club",null=True,blank=True)

    def __str__(self):
        return self.name
