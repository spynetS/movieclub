from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from movies.models import Movie
from .models import Rating

# Create your views here.
def create_or_update_rating(request: HttpRequest, movie_pk) -> HttpResponse:
    """
    Creates or updates a user's detailed rating for a movie.
    """
    if request.method == 'POST':
        movie: Movie = get_object_or_404(Movie, pk=movie_pk)
        user_profile: Profile = request.user

        # Retrieve each rating component from the POST data
        look_rating = request.POST.get('look')
        script_rating = request.POST.get('script')
        acting_rating = request.POST.get('acting')
        soundtrack_rating = request.POST.get('soundtrack')
        bonus_rating = request.POST.get('bonus')
        overall_score = request.POST.get('overalscore')
        description = request.POST.get('description')


        try:

            rating, created = Rating.objects.get_or_create(
                user=user_profile,
                movie=movie,
                defaults={
                    'look': look_rating,
                    'script': script_rating,
                    'acting': acting_rating,
                    'soundtrack': soundtrack_rating,
                    'bonus': bonus_rating,
                    'overalscore': overall_score,
                    'description': description,
                }
            )
        except:
            return HttpResponse("Cant do that!")


        # If the rating already existed, update its values
        if not created:
            rating.look = look_rating
            rating.script = script_rating
            rating.acting = acting_rating
            rating.soundtrack = soundtrack_rating
            rating.bonus = bonus_rating
            rating.overalscore = overall_score
            rating.description = description
            rating.save()

        return redirect('movie',movie.imdb_id)

    # Handle GET requests (e.g., if someone visits the URL directly)
    return redirect('movie')
