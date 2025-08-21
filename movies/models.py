from datetime import datetime
import os
from django.db import models
import requests

class Director(models.Model):
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)  # Optional field
    biography = models.TextField(null=True, blank=True)  # Optional field

    def __str__(self):
        return self.name


class Rating(models.Model):
    source = models.CharField(max_length=100)
    value = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.source}: {self.value}"

class Movie(models.Model):
    title = models.CharField(max_length=200)
    year = models.CharField(max_length=4)
    rated = models.CharField(max_length=10, null=True)
    released = models.DateField(null=True)
    runtime = models.CharField(max_length=20, null=True)
    genre = models.CharField(max_length=100, null=True)
    director = models.ForeignKey(Director, on_delete=models.CASCADE, related_name='movies', null=True)
    writer = models.CharField(max_length=100, null=True)
    actors = models.TextField(null=True)
    plot = models.TextField(null=True)
    language = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=100, null=True)
    awards = models.TextField(null=True)
    poster = models.URLField()
    metascore = models.CharField(max_length=10, null=True)
    imdb_rating = models.CharField(max_length=10, null=True)
    imdb_votes = models.CharField(max_length=20, null=True)
    imdb_id = models.CharField(max_length=20, unique=True)
    movie_type = models.CharField(max_length=20)
    dvd = models.CharField(max_length=10, null=True)
    box_office = models.CharField(max_length=20, null=True)
    production = models.CharField(max_length=100, null=True)
    website = models.URLField(null=True)
    response = models.BooleanField(default=True)
    ratings = models.ManyToManyField(Rating, related_name='movies')

    def __str__(self):
        return self.title

    def sync(self):
        api = os.getenv("OMDB_API_KEY")
        url = f"https://www.omdbapi.com/?i={self.imdb_id}&apikey={api}&plot=full"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            # Update the model fields with the data from the API response
            self.title = data.get("Title")
            self.year = data.get("Year")
            self.rated = data.get("Rated")
            self.runtime = data.get("Runtime")
            self.genre = data.get("Genre")
            # Update the director field
            director_name = data.get("Director")
            director, created = Director.objects.get_or_create(name=director_name)
            self.director = director
            self.writer = data.get("Writer")
            self.actors = data.get("Actors")
            self.plot = data.get("Plot")
            self.language = data.get("Language")
            self.country = data.get("Country")
            self.awards = data.get("Awards")
            self.poster = data.get("Poster")
            self.metascore = data.get("Metascore")
            self.imdb_rating = data.get("imdbRating")
            self.imdb_votes = data.get("imdbVotes")
            self.movie_type = data.get("Type")
            self.dvd = data.get("DVD")
            self.box_office = data.get("BoxOffice")
            self.production = data.get("Production")
            self.website = data.get("Website")
            self.response = data.get("Response") == "True"

            # Convert the released date to the correct format
            released_date_str = data.get("Released")
            if released_date_str and released_date_str != "N/A":
                try:
                    released_date = datetime.strptime(released_date_str, "%d %b %Y")
                    self.released = released_date.date()
                except ValueError:
                    self.released = None

            self.save()
        else:
            print(f"Error fetching data: {response.status_code}")

    def get_average_rating(self):
        from ratings.models import Rating
        from django.db.models import Avg, F, ExpressionWrapper, IntegerField

        rating = Rating.objects.filter(movie=self).annotate(
            avg_look=Avg('look'),
            avg_script=Avg('script'),
            avg_acting=Avg('acting'),
            avg_soundtrack=Avg('soundtrack'),
            avg_overalscore=Avg('overalscore'),
            avg_bonus=Avg('bonus'),
            avg_total=ExpressionWrapper(
                (F('look') + F('script') + F('acting') + F('soundtrack') + F('overalscore') + F('bonus')) / 5,
                output_field=IntegerField()
            )
        )[0]
        return rating

    def get_average_rating_5(self):
        from ratings.models import Rating
        from django.db.models import Avg, F, ExpressionWrapper, IntegerField

        rating = Rating.objects.filter(movie=self).annotate(
            avg_look=Avg('look')/ (2),
            avg_script=Avg('script')/ (2),
            avg_acting=Avg('acting')/ (2),
            avg_soundtrack=Avg('soundtrack')/ (2),
            avg_overalscore=Avg('overalscore')/ (2),
            avg_bonus=Avg('bonus')/ (2),
            avg_total=ExpressionWrapper(
                (F('look') + F('script') + F('acting') + F('soundtrack') + F('overalscore') + F('bonus')) / (5*2),
                output_field=IntegerField()
            )
        )[0]
        return rating
