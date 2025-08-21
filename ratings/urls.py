from django.contrib import admin
from django.urls import path

from movies.models import *
from .views import *

urlpatterns = [
    path("create-or-update-rating/<int:movie_pk>/",create_or_update_rating,name="create-or-update-rating"),

]
