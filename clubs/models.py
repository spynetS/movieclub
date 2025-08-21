from django.db import models
from accounts.models import Profile
from movies.models import Movie  # Ensure you import Movie from the correct module

class Vote(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)  # User who voted
    club = models.ForeignKey('Club', on_delete=models.CASCADE)  # Club where the vote is cast
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)  # Movie being voted for

    class Meta:
        unique_together = ('user', 'club')  # Ensure one vote per user per club

    def __str__(self):
        return f"{self.user.username} voted for {self.movie.title} in {self.club.name}"

class Club(models.Model):
    name = models.CharField(max_length=200, default="")  # Use CharField for better validation
    description = models.TextField(null=True, blank=True)  # Optional description of the club
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the club was created
    past_movies = models.ManyToManyField(Movie, related_name='past_clubs', blank=True)  # Movies watched by the club
    vote_movies = models.ManyToManyField(Movie, related_name='voted_clubs', blank=True)  # Movies available for voting
    next_movie = models.ForeignKey(Movie, on_delete=models.SET_NULL, null=True, blank=True)  # Next movie to watch

    users = models.ManyToManyField(Profile, related_name='clubs', blank=True)  # Users in the club
    owner = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="my_club",null=True,blank=True)

    next_pick = models.DateTimeField(null=True, blank=True)  # Date and time of the next pick

    def format_next_pick(self):
        # Check if next_pick is set
        if self.next_pick:
            # Format the date and time
            return self.next_pick.isoformat()
        return "No upcoming pick"

    def __str__(self):
        return self.name

    def get_voted_movie(self, user: Profile):
        vote: Vote = Vote.objects.get(user=user, club=self)
        return vote.movie

    def pick_new_movie(self):
        # picks random movie, which hasnt been picked jet, from the mebers lists
        pass
