from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path("clubs/", lambda request: render(request, "clubs.html", {}), name="clubs"),
]
