from django.db import models
from django.shortcuts import get_object_or_404
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
        try:
            vote: Vote = Vote.objects.get(user=user, club=self)
            return vote.movie
        except:
            return None

    def pick_movie(self):
        if self.vote_movies.count() <= 0:
            raise Exception("No votes have been initiated")

        votes = Vote.objects.filter(club=self)
        if votes.count() <= 0:
            # No votes have been cast, so pick a random movie from the club's available movies
            movie = self.vote_movies.order_by("?").first()
            if not movie:
                raise Exception("No movies available to pick")
            self.next_movie = movie
            self.vote_movies.clear()
            self.save()
            return

        voted = {}
        for vote in votes:
            key = str(vote.movie.pk)
            voted[key] = voted.get(key, 0) + 1

            print(voted)
            key_with_most = max(voted, key=voted.get)
            print(key_with_most)
            movie: Movie = get_object_or_404(Movie, pk=key_with_most)

        self.next_movie = movie
        self.vote_movies.clear()
        self.save()


    def pick_votes(self):
        # Clear any existing movies in the vote list.
        self.vote_movies.clear()
        votes = Vote.objects.filter(club=self).delete()
        self.past_movies.add(self.next_movie)
        self.next_movie = None

        # Iterate over the queryset of users.
        for member in self.users.all():
            # Check if the user's movie list is not empty.
            if member.movie_list.exists():
                # Get a single random movie from the user's list.
                random_movie = member.movie_list.order_by('?').first()

                # Add the movie to the vote_movies list.
                if random_movie:
                    self.vote_movies.add(random_movie)

        # Save the changes to the instance.
        self.save()
