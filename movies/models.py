from django.db import models

# Create your models here.
class Rating(models.Model):
    source = models.CharField(max_length=100)
    value = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.source}: {self.value}"

class Movie(models.Model):
    title = models.CharField(max_length=200)
    year = models.CharField(max_length=4)
    rated = models.CharField(max_length=10)
    released = models.DateField()
    runtime = models.CharField(max_length=20)
    genre = models.CharField(max_length=100)
    director = models.CharField(max_length=100)
    writer = models.CharField(max_length=100)
    actors = models.TextField()
    plot = models.TextField()
    language = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    awards = models.TextField()
    poster = models.URLField()
    metascore = models.CharField(max_length=10)
    imdb_rating = models.CharField(max_length=10)
    imdb_votes = models.CharField(max_length=20)
    imdb_id = models.CharField(max_length=20, unique=True)
    movie_type = models.CharField(max_length=20)
    dvd = models.CharField(max_length=10)
    box_office = models.CharField(max_length=20)
    production = models.CharField(max_length=100)
    website = models.URLField()
    response = models.BooleanField(default=True)
    ratings = models.ManyToManyField(Rating, related_name='movies')

    def __str__(self):
        return self.title
