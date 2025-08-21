from django.contrib.auth.forms import User
from django.db import models

from movies.models import Movie
from accounts.models import Profile
from django.utils import timezone
from datetime import timedelta

# Create your models here.

class Rating(models.Model):
    look        = models.DecimalField(decimal_places=2,max_digits=4,null=True)
    script      = models.DecimalField(decimal_places=2,max_digits=4,null=True)
    acting      = models.DecimalField(decimal_places=2,max_digits=4,null=True)
    soundtrack  = models.DecimalField(decimal_places=2,max_digits=4,null=True)
    bonus       = models.DecimalField(decimal_places=2,max_digits=4,null=True)
    overalscore = models.DecimalField(decimal_places=2,max_digits=4,null=True)
    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set at creation

    movie = models.ForeignKey(Movie,on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(Profile,on_delete=models.CASCADE, related_name="ratings")

    def save(self, *args, **kwargs):
        # Call the superclass's save method
        super().save(*args, **kwargs)

        # Check for existing ratings with null movie and older than 1 hour
        one_hour_ago = timezone.now() - timedelta(minutes=20)
        Rating.objects.filter(look__isnull=True, created_at__lt=one_hour_ago).delete()

    def average(self):
        # Create a list of all the fields
        fields = [self.look, self.script, self.acting, self.soundtrack, self.bonus, self.overalscore]
        # Filter out None values
        valid_scores = [score for score in fields if score is not None]

        # If there are no valid scores, return None to indicate no average can be computed
        if len(valid_scores) == 0:
            return None

        # Calculate the average of non-null scores
        return sum(valid_scores) / (len(valid_scores)-1) # we dont divide with the bonus

    def __str__(self):
        return self.movie.title if self.movie != None else ""
