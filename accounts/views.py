from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

# Create your views here.
# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import ProfileSignupForm, ProfileLoginForm

def signup_view(request):
    if request.method == "POST":
        form = ProfileSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/")  # change to your home url name
    else:
        form = ProfileSignupForm()
    return render(request, "accounts/signup.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = ProfileLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # handle next param if present
            next_url = request.GET.get("next") or request.POST.get("next") or "/"
            return redirect(next_url)
    else:
        form = ProfileLoginForm()
    return render(request, "accounts/login.html", {"form": form})

@login_required
def logout_view(request):
    logout(request)
    return redirect("login")
