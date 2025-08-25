#!/usr/bin/env python3

# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class ProfileCreationForm(UserCreationForm):
    class Meta:
        model = Profile
        fields = ('username', 'email')

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile

# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile

INPUT_CLASSES = "input input-bordered w-full"
LABEL_CLASSES = "label"
HELP_CLASSES = "text-sm text-gray-500"

class ProfileSignupForm(UserCreationForm):
    email = forms.EmailField(required=True,
                             widget=forms.EmailInput(attrs={"class": INPUT_CLASSES, "placeholder": "you@example.com"}))
    bio = forms.CharField(required=False, widget=forms.Textarea(attrs={
        "class": "textarea textarea-bordered w-full", "rows": 3, "placeholder": "A short bio..."
    }))

    class Meta:
        model = Profile
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add classes to user/password fields
        self.fields["username"].widget = forms.TextInput(attrs={"class": INPUT_CLASSES, "placeholder": "username"})
        self.fields["password1"].widget = forms.PasswordInput(attrs={"class": INPUT_CLASSES, "placeholder": "password"})
        self.fields["password2"].widget = forms.PasswordInput(attrs={"class": INPUT_CLASSES, "placeholder": "confirm password"})


class ProfileLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].widget = forms.TextInput(attrs={"class": INPUT_CLASSES, "autofocus": True, "placeholder": "username or email"})
        self.fields["password"].widget = forms.PasswordInput(attrs={"class": INPUT_CLASSES, "placeholder": "password"})
